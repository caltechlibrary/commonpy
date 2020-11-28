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

def antiformat(s):
    '''Quote instances of '{' and '}' in 's' so it can be passed to format.'''

    # This is a combo of 2 solutions posted by Stack Overflow users:
    # Kristján Valur (2019-12-17): https://stackoverflow.com/a/59371315/743730
    # "clickbait" (2018-07-31): https://stackoverflow.com/a/51623363/743730

    s = s.replace('{{', '⁌').replace('}}', '⁍')
    s = s.replace('{', '{{').replace('}', '}}')
    return s.replace('⁌', '{').replace('⁍', '}')
