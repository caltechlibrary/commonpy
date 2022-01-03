'''
data_structures: data structures

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2022 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

import collections


# Classes.
# .............................................................................

# The following code is based in part on a posting by user 'mloskot' on
# 2018-06-28 to Stack Overflow at https://stackoverflow.com/a/51083318/743730
# with some additional ideas from CaseInsensitiveDict from requests.structures
# (version 3.0.0).

class CaseFoldDict(collections.OrderedDict):
    '''A subclass of OrderedDict that compares keys in a case-fold manner.'''

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
