# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the source module."""

__version__ = "$Id$"

import unittest
from source import *

class TestSourceClass(unittest.TestCase):
    """Test the Source class."""

    def setUp(self):
        self._source = Source('file:///foo/bar.php', 'foo')

    def test_get_file_uri(self):
        self.assertEquals(self._source.file_uri, 'file:///foo/bar.php')

    def test_get_text(self):
        self.assertEquals(self._source.text, 'foo')

    def test_add_breakpoint(self):
        self._source.add_breakpoint('1', 'f10', 'line')
        self.assertEquals(self._source.get_breakpoints(), \
            {'f10': {'line_num': 1, 'id': 'f10', 'type': 'line'}})

    def test_has_breakpoint(self):
        self._source.add_breakpoint('1', 'f10', 'line')
        self.assertEquals(self._source.has_breakpoint('f10'), True)
        self.assertEquals(self._source.has_breakpoint('f11'), False)

    def test_get_breakpoints_on_line(self):
        self._source.add_breakpoint('1', 'f10', 'line')
        self._source.add_breakpoint('2', 'f11', 'line')
        breakpoints = self._source.get_breakpoints_on_line(2)
        self.assertEquals(len(breakpoints), 1)
        self.assertEquals(breakpoints[0], \
            {'line_num': 2, 'id': 'f11', 'type': 'line'})

    def test_remove_breakpoint(self):
        self._source.add_breakpoint('1', 'f10', 'line')
        self._source.add_breakpoint('2', 'f11', 'line')
        self.assertEquals(self._source.has_breakpoint('f10'), True)
        self.assertEquals(self._source.has_breakpoint('f11'), True)
        self._source.remove_breakpoint('f11')
        self.assertEquals(self._source.has_breakpoint('f10'), True)
        self.assertEquals(self._source.has_breakpoint('f11'), False)

    def test_current_line(self):
        self._source.current_line = 1
        self.assertEquals(self._source.current_line, 1)
        self._source.current_line = '2'
        self.assertEquals(self._source.current_line, 2)
        self._source.current_line = None
        self.assertEquals(self._source.current_line, None)

if __name__ == '__main__':
    unittest.main()
