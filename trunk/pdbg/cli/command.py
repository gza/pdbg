# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import re
from pdbg.cli.sessionmanager import SessionManager
from pdbg.cli.connectionmanager import ConnectionManager, \
    ConnectionManagerException
from pdbg.cli.pretty import *

def _to_int(str, default=None):
    try:
        return int(str)
    except ValueError, str:
        return default

class CommandArguments(list):

    def __init__(self, arg_str):
        super(CommandArguments, self).__init__()
        self._arg_str = arg_str
        self[:] = arg_str.split(' ')
        if self[0] == '':
            del self[0]

    def get(self, pos, default=None):
        if pos < len(self):
            return self[pos]
        else:
            return default

    def get_int(self, pos, default=None):
        return _to_int(self.get(pos, default), default)

    def get_payload(self, pos):
        parts = self._arg_str.split(' ', pos)
        if len(parts) >= pos+1:
            return parts[pos]
        else:
            return ''

class Command(object):

    def __init__(self, name):
        self._name = name

    @classmethod
    def get_names(klass):
        return ()

    def set_args(self, args):
        return True

    def reset(self):
        pass

    def execute(self):
        pass

class QuitCommandException(Exception):
    pass

class QuitCommand(Command):

    @classmethod
    def get_names(self):
        return ('quit',)

    def execute(self):
        print("Goodbye!")
        raise QuitCommandException()

class CloseCommandException(Exception):
    pass

class CloseCommand(Command):

    @classmethod
    def get_names(self):
        return ('close',)

    def execute(self):
        ConnectionManager.get_instance().close()
        raise CloseCommandException()

class BaseCommand(Command):

    @classmethod
    def get_names(self):
        return (('base',))

    def set_args(self, args):
        self._base = args.get(0, None)
        return True

    def execute(self):
        session = SessionManager.get_instance()
        if self._base == None:
            session['base_uri'] = re.sub('[^/]+$', '', session['file_uri'])
        else:
            session['base_uri'] = self._base
        print("Base URI set to " + session['base_uri'])

class QueueCommand(Command):

    @classmethod
    def get_names(self):
        return (('queue', 'q'),)

    def set_args(self, args):
        self._text = args.get_payload(0)
        return True

    def execute(self):
        session = SessionManager.get_instance()
        session['queue'].append(self._text)

class StepCommand(Command):

    @classmethod
    def get_names(self):
        return (
            ('run', 'r'),
            ('step_into', 'step', 's'), 
            ('step_over', 'over', 'ov'),
            ('step_out', 'out', 'ot'),
            ('detach',)
        )

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        if not session.can_continue():
            print("Engine stopped. Continuation commands not allowed.")
            return

        step_resp = conn_mgr.send_command(self._name)
        status_resp = conn_mgr.send_command('status')

        session['list_b'] = None
        session['list_e'] = None

        session['status'] = status_resp.status
        session['reason'] = status_resp.reason

        if session['status'] in ('stopping', 'stopped'):
            session['line_num'] = None
            session['file_uri'] = None
            print("Engine stopped normally.")
            return

        # on a run command tell the user what happened.
        if self._name == 'run':
            if session['reason'] == 'ok':
                print("Hit breakpoint. Execution halted.")
            elif session['reason'] == 'error':
                print("Hit error. Execution halted.")
            elif session['reason'] == 'aborted':
                print("Engine aborted. Execution halted.")
            elif session['reason'] == 'exception':
                print("Exception occurred. Execution halted.")

        (file_uri, line_num) = conn_mgr.get_position()

        source_resp = conn_mgr.send_command('source',
            { '-f': file_uri, '-b': line_num, '-e': line_num })

        session['file_uri'] = file_uri
        session['line_num'] = line_num
        
        print(file_uri)
        print(format_lines(source_resp.source, line_num))

class ListCommand(Command):

    @classmethod
    def get_names(self):
        return (
            ('list', 'l'),
            ('list_all', 'la'),
        )

    def _set_around(self, line, list_size=None):
        if list_size == None:
            s = SessionManager.get_instance()
            list_size = s['list_size']
        self._begin = max(1, line - list_size // 2)
        self._end = line + list_size // 2 

    def _set_around_current(self):
        s = SessionManager.get_instance()
        self._set_around(s['line_num'])

    def _set_from_start(self):
        s = SessionManager.get_instance()
        self._begin = 1
        self._end = self._begin + s['list_size'] - 1

    def _set_from_begin(self):
        s = SessionManager.get_instance()
        self._end = s['list_b'] - 1
        self._begin = max(1, self._end - s['list_size'] - 1)

    def _set_from_end(self):
        s = SessionManager.get_instance()
        self._begin = s['list_e'] + 1
        self._end = self._begin + s['list_size'] - 1

    def set_args(self, args):
        session = SessionManager.get_instance()
        param = args.get(0)
        if param == None or param == '+':
            if session['list_e'] != None:
                self._set_from_end()
            elif session['line_num'] != None:
                self._set_around_current()
            else:
                self._set_from_start()
        elif param == '-':
            if session['list_b'] != None:
                self._set_from_begin()
            elif session['line_num'] != None:
                self._set_around_current()
            else:
                self._set_from_start()
        else:
            parts = param.split(':', 1)
            if len(parts) > 1:
                line   = _to_int(parts[0], session.get('line_num', 1))
                around = _to_int(parts[1], session['list_size'])
                self._set_around(line, around)
            else:
                line = _to_int(parts[0], session.get('line_num', 1))
                self._set_around(line)
        session['list_b'] = self._begin
        session['list_e'] = self._end
        return True

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        if not session.can_continue():
            print("Engine stopped. Cannot execute list command.")
            return

        if session['line_num'] != None:
            highlight = session['line_num']
        else:
            highlight = None

        if self._name == 'list':
            num_start = self._begin
            args = { '-f': session['file_uri'], '-b': self._begin, '-e': self._end }
        else:
            num_start = 1
            args = { '-f': session['file_uri'] }

        try:
            source_resp = conn_mgr.send_command('source', args)
        except ConnectionManagerException, e:
            session['list_b'] = None
            session['list_e'] = None
            print("Could not fetch source.")
            return

        print(session['file_uri'])
        print(format_lines(source_resp.source, num_start, highlight))

class TraceCommand(Command):

    @classmethod
    def get_names(self):
        return (('back_trace', 'bt'),)

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        if session['status'] != 'break':
            print("Backtrace not allowed. The engine is not stopped on a line.")
            return

        stack_resp = conn_mgr.send_command('stack_get')
        elems = stack_resp.get_stack_elements()
        print(format_trace(elems))

class BreakpointCommand(Command):

    @classmethod
    def get_names(self):
        return (('break', 'b'),)

    def set_args(self, args):
        if len(args) < 1:
            return False
        self._line_num = args.get_int(0)
        if self._line_num == None:
            return False
        self._file_uri = args.get(1, None)
        return True

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        if self._file_uri == None:
            file_uri = session['file_uri']
        else:
            file_uri = session.append_base_uri(self._file_uri)

        args = {
            '-t': 'line', 
            '-f': file_uri,
            '-n': self._line_num
        }

        resp = conn_mgr.send_command('breakpoint_set', args)

        print("Breakpoint %s set on line %s of %s" % \
            (resp.id, self._line_num, file_uri))

class BreakCallCommand(Command):

    @classmethod
    def get_names(self):
        return (('break_call',),)

    def set_args(self, args):
        func = args.get(0)
        if func == '':
            return False
        parts = func.split('::', 1)
        if len(parts) > 1:
            self._class = parts[0]
            self._func  = parts[1]
        else:
            self._class = None
            self._func  = parts[0]
        return True

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        args = {
            '-t': 'call', 
            '-m': self._func
        }

        if self._class != None:
            args['-a'] = self._class

        resp = conn_mgr.send_command('breakpoint_set', args)

        print("Breakpoint %s set on %s" % (resp.id, self._func))

class GetCommand(Command):

    @classmethod
    def get_names(self):
        return (
            ('get', 'g'),
            ('var_info', 'i'),
        )

    def set_args(self, args):
        self._long_name = args.get_payload(0)
        if self._long_name == '':
            return False
        return True

    def execute(self):
        conn_mgr = ConnectionManager.get_instance()

        try:
            get_resp = conn_mgr.send_command('property_get',
                { '-n': self._long_name })
            prop = get_resp.get_property()
            if prop != None:
                if self._name == 'get':
                    print(format_value(prop))
                else:
                    print(format_property(prop))
        except ConnectionManagerException, e:
            print("Get failed: %s" % (e.message))

class SetCommand(Command):

    @classmethod
    def get_names(self):
        return (
            ('set_str', 'ss'),
            ('set_int', 'si'),
            ('set_bool', 'sb'),
            ('set_float', 'sf'),
        )

    def set_args(self, args):
        self._long_name = args.get_payload(0)
        if self._long_name == '':
            return False
        return True

    def execute(self):
        conn_mgr = ConnectionManager.get_instance()
        session = SessionManager.get_instance()

        value = session.input('enter value: ')

        if self._name == 'set_str':
            var_type = 'string'
        elif self._name == 'set_int':
            var_type = 'int'
        elif self._name == 'set_bool':
            var_type = 'bool'
            if value == 'true':
                value = '1'
            else:
                value = '0'
        elif self._name == 'set_float':
            var_type = 'float'

        try:
            set_resp = conn_mgr.send_command('property_set',
                {'-n': self._long_name, '-t': var_type}, value)
        except ConnectionManagerException, e:
            print("Set failed: %s" % e.message)

_commands = []

for (name, gbl) in globals().items():
    if isinstance(gbl, type) and re.match('.+Command$', name):
        _commands.append(gbl)

class CommandParserException(Exception):
    pass

def factory(cmd_line):
    parts = cmd_line.split(' ', 1)
    if len(parts) > 1:
        arg_str = parts[1]
    else:
        arg_str = ''
    supplied_name = parts[0].lower()
    for command_class in _commands:
        names = command_class.get_names()
        for name in names:
            if isinstance(name, tuple) and supplied_name in name:
                c = command_class(name[0])
            elif supplied_name == name:
                c = command_class(name)
            else:
                continue
            if not c.set_args(CommandArguments(arg_str)):
                raise CommandParserException("Arguments invalid")
            return c
    raise CommandParserException("Unknown Command")
