'''
module_utils: utilities related to Python modules and packages

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import os
from os import path as path
import sys


# Constants.
# .............................................................................

_APP_REG_PATH_FORMAT = r'Software\Caltech Library\{}\Settings'
'''Format of the the Windows registry path for this application.  Contains one
string format substitution placeholder.  Use this with a call to format(...)
like this: _APP_REG_PATH_FORMAT.format(module).
'''


# Main functions.
# .............................................................................

def module_path(module_name = __package__):
    '''Returns the absolute path to the installation directory of the Python
    module named 'name'.  The name defaults to __package__.
    '''
    if module_name in sys.modules:
        return path.abspath(sys.modules[module_name].__path__[0])
    else:
        return None


def datadir_path(module_name = __package__):
    '''Returns the path to the named module's internal data directory.'''
    return path.join(module_path(module_name), 'data')


def desktop_path():
    '''Returns the path to the user's desktop directory.'''
    if sys.platform.startswith('win'):
        return path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        return path.join(path.expanduser('~'), 'Desktop')


def installation_path(module_name = __package__):
    '''Returns the path to where the given Python package is installed.'''
    # The path returned by module.__path__ is to the directory containing
    # the __init__.py file.  What we want here is the path to the installation
    # of the application binary.
    if sys.platform.startswith('win'):
        from winreg import OpenKey, CloseKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ
        try:
            if __debug__: log('reading Windows registry entry')
            reg_path = _APP_REG_PATH_FORMAT.format(module_name)
            key = OpenKey(HKEY_LOCAL_MACHINE, reg_path)
            value, regtype = QueryValueEx(key, 'Path')
            CloseKey(key)
            if __debug__: log(f'path to windows installation: {value}')
            return value
        except WindowsError:
            # Kind of a problem. Punt and return a default value.
            default_path = path.abspath('C:\\Program Files\\{}'.format(module_name))
            if __debug__: log(f'defaulting to {default_path}')
            return default_path
    else:
        return path.abspath(path.join(module_path(module_name), '..'))


def config_path(module_name = __package__):
    '''Returns the path to ~/.config or equivalent.'''
    if sys.platform.startswith('win'):
        config_root = path.join(os.environ['USERPROFILE'], 'AppData', 'Local')
    else:
        config_root = path.join(path.expanduser('~'), '.config')
    return path.join(config_root, module_name)
