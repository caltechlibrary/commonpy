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

    s = str(s)
    s = s.replace('{{', '⁌').replace('}}', '⁍')
    s = s.replace('{', '{{').replace('}', '}}')
    return s.replace('⁌', '{').replace('⁍', '}')


# The following is based on code posted by user "Darkonaut" to Stack Overflow
# on 2019-11-09 at https://stackoverflow.com/a/58780542/743730
# The version below uses pure ASCII characters so that it will format normally
# in, e.g., server log files.

def print_boxed(msg, indent = 1, width = None, title = None):
    '''Print a boxed message with optional title.

    If optional parameter "width" is not set, this will use the width of
    the longest line in the "msg" text.
    '''

    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f',{"-" * (width + indent * 2)}.\n'
    if title:
        box += f'|{space}{title:<{width}}{space}|\n'             # title
        box += f'|{space}{"-" * len(title):<{width}}{space}|\n'  # underscore
    box += ''.join([f'|{space}{line:<{width}}{space}|\n' for line in lines])
    box += f'`{"-" * (width + indent * 2)}\''
    print(box)
