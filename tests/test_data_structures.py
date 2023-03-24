import json
import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.data_structures import *

def test_dict_basic():
    d = CaseFoldDict()
    d['A'] = 1
    assert 'a' in d
    assert d['a'] == 1

    d = CaseFoldDict({'A': 1})
    assert 'a' in d
    assert d['a'] == 1


def test_dict_comparison():
    d1 = CaseFoldDict()
    d2 = CaseFoldDict()
    d1['a'] = 1
    d1['B'] = 2

    d2['A'] = 1
    d2['b'] = 2

    assert d1 == d2
    assert d1.keys() == d2.keys()


def test_set_basic():
    d = CaseFoldSet()
    d.add('A')
    assert 'a' in d
    assert 'A' in d

    d = CaseFoldSet(['A'])
    assert 'a' in d
    assert 'A' in d

    d.add('b')
    d = CaseFoldSet(['a']) | CaseFoldSet(['B'])
    assert 'b' in d

    d.add('É')
    assert 'é' in d


def test_set_comparison():
    d1 = CaseFoldSet()
    d2 = CaseFoldSet()
    d1.add('a')
    d2.add('A')

    assert d1 == d2


def test_json_dumps_dict():
    s = json.dumps(CaseFoldDict({'A': 1, 'B': 2}))
    assert 'A' in s
    assert 'B' in s
