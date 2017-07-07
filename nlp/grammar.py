# -*- coding: utf-8 -*-
#
# Author: Florent Piétot <florent.pietot@gmail.com>

""" Basic data classes for representing a basic grammar using trees.
    The leaves of a tree are words, and non-leaves nodes are defined as
    NonTerminals.
    We uses productions to define what tree structures are allowed in the
    grammar.
"""

import re

class Production(object):

    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = tuple(rhs)

    def lhs(self):
        """ Return the left hand side of this ```production```

        Returns:
            sequence
        """
        return self._lhs

    def rhs(self):
        """ Return the right hand side of this ```production```

        Returns:
            sequence
        """
        return self._rhs

    def __str__(self):
        """ Return a representation of this ``Production``as a string
        """
        string = "%s -> " % self._lhs
        string += " ".join(el for el in self._rhs)
        return string

    def __repr__(self):
        """ Return a basic representation of this ``Production``as a string
        """
        return "%s" % self

    def __eq__(self, other):
        """
        Return True if this ``Production`` is equal to ``other``.
        """
        return (type(self) == type(other) and
                self._lhs == other._lhs and
                self._rhs == other._rhs)

    def __ne__(self, other):
        """ Return True if this ``Production``is not equal to ``other``
        """
        return not self == other


    @classmethod
    def _parse_production(cls, line):
        """ Parse a grammar rule, given as a string
            and returns a list of production
        """
        pos = 0
        line = line.strip()
        m = _NONTERMINAL_RE.match(line)
        # TODO: the strip() is not elegant, fix if possible
        lhs, pos = m.group().strip(), m.end()

        # Skip over the arrow
        m = _ARROW_RE.match(line, pos)
        pos = m.end()

        rhsides = [[]]

        while pos < len(line):
            # Terminal
            # print(line[pos:])
            if line[pos] in "\'\"":
                m = _TERMINAL_RE.match(line, pos)
                pos = m.end()
                # TODO: the strip() is not elegant, fix if possible
                rhsides[-1].append(m.group().strip())
            # Vertical bar - start new rhside
            elif line[pos] == '|':
                m = _DISJUNCTION_RE.match(line, pos)
                rhsides.append([])
                pos = m.end()
            # Non-terminal
            else:
                m = _NONTERMINAL_RE.match(line, pos)
                # print(line[pos:])
                pos = m.end()
                # TODO: the strip() is not elegant, fix if possible
                rhsides[-1].append(m.group().strip())
        return [Production(lhs, rhs) for rhs in rhsides]

class Grammar(object):
    """ A simple context-free grammar
    """

    def __init__(self, productions=None):
        """ Create a new grammar

            Args:
                productions: the list of productions for the grammar as a
                list(Production)
        """
        self._productions = productions

    def productions(self):
        """ Returns the productions for this grammar as a ``list``
        """
        return self._productions

    @classmethod
    def parse_grammar(cls, input):
        """ Read a grammar given as a string
        Args:
            input as a string
        Returns:
            list of `productions`
        Raises:
            TypeError if input is not a string
        """
        assert isinstance(input, str)
        lines = input.split('\n')
        productions = []
        for linenum, line in enumerate(lines):
            line = line.strip()
            if line.startswith("#") or line=="": continue
            try:
                productions += Production._parse_production(line)
            except ValueError:
                raise ValueError("Parse error on line %s: %s" % (linenum,
                                                                 line))
        return productions

###############
### Helpers ###
###############

_NONTERMINAL_RE = re.compile(r'([\w][\w]*) \s*', re.VERBOSE)
_ARROW_RE = re.compile(r'\s* -> \s*', re.VERBOSE)
_DISJUNCTION_RE = re.compile(r'\| \s*', re.VERBOSE)
_TERMINAL_RE = re.compile(r'(\'\w+\') \s*', re.VERBOSE)
