import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.network_utils import *
from commonpy.exceptions import *


def test_network_available():
    assert network_available()


def test_net():
    (response, error) = net('get', 'https://www.google.com')
    assert error == None
    assert response.status_code == 200


def test_on_localhost():
    assert on_localhost('localhost')
    assert on_localhost('127.0.0.1')


def test_net_fail_bad_address():
    (response, error) = net('get', 'https://www.nonexistent.foo')
    assert isinstance(error, ServiceFailure)
    assert response == None


def test_net_fail_refused_connection():
    (response, error) = net('get', 'https://www.library.caltech.edu/admin')
    assert isinstance(error, AuthenticationFailure)
    assert response.status_code == 403


def test_net_bad_args():
    (response, error) = net('get', 'https://www.google.com', data = {'foo': 1})
    assert isinstance(error, ArgumentError)
    assert response == None


def test_hostname():
    assert hostname('https://foo.com')            == 'foo.com'
    assert hostname('http://a.b.c')               == 'a.b.c'
    assert hostname('file://a.b.c')               == 'a.b.c'
    assert hostname('ftp://a.b.c')                == 'a.b.c'
    assert hostname('gopher://a.b.c')             == 'a.b.c'
    assert hostname('http://8server.com')         == '8server.com'
    assert hostname('8server.com')                == '8server.com'
    assert hostname('http://9292.nl/boo')         == '9292.nl'
    assert hostname('http://123.345.234.655/a/b') == '123.345.234.655'


def test_scheme():
    assert scheme('https://foo.com') == 'https'
    assert scheme('http://a.b.c')    == 'http'
    assert scheme('file://a.b.c')    == 'file'
    assert scheme('ftp://a.b.c')     == 'ftp'
    assert scheme('gopher://a.b.c')  == 'gopher'
    assert scheme('8server.com')     == ''


def test_netloc():
    assert netloc('https://foo.com') == 'foo.com'
    assert netloc('8server.com')     == '8server.com'
    assert netloc('ftp://a.b.c')     == 'a.b.c'
