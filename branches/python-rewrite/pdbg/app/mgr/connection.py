# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: Document"""

__version__ = "$Id$"

import inspect
from pdbg.app.patterns import Manager, Singleton
from pdbg.dbgp.socketwrapper import SocketWrapper
from pdbg.dbgp.connectionlistener import ConnectionListener
from pdbg.dbgp.idecommand import *
from pdbg.dbgp.engineresponse import *

_event_names = [
    'command_sent',
    'response_received',
    'init_packet',
    'init_source',
    'init_status'
]

def expected_response(type):
    def decorator(fn):
        def check_type(*arguments, **keywords):
            if not isinstance(arguments[2], type):
                raise TypeError, "Expected %s" % (type.__name__,)
            return fn(*arguments, **keywords)
        return check_type
    return decorator

class AwaitingInitState(object):

    @classmethod
    @expected_response(InitResponse)
    def run(klass, mgr, init):
        remote_address = mgr.connection.socket.handle.getpeername()
        mgr.fire('init_packet', init, remote_address)
        mgr.send_command('source', { '-f': init.file_uri })
        return AwaitingInitSourceState

class AwaitingInitSourceState(object):

    @classmethod
    @expected_response(SourceResponse)
    def run(klass, mgr, response):
        mgr.fire('init_source', response)
        mgr.send_command('status')
        return AwaitingInitStatusState

class AwaitingInitStatusState(object):

    @classmethod
    @expected_response(StatusResponse)
    def run(klass, mgr, response):
        mgr.fire('init_status', response)
        return None

class ConnectionManager(Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self._state = AwaitingInitState
        self.register_event(*_event_names)

    @property
    def connection(self):
        return self._connection

    def setup(self, connection):
        self._connection = connection

    def send_command(self, command_str, arguments=[], data=None):
        command = self.connection.send_command(command_str, arguments, data)
        self.fire('command_sent', command)

    def process_response(self):
        response = self._connection.recv_response()
        if response != None:
            self.fire('response_received', response)
            new_state = self._state.run(self, response)
            if new_state != None:
                self._state = new_state
