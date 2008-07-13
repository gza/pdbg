# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of a single ui tab page."""

__version__ = "$Id$"

import gobject
from ...app.patterns import Manager
from ...app.mgr.connection import ConnectionManager
from ...app.config import Config
from ..view.app import AppView
from ..view.page import PageView

class PageManager(Manager):

    def setup(self, connection):
        """Setup the manager."""
        self._connection = connection
        self._conn_mgr = ConnectionManager()
        self._conn_mgr.setup(connection)
        self._conn_mgr.add_observer('init_packet', self.on_init_packet)

        # Add a hook in the gobject main loop to monitor for incoming data
        # on the socket.
        gobject.io_add_watch( \
            connection.socket.handle, \
            gobject.IO_IN | gobject.IO_HUP | gobject.IO_ERR, \
            self.on_io_event)

    def on_io_event(self, source, condition):
        if condition == gobject.IO_IN:
            self._conn_mgr.process_response()
        # TODO: handle other conditions
        return True

    def on_init_packet(self, mgr, init, remote_addr):
        conn_info = init.get_engine_info()
        addr_info = { 'remote_ip': remote_addr[0], \
            'remote_port': remote_addr[1] }
        conn_info.update(addr_info)

        self._view = PageView(conn_info)
        outer_box = self._view['outer_box']
        tab_label = self._view['tab_label']

        app_view = AppView.get_instance()
        self.page_num = app_view['notebook'].append_page(outer_box, tab_label)

        # TODO: move
        outer_box.show_all()
