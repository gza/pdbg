# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: Document"""

__version__ = "$Id$"

import re
from pdbg.app.patterns import Manager, Singleton
from pdbg.dbgp.socketwrapper import SocketWrapper
from pdbg.dbgp.connectionlistener import ConnectionListener
from pdbg.dbgp.idecommand import *
from pdbg.dbgp.engineresponse import *

_event_names = (
    'state_changed',
    'command_sent',
    'response_received',
    'init_packet',
    'init_source',
    'init_status',
    'stack_update',
)

def expected_response(type):
    def decorator(fn):
        def check_type(*arguments, **keywords):
            if not isinstance(arguments[2], type):
                raise TypeError, "Expected %s" % (type.__name__,)
            return fn(*arguments, **keywords)
        return check_type
    return decorator

class ConnectionState(object):

    @classmethod
    def get_name(klass):
        underscore = lambda m: '_' + m.group(0).lower()
        return re.sub('[A-Z]', underscore, klass.__name__).lstrip('_')

class AwaitingInit(ConnectionState):

    @classmethod
    @expected_response(InitResponse)
    def run(klass, mgr, init):
        remote_address = mgr.connection.socket.handle.getpeername()
        mgr.fire('init_packet', init, remote_address)
        mgr.send_command_stateless('source', { '-f': init.file_uri })
        return AwaitingInitSource

class AwaitingInitSource(ConnectionState):

    @classmethod
    @expected_response(SourceResponse)
    def run(klass, mgr, response):
        mgr.fire('init_source', response)
        mgr.send_command_stateless('status')
        return AwaitingInitStatus

class AwaitingInitStatus(ConnectionState):

    @classmethod
    @expected_response(StatusResponse)
    def run(klass, mgr, response):
        mgr.fire('init_status', response)
        return CanInteract

class CanInteract(ConnectionState):

    @classmethod
    def run(klass, mgr, response):
        return None

class Stopped(ConnectionState):

    @classmethod
    def run(klass, mgr, response):
        return None

class AwaitingStatus(ConnectionState):

    @classmethod
    @expected_response(StatusResponse)
    def run(klass, mgr, response):
        status = response.status
        if status == 'break':
            mgr.send_command_stateless('stack_get')
            return AwaitingStackGetFollowup
        else:
            if status == 'stopping' or status == 'stopped':
                return Stopped
            elif status == 'running':
                raise ConnectionManagerException, "Async is currently not supported."

class AwaitingStackGetFollowup(ConnectionState):

    @classmethod
    @expected_response(StackGetResponse)
    def run(klass, mgr, response):
        stack = response.get_stack_elements()
        mgr.fire('stack_update', stack)
        return CanInteract

class CannotInteract(ConnectionState):

    @classmethod
    def run(klass, mgr, response):
        return CanInteract

class ConnectionManagerException(Exception):
    pass

class ConnectionManager(Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self._state = AwaitingInit
        self.register_event(*_event_names)

    def _change_state(self, state):
        self.fire('state_changed', self._state.get_name(), state.get_name())
        self._state = state

    @property
    def connection(self):
        return self._connection

    @property
    def can_interact(self):
        return self._state == CanInteract

    def setup(self, connection):
        self._connection = connection

    def send_command(self, command_str, arguments=[], data=None, \
        require=CanInteract, change_to=CannotInteract):
        if require != None and self._state != require:
            raise ConnectionManagerException, "cannot send command in current state"
        self.send_command_stateless(command_str, arguments, data)
        if change_to != None:
            self._change_state(change_to)

    def send_command_stateless(self, command_str, arguments=[], data=None):
        command = self.connection.send_command(command_str, arguments, data)
        self.fire('command_sent', command)

    def send_run(self):
        self.send_command('run', change_to=AwaitingStatus)

    def send_detach(self):
        self.send_command('detach', change_to=AwaitingStatus)

    def send_step_into(self):
        self.send_command('step_into', change_to=AwaitingStatus)

    def send_step_over(self):
        self.send_command('step_over', change_to=AwaitingStatus)

    def send_step_out(self):
        self.send_command('step_out', change_to=AwaitingStatus)

    def process_response(self):
        response = self._connection.recv_response()
        if response != None:
            self.fire('response_received', response)
            new_state = self._state.run(self, response)
            if new_state != None:
                self._change_state(new_state)
