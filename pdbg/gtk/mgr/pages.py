# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of ui tab pages."""

__version__ = "$Id$"

from ...app.patterns import Manager, Singleton
from ...app.mgr.listener import ListenerManager
from page import PageManager
from ..view.app import AppView

class PagesManager(Manager, Singleton):

    """Management of ui tab pages.

    This class receives new connections from the listener manager, and binds
    them to page manager instances.  Additionally, it manages the main ui
    notebook widget.
    """

    def __init__(self):
        """Construct an instance."""
        self._page_mgrs = []

    def setup(self):
        """Setup the manager."""
        listener_mgr = ListenerManager.get_instance()
        listener_mgr.add_observer('new_connection', self.on_new_connection)

    def on_new_connection(self, mgr, connection):
        """Handle the establishment of new DBGp connections.

        Binds new connections to page manager instances.
        """
        page_mgr = PageManager()
        page_mgr.setup(connection)
        self._page_mgrs.append(page_mgr)
