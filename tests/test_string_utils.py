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

def test_antiformat(tmpdir):
    assert antiformat('foo') == 'foo'
    assert antiformat('foo {bar') == 'foo {{bar'
    assert antiformat('foo {bar').format('bar') == 'foo {bar'
    assert antiformat('foo {bar}') == 'foo {{bar}}'
    assert antiformat('foo {bar}').format('bar') == 'foo {bar}'
    assert antiformat('foo {bar}').format(bar = 'biff') == 'foo {bar}'
    assert antiformat(Exception('test exception')) == 'test exception'
    assert antiformat(b'foo') == "b'foo'"
