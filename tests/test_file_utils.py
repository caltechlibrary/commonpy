import os
import pytest
import sys
from   time import time

try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

from commonpy.file_utils import *


def test_writable(tmpdir):
    assert writable(tmpdir)


def test_readable_and_nonempty(tmpdir):
    tmpfile = tmpdir.join('test.txt')
    with open(tmpfile, 'w') as f:
        f.write('foo\n')
    assert readable(tmpfile)
    assert nonempty(tmpfile)


def test_files_in_directory(tmpdir):
    tmpfile = tmpdir.join('test.txt')
    with open(tmpfile, 'w') as f:
        f.write('foo\n')
    assert files_in_directory(tmpdir)[0].endswith('test.txt')


def test_basenames_and_extensions():
    assert filename_basename('/foo/bar.txt') == '/foo/bar'
    assert filename_extension('/foo/bar.txt') == '.txt'
    assert filename_extension('foo') == ''
    assert filename_extension('/foo/bar.bif.j') == '.j'
    assert alt_extension('/foo.app/bar.txt', 'zip') == '/foo.app/bar.zip'


def test_copy_rename_delete_files(tmpdir):
    tmpfile1 = tmpdir.join('test1.txt')
    with open(tmpfile1, 'w') as f:
        f.write('foo\n')
    copy_file(tmpfile1, 'copy1.txt')
    assert readable('copy1.txt')
    rename_existing('copy1.txt')
    assert readable('copy1.txt.bak')
    delete_existing('copy1.txt.bak')
    assert not readable('copy1.txt.bak')

def test_relative():
    p = os.path.join(os.path.abspath('.'), '..', 'setup.cfg')
    assert relative(p) == '../setup.cfg'
