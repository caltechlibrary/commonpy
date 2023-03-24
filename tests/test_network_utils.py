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


def test_net_fail_no_content():
    (response, error) = net('get', 'https://library.caltech.edu/foobarbaz')
    assert isinstance(error, NoContent)
    assert response.status_code == 404


def test_net_bad_args():
    (response, error) = net('get', 'https://www.google.com', data = {'foo': 1})
    assert isinstance(error, ArgumentError)
    assert response == None


def test_hostname():
    assert hostname('https://foo.com')             == 'foo.com'
    assert hostname('http://a.b.c')                == 'a.b.c'
    assert hostname('file://a.b.c')                == 'a.b.c'
    assert hostname('ftp://a.b.c')                 == 'a.b.c'
    assert hostname('gopher://a.b.c')              == 'a.b.c'
    assert hostname('http://aserver.com')          == 'aserver.com'
    assert hostname('aserver.com')                 == 'aserver.com'
    assert hostname('aserver.com/some/path')       == 'aserver.com'
    assert hostname('http://9292.nl/boo')          == '9292.nl'
    assert hostname('http://123.345.234.655/a/b')  == '123.345.234.655'
    assert hostname('//mywebsite.com/resource.js') == 'mywebsite.com'


def test_scheme():
    assert scheme('https://foo.com') == 'https'
    assert scheme('http://a.b.c')    == 'http'
    assert scheme('file://a.b.c')    == 'file'
    assert scheme('ftp://a.b.c')     == 'ftp'
    assert scheme('gopher://a.b.c')  == 'gopher'
    assert scheme('aserver.com')     == ''


def test_netloc():
    assert netloc('https://foo.com') == 'foo.com'
    assert netloc('aserver.com')     == 'aserver.com'
    assert netloc('ftp://a.b.c')     == 'a.b.c'
