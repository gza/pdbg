# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of a single ui tab page."""

__version__ = "$Id$"

import gobject
import gtk
from pdbg.app.patterns import Manager, bind_params
from pdbg.app.mgr.connection import ConnectionManager
from pdbg.app.config import Config
from pdbg.app.source import Source, SourceCache
from pdbg.dbgp.engineresponse import *
from pdbg.dbgp.connection import ConnectionClosed
from pdbg.gtk.view.app import AppView
from pdbg.gtk.view.page import PageView
from pdbg.gtk.view.changeproperty import ChangePropertyView

_NUM_INIT_STEPS = 5

class PageManager(Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self._source_cache = SourceCache()
        self._page_num = None
        self._init_steps_done = set()

    def setup(self, connection):
        """Setup the manager."""
        self._connection = connection
        self._conn_mgr = ConnectionManager()
        self._conn_mgr.setup(connection)

        self._conn_mgr.add_observer(
            command_sent=self.on_command,
            response_received=self.on_response,
            stream_response_received=self.on_stream_response,
            init_packet=self.on_init_packet)

        # Add a hook in the gobject main loop to monitor for incoming data
        # on the socket.
        gobject.io_add_watch(
            connection.socket.handle,
            gobject.IO_IN | gobject.IO_HUP | gobject.IO_ERR,
            self.on_io_event)

        self._view = PageView()

        self._view['tab_button'].connect(
            'clicked',
            self.on_tab_close_button_clicked)

        self._view['source_view'].connect(
            'button-press-event',
            self.on_button_press_on_source_view)

        self._view['source_list'].connect(
            'row-activated',
            self.on_source_list_row_activated)

        self._view['get_uri_button'].connect(
            'clicked',
            self.on_get_uri_button_clicked)

        self._view['uri_entry'].connect(
            'activate',
            self.on_get_uri_button_clicked)
        
        self._view['property_notebook'].connect(
            'property-clicked',
            self.on_property_clicked)

    @property
    def conn_mgr(self):
        return self._conn_mgr

    def send_continuation(self, command):
        self._conn_mgr.send_continuation(command, self.on_cont_status)

    def refresh_page_number(self):
        notebook = AppView.get_instance()['notebook']
        self._page_num = notebook.page_num(self._view['outer_box'])

    def _set_line_breakpoint(self, line_num):
        source = self._view['source_view'].current_source
        if not source:
            return
        breaks_on_line = source.get_breakpoints_on_line(line_num)
        if len(breaks_on_line) > 0:
            return
        callback = bind_params(self.on_breakpoint_set, source, line_num)
        self._conn_mgr.send_line_breakpoint_set(source.file_uri, 
            line_num + 1, callback)

    def _remove_line_breakpoint(self, line_num):
        source = self._view['source_view'].current_source
        if not source:
            return
        breaks_on_line = source.get_breakpoints_on_line(line_num)
        if len(breaks_on_line) == 0:
            return
        id = breaks_on_line[0]['id']
        callback = bind_params(self.on_breakpoint_remove, source, id)
        self._conn_mgr.send_breakpoint_remove(id, callback)

    def on_io_event(self, source, condition):
        # Called from the gobject main loop when an event occurs on the 
        # connection socket.
        if condition == gobject.IO_IN:
            try:
                self._conn_mgr.process_response()
            except ConnectionClosed, e:
                self._conn_mgr.close_connection()
                app_view = AppView.get_instance()
                app_view['notebook'].set_current_page(self._page_num)
                app_view.show_error('conn_closed')
                app_view['notebook'].remove_page(self._page_num)
        elif condition == gobject.IO_HUP:
            self._conn_mgr.close_connection()
        # TODO: handle other conditions
        return True

    def on_tab_close_button_clicked(self, button):
        # Called by gtk when the close button on the pages tab is clicked.
        self._conn_mgr.close_connection()
        app_view = AppView.get_instance()
        app_view['notebook'].remove_page(self._page_num)

    def on_button_press_on_source_view(self, source_view, ev):
        # Called by gtk when a button press has occurred on the sourceview
        # control. This method sets or removes line breakpoints.
        if not self._conn_mgr.can_interact:
            return
        iter = source_view.get_iter_of_pressed_line_number(ev)
        if iter != None:
            if ev.button == 1:
                # left button pressed
                self._set_line_breakpoint(iter.get_line())
            elif ev.button == 3:
                # right button pressed
                self._remove_line_breakpoint(iter.get_line())

    def on_source_list_row_activated(self, source_list, path, column):
        # Called by gtk when a row is clicked in the source list.
        file_uri = self._view.get_file_uri_from_list_path(path)
        if file_uri != self._view['source_view'].current_file_uri:
            self._view.update_source(self._source_cache[file_uri])
        else:
            self._view['uri_entry'].set_text(file_uri)

    def on_get_uri_button_clicked(self, *args):
        # Called by gtk when the get URI button is clicked, AND when enter
        # is pressed in the current URI entry. (The latter is due to the
        # connecting of the entries activate signal to this method).
        if not self._conn_mgr.can_interact:
            return
        entered_uri = self._view['uri_entry'].get_text()
        if entered_uri == self._view['source_view'].current_file_uri:
            return
        if self._source_cache.has_key(entered_uri):
            source = self._source_cache[entered_uri]
            self._view.update_source(source)
        else:
            callback = bind_params(self.on_get_uri_source, entered_uri)
            self._conn_mgr.send_source(entered_uri, callback)

    def on_property_clicked(self, notebook, column_id, context_id, name, type, value):
        if not self._conn_mgr.can_interact:
            return
        if column_id == 'value':
            display_names = self._conn_mgr.get_type_display_names()
            prop_view = ChangePropertyView(type, display_names)
            dialog = prop_view['prop_dialog']
            response = dialog.run()
            dialog.hide()
            if response == gtk.RESPONSE_ACCEPT:
                callback = bind_params(self.on_prop_set, name, context_id)
                self._conn_mgr.send_property_set(name, type=dialog.get_type(), 
                    value=dialog.get_value(), context=context_id, 
                    observer=callback)

    def on_check_init_steps(self):
        if len(self._init_steps_done) == _NUM_INIT_STEPS:
            # The page's initial state is prepared, make it show up.
            self._view['outer_box'].show_all()
            # Make this page be on top in the notebook.
            app_view = AppView.get_instance()
            app_view['notebook'].set_current_page(self._page_num)
            return False
        else:
            return True

    def on_command(self, mgr, command):
        # Called by conn_mgr when a command is being sent. The command string
        # is logged to the communcations log.
        self._view['log'].log('>>', str(command))

    def on_response(self, mgr, response):
        # Called by conn_mgr when a response was received. The XML is logged
        # to the communications log.
        self._view['log'].log('<<', str(response))

    def on_stream_response(self, mgr, response):
        # Called by conn_mgr when a packet of stream data is received. The data
        # is logged to the appropriate io stream widget.
        if response.type == 'stdout':
            self._view['stdout'].log_no_prefix(response.data)
        elif response.type == 'stderr':
            self._view['stderr'].log_no_prefix(response.data)

    def on_init_packet(self, mgr, init, remote_addr):
        # Called by conn_mgr when the initial XML packet is received from the
        # engine. Appends a new notebook page and requests the source for the
        # initial script.
        conn_info = init.get_engine_info()
        conn_info.update({ 'remote_ip': remote_addr[0], 
            'remote_port': remote_addr[1] })

        app_view = AppView.get_instance()
        self._page_num = self._view.append_page_on_init(conn_info, 
            app_view['notebook'])

        file_uri = init.file_uri
        src_callback = bind_params(self.on_init_source, file_uri)

        mgr.send_source(file_uri, observer=src_callback)
        mgr.send_typemap_get(observer=self.on_init_typemap_get)
        mgr.send_stdout(observer=self.on_init_stdout)
        mgr.send_stderr(observer=self.on_init_stderr)
        mgr.send_status(observer=self.on_init_status)

        config = Config.get_instance()
        gobject.timeout_add(config['init_check_timeout_ms'], 
            self.on_check_init_steps)

    def on_init_source(self, mgr, response, init_file_uri):
        # Called by conn_mgr after on_init_packet when the source of the script
        # file being debugged is received. The source is cached and the 
        # sourceview is updated with the text.
        source = Source(init_file_uri, response.source)
        self._source_cache[init_file_uri] = source
        self._view.update_source(source)
        self._init_steps_done.add('source')

    def on_init_typemap_get(self, mgr, response):
        self._init_steps_done.add('typemap_get')

    def on_init_stdout(self, mgr, response):
        self._init_steps_done.add('stdout')

    def on_init_stderr(self, mgr, response):
        # Called by conn_mgr after on_init_stdout with the result of the stderr
        # command. stderr is a core command, yet xdebug does not support it :) 
        # so we remove the tab page if the command fails. (this is true as of 
        # v2.0.3)
        if not response.successful:
            self._view.remove_stderr_page()
        self._init_steps_done.add('stderr')

    def on_init_status(self, mgr, response):
        # Called by conn_mgr after on_init_stderr with the initial status of
        # the debugger engine.  Makes the new tab page show up.

        if response.status == 'break':
            mgr.send_stack_get(self.on_cont_stack_get)

        # TODO: something will be here eventually ...
        self._init_steps_done.add('status')

    def on_cont_status(self, mgr, response):
        # Called by conn_mgr when a status response is received resulting from
        # a continuation command.  Requests stack information if the engine
        # is stopped on a line. Or, if not, updates the display accordingly.
        if response.status == 'break':
            mgr.send_stack_get(self.on_cont_stack_get)
        else:
            self._source_cache.unset_current_lines()
            source_view = self._view['source_view']
            source_view.refresh_current_line()
            source_view.scroll_to_current_line()

    def on_cont_stack_get(self, mgr, response):
        # Called by conn_mgr after on_cont_status, with a stack_get response.
        # Updates the the source in the source view and the line number if 
        # the file on the top of the stack is in the source cache. Or, requests
        # the source file on the top of the stack.
        stack = response.get_stack_elements()
        top = stack[0]
        source_view = self._view['source_view']

        self._source_cache.unset_current_lines()

        # check if the sourceview is showing the file on the top of the stack.
        # If so, update the current line and return.
        if source_view.current_file_uri == top['filename']:
            source_view.current_source.current_line = top['lineno']
            source_view.refresh_current_line()
            source_view.scroll_to_current_line()
            mgr.send_context_names(observer=self.on_cont_context_names)
            return

        if self._source_cache.has_key(top['filename']):
            source = self._source_cache[top['filename']]
            source.current_line = top['lineno']
            self._view.update_source(source)
            mgr.send_context_names(observer=self.on_cont_context_names)
        else:
            file_uri = top['filename']
            callback = bind_params(self.on_cont_source, stack)
            mgr.send_source(file_uri, callback)
            mgr.send_context_names(observer=self.on_cont_context_names)

    def on_cont_source(self, mgr, response, last_stack):
        # Called by conn_mgr after on_cont_stack_get, with a source response.
        # Updates the source in the sourceview and the current line number.
        top = last_stack[0]
        source = Source(top['filename'], response.source)
        source.current_line = top['lineno']
        self._source_cache[top['filename']] = source
        self._view.update_source(source)

    def on_cont_context_names(self, mgr, response):
        # Called by conn_mgr after on_cont_source or on_cont_stack_get with a
        # context_names response. Sends requests for all contexts.
        notebook = self._view['property_notebook']
        names = response.get_names()
        for (name, id) in names:
            observer = bind_params(self.on_cont_context_get, id)
            mgr.send_context_get(context_id=id, observer=observer)
            notebook.setup_property_page(id, name)
        notebook.remove_invalid_pages(id for (name, id) in names)

    def on_cont_context_get(self, mgr, response, context_id):
        if isinstance(response, ContextGetResponse):
            notebook = self._view['property_notebook']
            props = response.get_properties()
            notebook.refresh_properties(context_id, props)
    
    def on_breakpoint_set(self, mgr, response, source, line_num):
        # Called by conn_mgr with a breakpoint_set response. If the command
        # was successful, updates the internal state and the display.
        if isinstance(response, BreakpointSetResponse):
            source.add_breakpoint(line_num, response.id, 'line')
            self._view['source_view'].refresh_breakpoints()
        else:
            # TODO: do something ...
            pass

    def on_breakpoint_remove(self, mgr, response, source, id):
        # Called by conn_mgr with a breakpoint_remove response. If the command
        # was successful, updates the internal state and the display.
        if isinstance(response, BreakpointRemoveResponse):
            source.remove_breakpoint(id)
            self._view['source_view'].refresh_breakpoints()
        else:
            # TODO: do something ...
            pass

    def on_get_uri_source(self, mgr, response, entered_uri):
        # Called by conn_mgr with a source response containing source for a 
        # user requested file.
        if isinstance(response, SourceResponse):
            source = Source(entered_uri, response.source)
            self._source_cache[entered_uri] = source
            self._view.update_source(source)
        else:
            app_view = AppView.get_instance()
            app_view.show_warning('error_req_source', entered_uri, 
                response.error_msg)

    def on_prop_set(self, mgr, response, name, context_id):
        if isinstance(response, PropertySetResponse):
            callback = bind_params(self.on_prop_set_prop_get, context_id)
            mgr.send_property_get(name, context=context_id, observer=callback) 
        else:
            # TODO: do something ...
            pass

    def on_prop_set_prop_get(self, mgr, response, context_id):
        if isinstance(response, PropertyGetResponse):
            prop = response.get_property()
            self._view['property_notebook'].update_property(context_id, prop)
        else:
            # TODO: do something ...
            pass
