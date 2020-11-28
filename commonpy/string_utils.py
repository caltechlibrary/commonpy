'''
string_utils: string manipulation utilities

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''


# Functions.
# .............................................................................

def safe_str(s):
    '''Quote instances of '{' and '}' in 's' so it can be passed to format.'''
    return s.replace('{', '{{{{').replace('}', '}}}}')
