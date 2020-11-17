'''
data_utils: operating system & platform utilities

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from   boltons import ecoutils
import yaml


# Functions.
# .............................................................................

def system_profile(anonymize = False, as_dict = False):
    '''Return a summary of this system.

    The default output format is a string that is more or less human readable.
    If the value of parameter "as_dict" is True, the output is a Python dict.

    If the value of parameter "anonymize" is True, the results will have values
    of '-' for certain identifiable information.  This includes current working
    directory, hostname, Python executable path, command-line arguments, and
    username.
    '''

    details = ecoutils.get_profile(scrub = anonymize)
    return details if as_dict else yaml.dump(details)
