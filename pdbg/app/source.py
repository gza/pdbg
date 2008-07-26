# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Represent source text and its breakpoints."""

__version__ = "$Id$"

from copy import copy

class Source(object):

    def __init__(self, text):
        self._text = text
        self._breakpoints = set()

    def add_breakpoint(self, line_num):
        """Add a breakpoint to the source file.

        No change is made if the breakpoint was previously set.
        """
        line_num = int(line_num)
        self._breakpoints.add(line_num)

    def remove_breakpoint(self, line_num):
        """Remove a breakpoint from a specified line (if present)."""
        self._breakpoints.discard(line_num)

    def get_breakpoints(self):
        """Return a copy of the breakpoints set on the file."""
        return copy(self._breakpoints)

    def has_breakpoint(self, line_num):
        """Return True if a breakpoint exists on the specified line."""
        return int(line_num) in self._breakpoints

    @property
    def text(self):
        """Return the source text."""
        return self._text
