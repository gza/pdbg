# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import readline
import logging
import time
from pdbg.app.patterns import Singleton
from pdbg.app.config import Config
from pdbg.dbgp.connectionlistener import ConnectionListener
from pdbg.dbgp.connection import ConnectionClosed
from pdbg.cli.command import factory as command_factory
from pdbg.cli.command import QuitCommandException, CloseCommandException, \
    CommandParserException
from pdbg.cli.connectionmanager import ConnectionManager
from pdbg.cli.sessionmanager import SessionManager

def remove_last_history_item():
    num_items = readline.get_current_history_length()
    if num_items > 0:
        readline.remove_history_item(num_items-1)

class AppException(Exception):
    pass

class App(Singleton):

    def __init__(self):
        super(App, self).__init__()

    def _setup(self):
        config = Config.get_instance()

        logging.basicConfig(
            level=config['logging_level'], 
            format='%(asctime)s %(levelname)s %(message)s')

        readline.parse_and_bind('tab: complete')

    def _run_debug_session(self, conn):
        conn_mgr = ConnectionManager.get_instance()
        conn_mgr.set_connection(conn)

        init = conn_mgr.wait_for_response()
        engine_info = init.get_engine_info()

        print("")
        print("Got connection.")

        if engine_info.has_key('engine'):
            engine_str = engine_info['engine']
            if engine_info.has_key('engine_version'):
                engine_str += ' ' + engine_info['engine_version']
            print("Remote engine is: " + engine_str)

        session = SessionManager.get_instance()
        session.reset()

        status_resp = conn_mgr.send_command('status')
        session['status'] = status_resp.status

        if session['status'] == 'break':
            (session['file_uri'], session['line_num']) = conn_mgr.get_position()

        print("Debugging script at uri: " + init.file_uri)
        print("Type help for more information, or quit to exit the program.")

        prev_cmd_line = None

        while True:
            cmd_line = raw_input('>>> ').strip()
            if cmd_line == '' and prev_cmd_line != None:
                cmd_line = prev_cmd_line
            elif cmd_line == '':
                continue

            try:
                command = command_factory(cmd_line)
                command.execute()
            except CommandParserException, e:
                remove_last_history_item()
                print("Invalid command string: %s" % cmd_line)
            except ConnectionClosed, e:
                print("Connection was closed remotely.")
                return 
            except CloseCommandException, e:
                return
            else:
                # if the command line was valid, save it so the user can avoid
                # typing it again.
                prev_cmd_line = cmd_line

    def run(self):
        self._setup()

        print("pDBG Command Line - v0.1")
        print("Welcome! Waiting for connection on 127.0.0.1:9000 ...")

        listener = ConnectionListener()

        try:
            while True:
                conn = listener.accept()
                if conn == None:
                    time.sleep(0.1)
                    continue
                self._run_debug_session(conn)
                print("")
                print("Waiting for connection ...")
        except QuitCommandException, e:
            pass
