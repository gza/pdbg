# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

from pdbg.cli.sessionmanager import SessionManager
from pdbg.cli.connectionmanager import ConnectionManager
from pdbg.cli.pretty import *

class Command(object):

    def __init__(self, name, args):
        self._name = name
        self._args = args

    @classmethod
    def get_names(klass):
        return ()

    def _get_arg(self, pos, default=None):
        if pos < len(self._args):
            return self._args[pos]
        else:
            return default

    def _get_int_arg(self, pos, default=None):
        arg = self._get_arg(pos, default)
        return int(arg)

    def reset(self):
        pass

    def execute(self):
        pass

class NopCommand(Command):

    @classmethod
    def get_names(self):
        return ('nop',)

    def execute(self):
        print("Did nothing successfully.")

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

        session['status'] = status_resp.status

        if session['status'] in ('stopping', 'stopped'):
            session['line_num'] = None
            session['file_uri'] = None
            print("Engine stopped normally.")
            return

        (file_uri, line_num) = conn_mgr.get_position()

        source_resp = conn_mgr.send_command('source',
            { '-f': file_uri, '-b': line_num, '-e': line_num })

        session['file_uri'] = file_uri
        session['line_num'] = line_num
        
        print(file_uri)
        print(format_lines(source_resp.source, line_num))

class ViewCommand(Command):

    @classmethod
    def get_names(self):
        return (
            ('view', 'v'),
            ('viewall', 'va'),
        )

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        if not session.can_continue():
            print("Engine stopped. View command not allowed.")
            return
        elif session['file_uri'] == None:
            return

        if self._name == 'view':
            lines_around = max(1, self._get_int_arg(0, 3))
            begin = max(1, session['line_num'] - lines_around)
            end = session['line_num'] + lines_around
            args = { '-f': session['file_uri'], '-b': begin, '-e': end }
        else:
            begin = 1
            args = { '-f': session['file_uri'] }

        source_resp = conn_mgr.send_command('source', args)

        print(session['file_uri'])
        print(format_lines(source_resp.source, begin, session['line_num']))

class TraceCommand(Command):

    @classmethod
    def get_names(self):
        return (('trace', 't'),)

    def execute(self):
        session = SessionManager.get_instance()
        conn_mgr = ConnectionManager.get_instance()

        if session['file_uri'] == None:
            return

        stack_resp = conn_mgr.send_command('stack_get')
        elems = stack_resp.get_stack_elements()
        print(format_trace(elems))

_commands = (
    NopCommand,
    QuitCommand,
    CloseCommand,
    StepCommand,
    ViewCommand,
    TraceCommand
)

class CommandParserException(Exception):
    pass

def factory(cmd_line):
    parts = cmd_line.split(' ')
    if parts == 0:
        raise CommandParserException("Not enough parts")
    supplied_name = parts[0].lower()
    for command_class in _commands:
        names = command_class.get_names()
        for name in names:
            if isinstance(name, tuple) and supplied_name in name:
                return command_class(name[0], parts[1:])
            elif supplied_name == name:
                return command_class(name, parts[1:])
    raise CommandParserException("Unknown Command")
