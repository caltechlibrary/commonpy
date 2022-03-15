import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.module_utils import *


def test_configpath():
    if not sys.platform.startswith('win'):
        assert config_path('foo') == path.join(path.expanduser('~'), '.config', 'foo')


def test_desktop_path():
    expected = path.join(path.expanduser('~'), 'Desktop')
    if not sys.platform.startswith('win'):
        assert desktop_path() == expected


def test_datadir_path():
    assert datadir_path().endswith('data')
