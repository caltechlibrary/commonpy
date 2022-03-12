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
