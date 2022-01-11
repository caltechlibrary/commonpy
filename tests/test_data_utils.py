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


def test_expanded_range():
    assert expanded_range('1-5') == ['1', '2', '3', '4', '5']
    assert expanded_range('2-10') == ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    assert expanded_range('-5') == ['1', '2', '3', '4', '5']
    try:
        # It's a malformed expression.
        assert expanded_range('5-') == '5-'
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


def test_pluralized():
    assert pluralized('flower', 1) == 'flower'
    assert pluralized('flower', 2) == 'flowers'
    assert pluralized('error', [1]) == 'error'
    assert pluralized('error', [1, 2]) == 'errors'
    assert pluralized('word', 3) == 'words'
    assert pluralized('bus', 3) == 'buses'
    assert pluralized('theory', 2) == 'theories'
    assert pluralized('dictionary', 2) == 'dictionaries'
    assert pluralized('flower', 1, True) == '1 flower'
    assert pluralized('flower', 2, True) == '2 flowers'
    assert pluralized('error', [1, 2], True) == '2 errors'
    assert pluralized('word', 10000, True) == '10,000 words'


def test_flattened():
    assert flattened([[1, 2], 3, [4, 5], []]) == [1, 2, 3, 4, 5]
    original = dict({'a': 1, 'b': {'c': 2}, 'd': {'e': 3, 'f': 4, 'g': [5, 6]}})
    assert flattened(original) == {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}
    assert flattened([original, original]) == [{'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}, {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}]
    assert flattened([[1, 2], original, [original]]) == [1, 2, {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}, {'a': 1, 'b.c': 2, 'd.e': 3, 'd.f': 4, 'd.g.0': 5, 'd.g.1': 6}]
    assert flattened(iter(range(0, 3))) == [0, 1, 2]
    assert flattened(['abc', [1, 2], 'def']) == ['abc', 1, 2, 'def']
    original = r = [('35047019633510',
                     [{'id': '6a904e08-34dd-4392-be3d-7cbe0046c8d2',
                       'status': {'name': 'Available', 'date': '2021-09-15T21:36:13.318+00:00'},
                       'contributorNames': [{'name': 'Back, K. (Kerry)'}],
                       'formerIds': [],
                       'discoverySuppress': None,
                       'tags': {'tagList': []}}])]
    assert flattened(original) == ['35047019633510',
                                   {'id': '6a904e08-34dd-4392-be3d-7cbe0046c8d2',
                                    'status.name': 'Available',
                                    'status.date': '2021-09-15T21:36:13.318+00:00',
                                    'contributorNames.0.name': 'Back, K. (Kerry)',
                                    'formerIds': None,
                                    'discoverySuppress': None,
                                    'tags.tagList': None}]
    x = {'a':1}
    y = {'b':2}
    assert flattened([d.keys() for d in [x, y]]) == ['a', 'b']
    assert flattened([x.keys(), 1, 2, [3], 'a', 'b']) == ['a', 1, 2, 3, 'a', 'b']
