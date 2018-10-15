#!/usr/bin/env python

'''
    The time complexity is O(N + M) where N is number of patterns and M is
    number of paths.

    I wrote the PatternMap class keeping in mind that the code is supposed to
    be as generic as possible. Hopefully it does not come off as over-
    engineered.
'''

import re

class PatternMap:
    """
        Map for searching for a matching pattern. 

        Example of how it works internally:

        addPattern(('a','b','c'))
        self.__map = {'a': {'b': {'c': {'COMPLETE': ('a','b','c')} } } }
        addPattern(('a','b','d','e'))
        self.__map = {'a': {'b': {'c': {'COMPLETE': ('a','b','c')},
                                  'd': {'e': {'COMPLETE': ('a','b','d','e'} } }
                      } }

        In this way any number of patterns can be added to the map without
        slowing down matching functionality.
    """
    
    def __init__(self, wildcard='*', complete=hash('COMPLETE')):
        """
            Initializes the PatternMap.

            @param wildcard (default '*'): this str will match any field
            @param complete (default hash('COMPLETE')): indicates a match,
                this value should never be given in a path
        """
        self.__map = {}
        self.__wildcard = wildcard
        self.__complete = complete

    def addPattern(self, pattern):
        """
            Adds {pattern} to the map.

            @type pattern: iterable
        """
        current = self.__map

        for field in pattern:
            if field not in current:
                current[field] = {}
            current = current[field]

        current[self.__complete] = pattern

    def matchPath(self, path):
        """
            Checks if {path} is in the map. Returns the match pattern
            if a match is found, None otherwise

            @type path: iterable
            @rtype: iterable or None
        """
        current = self.__map

        for field in path:
            if field in current:
                current = current[field]
            elif self.__wildcard in current:
                current = current[self.__wildcard]
            else:
                return None

        return current.get(self.__complete)

    def __repr__(self):
        return 'PatternMap(' + str(self.__map) + ')'


if __name__ == "__main__":

    pattern_map = PatternMap()
    paths = []
    
    # get N number of patterns
    num_patterns = int(raw_input())
    for i in range(num_patterns):
        pattern_str = raw_input()
        # convert the pattern to a tuple (for immutability) and add to pattern_map
        pattern_map.addPattern(tuple(pattern_str.split(',')))

    # get M number of paths
    num_paths = int(raw_input())
    # regex for stripping '/' at the beginning and end of the str
    path_re = re.compile(r'/?(?P<path>((?!/$).)*)')
    for i in range(num_paths):
        path_str = raw_input()
        path_str = path_re.match(path_str).group('path')
        paths.append(tuple(path_str.split('/')))

    # match paths
    for path in paths:
        match = pattern_map.matchPath(path)
        if match is not None:
            print ','.join(match)
        else:
            print 'NO MATCH'
