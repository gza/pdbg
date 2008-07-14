# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the idecommand module."""

__version__ = "$Id$"

import unittest
import idecommand

class TestIdeCommandClass(unittest.TestCase):
    """Test the IdeCommand class."""

    def test_has_arg(self):
        c = idecommand.IdeCommand('status', (('-a', 5),))
        self.assertEqual(c.has_argument('-i'), True)
        self.assertEqual(c.has_argument('-foo'), False)

    def test_get_arg(self):
        c = idecommand.IdeCommand('status', (('-a', 'x'),))
        self.assertEqual('x', c.get_argument('-a'))

    def test_get_missing_arg(self):
        c = idecommand.IdeCommand('status')
        try:
            c.get_argument('-foo')
        except LookupError:
            return
        self.fail("LookupError expected")

    def test_build_name(self):
        c = idecommand.IdeCommand('status')
        self.assertEqual(c.build(), "status -i 1\x00")
    
    def test_build_name_args(self):
        c = idecommand.IdeCommand('status', (('-a', 1), ('-b', 'foo')))
        self.assertEqual(c.build(), "status -a 1 -b foo -i 2\x00")

    def test_build_name_args_data(self):
        c = idecommand.IdeCommand('status', (('-a', 1),), 'foo')
        self.assertEqual(c.build(), "status -a 1 -i 3 -- Zm9v\x00")

    def test_build_no_null(self):
        c = idecommand.IdeCommand('status')
        self.assertEqual(c.build(False), "status -i 4")

    def test_specify_trans_id(self):
        c = idecommand.IdeCommand('zzz', {'-i': 1000})
        self.assertEqual(c.transaction_id, 1000)
        self.assertEqual(c.build(False), "zzz -i 1000")

    def test_str(self):
        c = idecommand.IdeCommand('zzz', {'-i': 1000})
        self.assertEqual(str(c), 'zzz -i 1000')

class TestModuleFunctions(unittest.TestCase):
    """Test the module functions."""

    def test_build_func(self):
        args = (('-i', 20), ('-a', 'foo'))
        cmd_str = idecommand.build('qq', args, 'foo', False)
        self.assertEqual(cmd_str, "qq -i 20 -a foo -- Zm9v")

if __name__ == '__main__':
    unittest.main()
