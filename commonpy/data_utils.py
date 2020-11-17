'''
data_utils: data manipulation utilities

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import dateparser
import datetime
from   datetime import datetime as dt
from   dateutil import tz


# Constants.
# .............................................................................

DATE_FORMAT = '%b %d %Y %H:%M:%S %Z'
'''Format in which lastmod date is printed back to the user. The value is used
with datetime.strftime().'''


# Functions.
# .............................................................................

def slice(lst, n):
    '''Yield n number of slices from lst.'''
    # Original algorithm from Jurgen Strydom posted 2019-02-21 Stack Overflow
    # https://stackoverflow.com/a/54802737/743730
    for i in range(0, n):
        yield lst[i::n]


def unique(lst):
    '''Take list "lst" and return a version without duplicates.'''
    # This exists because I think the intention behind list(set(...)) is
    # too easily lost and makes code muddier.
    return list(set(lst))


def ordinal(n):
    '''Print a number followed by "st" or "nd" or "rd", as appropriate.'''
    # Spectacular algorithm by user "Gareth" at this posting:
    # http://codegolf.stackexchange.com/a/4712
    return '{}{}'.format(n, 'tsnrhtdd'[(n/10%10!=1)*(n%10<4)*n%10::4])


def expand_range(text):
    '''Return individual numbers for a range expressed as X-Y.'''
    # This makes the range 1-100 be 1, 2, ..., 100 instead of 1, 2, ..., 99
    if '-' in text:
        range_list = text.split('-')
        # Malformed cases of -x, where first number is missing.  Take it as 1.
        if not range_list[0].isdigit():
            range_list = [1, range_list[1]]
        # Malformed cases of x-, where 2nd number missing.  Can't handle this.
        if not range_list[1].isdigit():
            raise ValueError(f'Malformed range expression: "{text}"')
        range_list.sort(key = int)
        return [*map(str, range(int(range_list[0]), int(range_list[1]) + 1))]
    else:
        return text


def timestamp():
    '''Return a string describing the date and time right now.'''
    return dt.now(tz = tz.tzlocal()).strftime(DATE_FORMAT)


def parse_datetime(string):
    '''Parse a human-written time/date string using dateparser's parse()
function with predefined settings.'''
    return dateparser.parse(string, settings = {'RETURN_AS_TIMEZONE_AWARE': True})


def plural(word, count):
    '''Simple pluralization; adds "s" to the end of "word" if count > 1.'''
    if isinstance(count, int):
        num = count
    elif isinstance(count, (list, set, dict)) or type(count) is {}.values().__class__:
        num = len(count)
    else:
        # If we don't recognize the kind of thing it is, return it unchanged.
        return word
    if num > 1:
        return word + 's' if not word.endswith('s') else word
    else:
        return word
