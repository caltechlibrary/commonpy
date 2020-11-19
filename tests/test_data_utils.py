import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.data_utils import *


def test_slice():
    assert list(slice([1, 2, 3, 4], 2)) == [[1, 3], [2, 4]]
    assert list(slice([1, 2, 3, 4, 5], 2)) == [[1, 3, 5], [2, 4]]


def test_expand_range():
    assert expand_range('1-5') == ['1', '2', '3', '4', '5']
    assert expand_range('2-10') == ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    assert expand_range('-5') == ['1', '2', '3', '4', '5']
    try:
        # It's a malformed expression.
        assert expand_range('5-') == '5-'
    except ValueError:
        pass
    except Exception:
        raise


def test_unique():
    assert unique([1, 2, 3]) == [1, 2, 3]
    assert unique([1, 2, 3, 3]) == [1, 2, 3]
    assert unique([3, 2, 2]) == [2, 3]


def test_ordinal():
    assert ordinal(1) == '1st'
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(4) == '4th'
    assert ordinal(5) == '5th'
    assert ordinal(10) == '10th'


def test_plural():
    assert plural('flower', 1) == 'flower'
    assert plural('flower', 2) == 'flowers'
    assert plural('error', [1]) == 'error'
    assert plural('error', [1, 2]) == 'errors'
    assert plural('word', 3) == 'words'
    assert plural('bus', 3) == 'buses'
    assert plural('theory', 2) == 'theories'
    assert plural('dictionary', 2) == 'dictionaries'
