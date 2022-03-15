from   contextlib import redirect_stdout
import io
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


def test_print_boxed1():
    output = io.StringIO()
    with redirect_stdout(output):
        print_boxed('foo')
    assert output.getvalue() == ",-----.\n| foo |\n`-----'\n"


def test_print_boxed2():
    output = io.StringIO()
    with redirect_stdout(output):
        print_boxed('foo\nbar')
    assert output.getvalue() == ",-----.\n| foo |\n| bar |\n`-----'\n"


def test_print_boxed3():
    output = io.StringIO()
    with redirect_stdout(output):
        print_boxed('foo\nbar', indent = 2)
    assert output.getvalue() == ",-------.\n|  foo  |\n|  bar  |\n`-------'\n"


def test_print_boxed4():
    output = io.StringIO()
    with redirect_stdout(output):
        print_boxed('foo\nbar', width = 8)
    assert output.getvalue() == ",----------.\n| foo      |\n| bar      |\n`----------'\n"


def test_print_boxed5():
    output = io.StringIO()
    with redirect_stdout(output):
        print_boxed('foo\nbar', title = 'wow')
    assert output.getvalue() == ",-----.\n| wow |\n| --- |\n| foo |\n| bar |\n`-----'\n"
