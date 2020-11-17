'''
file_utils.py: utilities for working with files.

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import inspect
import os
from   os import path
import sys
import tempfile


# Main functions.
# .............................................................................

def readable(dest):
    '''Returns True if the given 'dest' is accessible and readable.'''
    return os.access(dest, os.F_OK | os.R_OK)


def writable(dest):
    '''Returns True if the destination is writable.'''

    # Helper function to test if a directory is writable.
    def dir_writable(dir):
        # This is based on the following Stack Overflow answer by user "zak":
        # https://stackoverflow.com/a/25868839/743730
        try:
            testfile = tempfile.TemporaryFile(dir = dir)
            testfile.close()
        except (OSError, IOError) as e:
            return False
        return True

    if path.exists(dest) and not path.isdir(dest):
        # Path is an existing file.
        return os.access(dest, os.F_OK | os.W_OK)
    elif path.isdir(dest):
        # Path itself is an existing directory.  Is it writable?
        return dir_writable(dest)
    else:
        # Path is a file but doesn't exist yet. Can we write to the parent dir?
        return dir_writable(path.dirname(dest))


def nonempty(dest):
    '''Returns True if the file is not empty.'''
    return os.stat(dest).st_size != 0


def files_in_directory(dir, extensions = None, recursive = True):
    if not path.isdir(dir):
        return []
    if not readable(dir):
        return []
    files = []
    for item in os.listdir(dir):
        full_path = path.join(dir, item)
        if path.isfile(full_path) and readable(full_path):
            if not extensions or filename_extension(item) in extensions:
                files.append(full_path)
        elif path.isdir(full_path) and recursive:
            files += files_in_directory(full_path, extensions)
    return sorted(files)


def filename_basename(file):
    parts = file.rpartition('.')
    if len(parts) > 1:
        return ''.join(parts[:-1]).rstrip('.')
    else:
        return file


def filename_extension(file):
    parts = file.rpartition('.')
    if parts[0] != '' and parts[1] != '':
        return '.' + parts[-1].lower()
    else:
        return ''


def alt_extension(filepath, ext):
    '''Returns the 'filepath' with the extension replaced by 'ext'.  The
    extension given in 'ext' should NOT have a leading period: that is, it
    should be "foo", not ".foo".'''
    return path.splitext(filepath)[0] + '.' + ext


def filter_by_extensions(item_list, endings):
    if not item_list:
        return []
    if not endings:
        return item_list
    results = item_list
    for ending in endings:
        results = list(filter(lambda name: ending not in name.lower(), results))
    return results


def relative(file):
    '''Returns a path that is relative to the current directory.  If the
    relative path would require more than one parent step (i.e., ../../*
    instead of ../*) then it will return an absolute path instead.  If the
    argument is actuall a file path, it will return it unchanged.'''
    if is_url(file):
        return file
    candidate = path.relpath(file, os.getcwd())
    if not candidate.startswith('../..'):
        return candidate
    else:
        return path.realpath(candidate)
