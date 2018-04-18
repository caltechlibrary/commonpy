
import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy import http_code

class TestClass:
    def test_http_meanings(self, capsys):
        assert http_code.description(200) == "The request has succeeded."
