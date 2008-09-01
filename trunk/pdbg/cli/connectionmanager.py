# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import time
from pdbg.app.patterns import *
from pdbg.dbgp.connection import *

class ConnectionManager(Singleton):

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self._conn = None

    def set_connection(self, conn):
        self._conn = conn

    def wait_for_response(self):
        return self._conn.recv_response_blocking()

    def send_command(self, command, arguments=[], data=None):
        cmd  = self._conn.send_command(command, arguments, data)
        resp = self.wait_for_response()
        if not resp.successful:
            raise ConnectionManagerException(
                "command %s not successful: %s" % (cmd.name, resp.error_msg))
        return resp

    def get_position(self):
        resp = self.send_command('stack_get', {'-d': '0'})
        if not resp.successful:
            return None
        stack = resp.get_stack_elements()
        return (stack[0]['filename'], stack[0]['lineno'])

    def close(self):
        self._conn.close()
