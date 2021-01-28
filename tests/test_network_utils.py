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


def test_net():
    (response, error) = net('get', 'https://www.google.com')
    assert error == None
    assert response.status_code == 200
