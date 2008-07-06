# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the connectionlistener module."""

__version__ = "$Id$"

import unittest
import socket
from connection import *
from connectionlistener import *

class DummyWrapper:
    def __init__(self, s):
        self.s = s

class TestConnectionListenerClass(unittest.TestCase):
    """Test the ConnectionListener class."""

    def test_none_pending(self):
        l = ConnectionListener(DummyWrapper)
        self.assertEqual(l.accept(), None)
        l.socket.close()

    def test_pending(self):
        l = ConnectionListener(DummyWrapper)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9000))
        c = l.accept()
        self.assertEqual(isinstance(c, Connection), True)
        self.assertEqual(isinstance(c.socket, DummyWrapper), True)
        l.socket.close()

if __name__ == '__main__':
    unittest.main()
