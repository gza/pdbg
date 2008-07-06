# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the connection module."""

__version__ = "$Id$"

import unittest
from StringIO import StringIO
from idecommand import *
from engineresponse import *
from connection import *

_status_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="status" 
          transaction_id="1" 
          status="starting" 
          reason="ok"/>
"""
_status_response_str = str(len(_status_response_xml)) + "\x00" + \
    _status_response_xml + "\x00"

class MockSocketWrapper:
    def __init__(self, io):
        self.io = io
        self.eof = False

    def send_all(self, data):
        self.io.write(data)

    def recv(self, size):
        r = self.io.read(size)
        return r

    def is_data_available(self):
        return self.io.tell() < len(self.io.getvalue())

class MockSocketWrapperClosed:
    def recv(self, size):
        return ''

    def is_data_available(self):
        return True

class TestConnectionClass(unittest.TestCase):
    """Test the Connection class."""

    def test_write_command(self):
        c = Connection(MockSocketWrapper(StringIO()))
        c.send_command('status', {'-i': '5'}, 'foo')
        self.assertEqual(c.socket.io.getvalue(), "status -i 5 -- Zm9v\x00")

    def test_write_command_obj(self):
        o = IdeCommand('status', {'-i': '5'}, 'foo')
        c = Connection(MockSocketWrapper(StringIO()))
        c.send_command(o)
        self.assertEqual(c.socket.io.getvalue(), "status -i 5 -- Zm9v\x00")

    def test_recv_response(self):
        c = Connection(MockSocketWrapper(StringIO(_status_response_str)))
        self.assertEqual(c.recv_response().status, 'starting')
        self.assertEqual(c.recv_response(), None)

    def test_recv_response_twice(self):
        s = _status_response_str*2
        c = Connection(MockSocketWrapper(StringIO(s)))
        self.assertEqual(c.recv_response().status, 'starting')
        self.assertEqual(c.recv_response().status, 'starting')
        self.assertEqual(c.recv_response(), None)

    def test_recv_response_closed(self):
        c = Connection(MockSocketWrapperClosed())
        try:
            c.recv_response()
        except ConnectionClosed:
            return
        self.fail("ConnectionClosed expected")

if __name__ == '__main__':
    unittest.main()
