# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of a single ui tab page."""

__version__ = "$Id$"

import gobject
from ...app.patterns import Manager
from ...app.mgr.connection import ConnectionManager
from ...app.config import Config
from ...dbgp.engineresponse import StatusResponse, StackGetResponse
from ..view.app import AppView
from ..view.page import PageView

class PageManager(Manager):

    def __init__(self):
        super(Manager, self).__init__()
        self._source_cache = {}

    def setup(self, connection):
        """Setup the manager."""
        self._connection = connection
        self._conn_mgr = ConnectionManager()
        self._conn_mgr.setup(connection)

        self._conn_mgr.add_observer(
            command_sent=self.on_command_sent,
            response_received=self.on_response_received,
            init_packet=self.on_init_packet)

        # Add a hook in the gobject main loop to monitor for incoming data
        # on the socket.
        gobject.io_add_watch(
            connection.socket.handle,
            gobject.IO_IN | gobject.IO_HUP | gobject.IO_ERR,
            self.on_io_event)

        self._view = PageView()

        app_view = AppView.get_instance()
        app_view['notebook'].connect('page-reordered', self.on_page_reordered)

    @property
    def conn_mgr(self):
        return self._conn_mgr

    def send_continuation(self, command):
        self._conn_mgr.send_continuation(command, self.on_cont_status)

    def on_io_event(self, source, condition):
        if condition == gobject.IO_IN:
            self._conn_mgr.process_response()
        # TODO: handle other conditions
        return True

    def on_page_reordered(self, notebook, child, page_num):
        # If the page ordering of the notebook is modified, ensure that the
        # _page_num variable is updated accordingly.
        if child == self._view['outer_box']:
            self._page_num = page_num

    def on_command_sent(self, mgr, command):
        self._view['log'].log('>>', str(command))

    def on_response_received(self, mgr, response):
        self._view['log'].log('<<', str(response))

    def on_init_packet(self, mgr, init, remote_addr):
        conn_info = init.get_engine_info()
        addr_info = { 'remote_ip': remote_addr[0], \
            'remote_port': remote_addr[1] }
        conn_info.update(addr_info)

        self._view.set_connection_info(conn_info)

        outer_box = self._view['outer_box']
        tab_label = self._view['tab_label']

        app_view = AppView.get_instance()
        self._page_num = app_view['notebook'].append_page(outer_box, tab_label)

        mgr.send_source(init.file_uri, self.on_init_source)

    def on_init_source(self, mgr, response):
        self._view.set_source(response.source)
        mgr.send_status(self.on_init_status)

    def on_init_status(self, mgr, response):
        # The page's initial state is prepared, make it show up.
        self._view['outer_box'].show_all()

        # Make this page be on top in the notebook.
        app_view = AppView.get_instance()
        app_view['notebook'].set_current_page(self._page_num)

    def on_cont_status(self, mgr, response):
        if response.status == 'break':
            mgr.send_stack_get(self.on_cont_stack_get)
        else:
            self._view['source_view'].unset_current_line()

    def on_cont_stack_get(self, mgr, response):
        # check the source file in the source view currently, and
        # change it if it differs from the top of the stack.

        stack = response.get_stack_elements()
        self._view['source_view'].set_current_line(stack[0]['lineno']-1)

        #current = stack[0]
        #
        #if self._source_cache.has_key(current['filename']):
        #    self._view.set_source(self._source_cache[current['filename']])
        #else:
        #    self._conn_mgr.add_observer('source', self.on_source_update_view, \
        #        once_only=True)
        #    self._conn_mgr.send_source(current['filename'])
