'''
Commonpy: an assortment of Python helper functions and utility classes

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2018-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

# Package metadata ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#  ╭────────────────────── Notice ── Notice ── Notice ─────────────────────╮
#  |    The following values are automatically updated at every release    |
#  |    by the Makefile. Manual changes to these values will be lost.      |
#  ╰────────────────────── Notice ── Notice ── Notice ─────────────────────╯

__version__     = '0.0.2'
__description__ = 'Assortment of Python helper functions and utility classes'
__url__         = 'https://github.com/caltechlibrary/commonpy'
__author__      = 'Michael Hucka'
__email__       = 'mhucka@caltech.edu'
__license__     = 'BSD 3-clause'


# Main exports.
# .............................................................................

from .data_utils import *
from .file_utils import *
from .http_code import *
from .system_utils import *


# Miscellaneous utilities.
# .............................................................................

def print_version():
    print(f'{__name__} version {__version__}')
    print(f'Authors: {__author__}')
    print(f'URL: {__url__}')
    print(f'License: {__license__}')
