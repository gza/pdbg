# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the source module."""

__version__ = "$Id$"

import unittest
from source import *

class TestSourceClass(unittest.TestCase):
    """Test the Source class."""

    def setUp(self):
        self._source = Source('foo')

    def test_get_text(self):
        self.assertEquals(self._source.text, 'foo')

    def test_add_breakpoint(self):
        self._source.add_breakpoint('1')
        self._source.add_breakpoint(1)
        self.assertEquals(self._source.get_breakpoints(), set((1,)))

    def test_has_breakpoint(self):
        self._source.add_breakpoint(1)
        self.assertEquals(self._source.has_breakpoint(1), True)
        self.assertEquals(self._source.has_breakpoint(2), False)
        self.assertEquals(self._source.has_breakpoint('1'), True)

    def test_remove_breakpoint(self):
        self._source.add_breakpoint(1)
        self._source.add_breakpoint(2)
        self.assertEquals(self._source.get_breakpoints(), set((1, 2)))
        self._source.remove_breakpoint(1)
        self.assertEquals(self._source.get_breakpoints(), set((2,)))

    def test_get_breakpoints(self):
        self._source.add_breakpoint(1)
        breakpoints = self._source.get_breakpoints()
        breakpoints.add(2)
        self.assertEquals(self._source.get_breakpoints(), set((1,)))

if __name__ == '__main__':
    unittest.main()
