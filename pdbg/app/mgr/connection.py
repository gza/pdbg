# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: Document"""

__version__ = "$Id$"

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

(
    STATUS_AWAITING_INIT,
    STATUS_READY,
    STATUS_STOPPED,
) = range(3)

def _trans_id_condition(id):
    def condition(conn_mgr, resp):
        return hasattr(resp, 'transaction_id') and resp.transaction_id == id
    return condition

def _aggregrate_func(*funcs):
    def aggregate_func(*arguments, **keywords):
        for func in funcs:
            if func: func(*arguments, **keywords)
    return aggregate_func

class ConnectionManagerException(Exception):
    pass

class ConnectionManager(Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self._state = STATUS_AWAITING_INIT
        self._num_unresponded = 1
        self._type_map = []
        self.register_event(*_event_names)

    def _change_state(self, state):
        self.fire('state_changed', self._state)
        self._state = state

    @property
    def connection(self):
        return self._connection

    @property
    def can_interact(self):
        return self._num_unresponded == 0 and self._state == STATUS_READY

    def setup(self, connection):
        self._connection = connection

    def close_connection(self):
        self.connection.close()

    def get_type_display_names(self, filter=None):
        names = {}
        for type in self._type_map:
            names[type.name] = type.name.capitalize()
        return names

    def send_command(self, command_str, arguments=[], data=None, \
        observer=None):
        could_interact = self.can_interact
        command = self.connection.send_command(command_str, arguments, data)
        self._num_unresponded += 1
        if observer != None:
            condition = _trans_id_condition(command.transaction_id)
            self.add_observer('response_handled', observer, condition, True)
        self.fire('command_sent', command)
        if could_interact and not self.can_interact:
            self.fire('can_interact', False)

    def send_status(self, observer=None):
        observer = _aggregrate_func(self._on_status_response, observer)
        self.send_command('status', observer=observer)

    def send_typemap_get(self, observer=None):
        observer = _aggregrate_func(self._on_typemap_get, observer)
        self.send_command('typemap_get', observer=observer)

    def send_continuation(self, name, observer=None):
        if name not in ('run','detach','step_into','step_over','step_out'):
            raise ConnectionManagerException, "%s is not a continuation command" % (name,)
        observer = _aggregrate_func(self._on_status_response, observer)
        self.send_command(name, observer=observer)

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

    def send_property_get(self, full_name, depth='0', context='0', observer=None):
        args = { '-n': full_name, '-d': depth, '-c': context }
        self.send_command('property_get', args, observer=observer)

    def send_property_set(self, full_name, depth='0', context='0', type=None, value=None, observer=None):
        args = { '-n': full_name, '-d': depth, '-c': context }
        if type != None:
            args['-t'] = type
        self.send_command('property_set', args, data=value, observer=observer)

    def process_response(self):
        response = self._connection.recv_response()
        if response != None:
            if type(response) == StreamResponse:
                self.fire('stream_response_received', response)
                return
            elif type(response) == InitResponse:
                remote_address = self.connection.socket.handle.getpeername()
                self.fire('init_packet', response, remote_address)
                self._status = STATUS_READY
            self._num_unresponded -= 1
            self.fire('response_received', response)
            self.fire('response_handled', response)
            # if can_interact is True here, then it must have changed as a 
            # result of this call to process_response.
            if self.can_interact:
                self.fire('can_interact', True)

    def _on_status_response(self, mgr, response):
        if not isinstance(response, StatusResponse):
            self._change_state(STATUS_STOPPED)
            # TODO: log something ...
            return
        status = response.status
        if status == 'starting' or status == 'break':
            self._change_state(STATUS_READY)
        else:
            if status == 'stopping' or status == 'stopped':
                self.close_connection()
                self._change_state(STATUS_STOPPED)
            elif status == 'running':
                raise ConnectionManagerException, "Async is currently not supported."

    def _on_typemap_get(self, mgr, response):
        if isinstance(response, TypemapGetResponse):
            self._type_map = response.get_type_map()
