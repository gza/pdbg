# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Represent source text and its breakpoints."""

__version__ = "$Id$"

from copy import copy, deepcopy

class Source(object):

    def __init__(self, file_uri, text):
        self._file_uri = file_uri
        self._text = text
        self._breakpoints = {}

    def add_breakpoint(self, line_num, id, type):
        """Add a breakpoint to the source file."""
        id = str(id)
        breakpoint = { 
            'line_num': int(line_num),
            'id': id,
            'type': str(type)
        }
        self._breakpoints[id] = breakpoint

    def remove_breakpoint(self, id):
        """Remove a breakpoint of the specified id (if present)."""
        id = str(id)
        if self._breakpoints.has_key(id):
            del self._breakpoints[id]

    def get_breakpoints(self):
        """Return a copy of the breakpoints set on the file."""
        return deepcopy(self._breakpoints)

    def has_breakpoint(self, id):
        """Return True if a breakpoint of the specified id is set."""
        return self._breakpoints.has_key(str(id))

    def get_breakpoints_on_line(self, line_num):
        """Return all breakpoints on a specified line."""
        line_num = int(line_num)
        result = []
        for id in self._breakpoints:
            breakpoint = self._breakpoints[id]
            if breakpoint['line_num'] == line_num:
                result.append(copy(breakpoint))
        return result

    @property
    def text(self):
        """Return the source text."""
        return self._text

    @property
    def file_uri(self):
        """Return the source file uri."""
        return self._file_uri
