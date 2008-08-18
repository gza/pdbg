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
    'stream_response_received',
    'response_handled',
    'init_packet',
    'can_interact',
)

def expected_response(type):
    def decorator(fn):
        def check_type(*arguments, **keywords):
            if not isinstance(arguments[2], type):
                raise TypeError, "Expected %s" % (type.__name__,)
            return fn(*arguments, **keywords)
        return check_type
    return decorator

def _trans_id_condition(id):
    def condition(conn_mgr, resp):
        return hasattr(resp, 'transaction_id') and resp.transaction_id == id
    return condition

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
        return Ready

class Ready(ConnectionState):

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
        if status == 'starting' or status == 'break':
            return Ready
        else:
            if status == 'stopping' or status == 'stopped':
                mgr.close_connection()
                return Stopped
            elif status == 'running':
                raise ConnectionManagerException, "Async is currently not supported."

class ConnectionManagerException(Exception):
    pass

class ConnectionManager(Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self._state = AwaitingInit
        self._num_unresponded = 1
        self.register_event(*_event_names)

    def _change_state(self, state):
        self.fire('state_changed', self._state.get_name(), state.get_name())
        self._state = state

    @property
    def connection(self):
        return self._connection

    @property
    def can_interact(self):
        return self._num_unresponded == 0 and self._state == Ready

    def setup(self, connection):
        self._connection = connection

    def close_connection(self):
        self.connection.close()

    def send_command(self, command_str, arguments=[], data=None, \
        change_to=None, observer=None):
        could_interact = self.can_interact
        command = self.connection.send_command(command_str, arguments, data)
        self._num_unresponded += 1
        if observer != None:
            condition = _trans_id_condition(command.transaction_id)
            self.add_observer('response_handled', observer, condition, True)
        self.fire('command_sent', command)
        if change_to != None:
            self._change_state(change_to)
        if could_interact and not self.can_interact:
            self.fire('can_interact', False)

    def send_status(self, observer=None):
        self.send_command('status', change_to=AwaitingStatus, observer=observer)

    def send_continuation(self, name, observer=None):
        if name not in ('run','detach','step_into','step_over','step_out'):
            raise ConnectionManagerException, "%s is not a continuation command" % (name,)
        self.send_command(name, change_to=AwaitingStatus, observer=observer)

    def send_stack_get(self, observer=None):
        self.send_command('stack_get', observer=observer)

    def send_source(self, file_uri, observer=None):
        self.send_command('source', { '-f': file_uri }, observer=observer)

    def send_line_breakpoint_set(self, file_uri, line_num, observer=None):
        self.send_command('breakpoint_set', \
            { '-t': 'line', '-f': file_uri, '-n': line_num }, observer=observer)

    def send_breakpoint_remove(self, breakpoint_id, observer=None):
        self.send_command('breakpoint_remove', \
            { '-d': breakpoint_id }, observer=observer)

    def send_stdout(self, redirect_type='2', observer=None):
        redirect_type = str(redirect_type)
        if redirect_type not in ('0', '1', '2'):
            raise ConnectionManagerException, "%s is not a redirection type." \
                % (redirect_type,)
        self.send_command('stdout', { '-c': redirect_type }, observer=observer)

    def send_stderr(self, redirect_type='2', observer=None):
        redirect_type = str(redirect_type)
        if redirect_type not in ('0', '1', '2'):
            raise ConnectionManagerException, "%s is not a redirection type." \
                % (redirect_type,)
        self.send_command('stderr', { '-c': redirect_type }, observer=observer)

    def send_context_names(self, depth='0', observer=None):
        self.send_command('context_names', { '-d': depth }, observer=observer)

    def send_context_get(self, context_id='0', depth='0', observer=None):
        self.send_command('context_get', { '-d': depth, '-c': context_id }, 
            observer=observer)

    def send_property_set(self, full_name, depth='0', type=None, value=None, observer=None):
        args = { '-n': full_name, '-d': depth }
        if type != None:
            args['-t'] = type
        self.send_command('property_set', args, data=value, observer=observer)

    def process_response(self):
        response = self._connection.recv_response()
        if response != None:
            if type(response) == StreamResponse:
                self.fire('stream_response_received', response)
                return
            self._num_unresponded -= 1
            self.fire('response_received', response)
            new_state = self._state.run(self, response)
            if new_state != None:
                self._change_state(new_state)
            self.fire('response_handled', response)
            # if can_interact is True here, then it must have changed as a 
            # result of this call to process_response.
            if self.can_interact:
                self.fire('can_interact', True)
