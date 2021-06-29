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
from   os.path import exists, isdir, isfile, join, dirname, relpath, realpath
from   os.path import splitext
import shutil
import subprocess
import sys
import tempfile
import webbrowser

if __debug__:
    from sidetrack import log


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

    if exists(dest) and not isdir(dest):
        # Path is an existing file.
        return os.access(dest, os.F_OK | os.W_OK)
    elif isdir(dest):
        # Path itself is an existing directory.  Is it writable?
        return dir_writable(dest)
    else:
        # Path is a file but doesn't exist yet. Can we write to the parent dir?
        return dir_writable(dirname(dest))


def nonempty(dest):
    '''Returns True if the file is not empty.'''
    return os.stat(dest).st_size != 0


def files_in_directory(dir, extensions = None, recursive = True):
    if not isdir(dir):
        return []
    if not readable(dir):
        return []
    if __debug__: log(f'reading directory {dir}')
    files = []
    for item in os.listdir(dir):
        full_path = join(dir, item)
        if isfile(full_path) and readable(full_path):
            if not extensions or filename_extension(item) in extensions:
                files.append(full_path)
        elif isdir(full_path) and recursive:
            files += files_in_directory(full_path, extensions)
    return sorted(files)


def filename_basename(file):
    parts = file.rpartition('.')
    if len(parts) > 1:
        return ''.join(parts[:-1]).rstrip('.') if parts[0] else file
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
    return splitext(filepath)[0] + '.' + ext


def filtered_by_extensions(item_list, endings):
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

    # Validator_collection takes a long time to load.  Delay loading it until
    # it's actually needed, so that application startup times can be faster.
    from validator_collection.checkers import is_url

    if is_url(file):
        return file
    try:
        # This can fail on Windows if we're on a network-mapped drive.
        candidate = relpath(file, os.getcwd())
    except Exception as ex:
        return file
    else:
        if not candidate.startswith('../..'):
            return candidate
        else:
            return realpath(candidate)


def rename_existing(file):
    '''Renames 'file' to 'file.bak'.'''

    def rename(f):
        backup = f + '.bak'
        # If we fail, we just give up instead of throwing an exception.
        try:
            os.rename(f, backup)
            if __debug__: log(f'renamed {file} to {backup}')
        except:
            try:
                delete_existing(backup)
                os.rename(f, backup)
            except:
                if __debug__: log(f'failed to delete {backup}')
                if __debug__: log(f'failed to rename {file} to {backup}')

    if exists(file):
        rename(file)
        return
    full_path = join(os.getcwd(), file)
    if exists(full_path):
        rename(full_path)
        return


def delete_existing(file):
    '''Delete the given file.'''
    # Check if it's actually a directory.
    if isdir(file):
        if __debug__: log(f'doing rmtree on directory {file}')
        try:
            shutil.rmtree(file)
        except:
            if __debug__: log(f'unable to rmtree {file}; will try renaming')
            try:
                rename_existing(file)
            except:
                if __debug__: log(f'unable to rmtree or rename {file}')
    else:
        if __debug__: log(f'doing os.remove on file {file}')
        os.remove(file)


def file_in_use(file):
    '''Returns True if the given 'file' appears to be in use.  Note: this only
    works on Windows, currently.
    '''
    if not exists(file):
        return False
    if sys.platform.startswith('win'):
        # This is a hack, and it really only works for this purpose on Windows.
        try:
            os.rename(file, file)
            return False
        except:
            return True
    return False


def copy_file(src, dst):
    '''Copies a file from "src" to "dst".'''
    if __debug__: log(f'copying file {src} to {dst}')
    shutil.copy2(src, dst, follow_symlinks = True)


def open_file(file):
    '''Opens document with default application in Python.'''
    # Code originally from https://stackoverflow.com/a/435669/743730
    if __debug__: log(f'opening file {file}')
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', file))
    elif os.name == 'nt':
        os.startfile(file)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', file))


def open_url(url):
    '''Opens the given 'url' in a web browser using the current platform's
    default approach.'''
    if __debug__: log(f'opening url {url}')
    webbrowser.open(url)
