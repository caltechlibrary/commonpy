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

from   boltons.strutils import pluralize
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


def expanded_range(text):
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


def parsed_datetime(string):
    '''Parse a human-written time/date string using dateparser's parse()
function with predefined settings.'''
    # Dateparser imports regex, a large package that takes a long time to load.
    # Delay loading it so that application startup times can be faster.
    import dateparser
    return dateparser.parse(string, settings = {'RETURN_AS_TIMEZONE_AWARE': True})


def pluralized(word, count, include_number = False):
    '''Pluralize the "word" if "count" is > 1 or has length > 1.

    If "include_number" is true, then the value of "count" will be prepended
    before the string:

        files_list = ['one.txt', 'two.txt', 'three.txt']
        plural('file', files_list)       --> 'files'
        plural('file', files_list, True) --> '3 files'

    This function is useful in f-strings when words refer to a number of items
    whose total or length is only known at run time.  For example,

       f"Uploading {pluralized('file', files_list, True)} to server."
    '''

    if isinstance(count, int):
        num = count
    elif isinstance(count, (list, set, dict)) or type(count) is {}.values().__class__:
        num = len(count)
    else:
        # If we can't figure out what kind of thing we're counting, we can't
        # pluralize, so just return the word as-is.
        return word
    text = pluralize(word) if num > 1 else word
    if include_number:
        # Humanize imports pkg_resources, which takes a long time to load.
        # Delay loading it so that application startup times can be faster.
        from humanize import intcomma
        return f'{intcomma(num)} {text}'
    else:
        return text
