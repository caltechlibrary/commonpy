import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.http_code import *

class TestClass:
    def test_http_meanings(self, capsys):
        assert http_code_meaning(200) == "The request has succeeded."
