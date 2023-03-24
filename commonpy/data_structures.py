'''
data_structures: data structures

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2022-2023 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import collections
from   collections.abc import MutableSet
from   contextlib import suppress


# Classes.
# .............................................................................

# The following code is based in part on a posting by user 'mloskot' on
# 2018-06-28 to Stack Overflow at https://stackoverflow.com/a/51083318/743730
# with some additional ideas from CaseInsensitiveDict from requests.structures
# (version 3.0.0).

class CaseFoldDict(collections.OrderedDict):
    '''A subclass of OrderedDict that compares keys in a case-fold manner.

    The case of stored values is preserved.
    '''

    class Key(str):
        def __init__(self, key):
            str.__init__(key)

        def __hash__(self):
            return hash(self.casefold())

        def __eq__(self, other):
            return self.casefold() == other.casefold()


    def __init__(self, data=None):
        super(CaseFoldDict, self).__init__()
        if data is None:
            data = {}
        self.update(data)


    def __contains__(self, key):
        key = self.Key(key)
        return super(CaseFoldDict, self).__contains__(key)


    def __setitem__(self, key, value):
        key = self.Key(key)
        super(CaseFoldDict, self).__setitem__(key, value)


    def __getitem__(self, key):
        key = self.Key(key)
        return super(CaseFoldDict, self).__getitem__(key)


    def __eq__(self, other):
        if isinstance(other, dict):
            other = CaseFoldDict(other)
        else:
            return NotImplemented
        return dict(self.items()) == dict(other.items())


# The following code is based in part on a posting by user Martijn Pieters on
# 2020-04-07 to Stack Overflow at https://stackoverflow.com/a/27531275/743730

class CaseFoldSet(MutableSet):
    '''A subclass of MutableSet tests for containment in a case-fold manner.

    The case of values is preserved. Note that this class preserves the case
    of the last-inserted variant; i.e., if the same value is added multiple
    times, but with different cases, the value remembered is the last one.

    Example: the following test will be True:
    > 'Foo' in CaseFoldSet(['FOO'])
    '''
    def __init__(self, *args):
        self._values = {}
        if len(args) > 1:
            raise TypeError(
                f"{type(self).__name__} expected at most 1 argument, "
                f"got {len(args)}"
            )
        values = args[0] if args else ()
        self._fold = str.casefold
        for v in values:
            self.add(v)


    def __repr__(self):
        return '<{}{} at {:x}>'.format(
            type(self).__name__, tuple(self._values.values()), id(self))


    def __contains__(self, value):
        return self._fold(value) in self._values


    def __iter__(self):
        return iter(self._values.values())


    def __len__(self):
        return len(self._values)


    def add(self, value):
        self._values[self._fold(value)] = value


    def discard(self, value):
        with suppress(KeyError):
            del self._values[self._fold(value)]


    def update(self, values):
        for v in values:
            self.add(v)
