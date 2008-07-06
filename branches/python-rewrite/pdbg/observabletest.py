# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the observable module."""

__version__ = "$Id$"

import unittest
from observable import *

def _new_inc_observer():
    def f(observable, amt=1):
        f.times += amt
    f.times = 0
    return f

class TestObservableClass(unittest.TestCase):
    """Test the Observable class."""

    def test_fire(self):
        f = _new_inc_observer()
        o = Observable()
        o.register_event('foo')
        o.add_observer('foo', f)
        self.assertEqual(f.times, 0)
        o.fire('foo')
        self.assertEqual(f.times, 1)
        o.fire('foo')
        self.assertEqual(f.times, 2)

    def test_two_observers(self):
        f = _new_inc_observer()
        o = Observable()
        o.register_event('foo')
        o.add_observer('foo', f).add_observer('foo', f)
        o.fire('foo')
        self.assertEqual(f.times, 2)

    def test_two_events(self):
        f = _new_inc_observer()
        o = Observable()
        o.register_event('foo', 'bar')
        o.add_observer(foo=f, bar=f)
        o.fire('foo').fire('bar')
        self.assertEqual(f.times, 2)

    def test_fire_param(self):
        f = _new_inc_observer()
        o = Observable()
        o.register_event('foo', 'bar')
        o.add_observer(foo=f, bar=f)
        o.fire('foo').fire('bar', 2)
        self.assertEqual(f.times, 3)

    def test_remove_observer(self):
        f1 = _new_inc_observer()
        f2 = _new_inc_observer()
        o = Observable()
        o.register_event('foo')
        o.add_observer('foo', f1).add_observer('foo', f2)
        self.assertEqual(o.remove_observer('foo', f2), True)
        o.fire('foo')
        self.assertEqual(f1.times, 1)
        self.assertEqual(f2.times, 0)

if __name__ == '__main__':
    unittest.main()
