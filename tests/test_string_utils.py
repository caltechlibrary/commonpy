import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.string_utils import *

def test_safe_str(tmpdir):
    assert safe_str('foo') == 'foo'
    assert safe_str('foo {bar') == 'foo {{{{bar'
    assert safe_str('foo {bar').format('bar') == 'foo {{bar'
