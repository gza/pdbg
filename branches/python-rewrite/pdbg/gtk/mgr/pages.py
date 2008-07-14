# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of ui tab pages."""

__version__ = "$Id$"

from ...app.patterns import Manager, Singleton
from ...app.mgr.listener import ListenerManager
from page import PageManager
from ..view.app import AppView

_event_names = (
    'page_mgr_deactivated',
    'page_mgr_activated'
)

class PagesManager(Manager, Singleton):

    """Management of ui tab pages.

    This class receives new connections from the listener manager, and binds
    them to page manager instances.  Additionally, it manages the main ui
    notebook widget.
    """

    def __init__(self):
        """Construct an instance."""
        super(PagesManager, self).__init__()
        self._page_mgrs = []
        self._active_mgr = None
        self.register_event(*_event_names)

    def setup(self):
        """Setup the manager."""
        listener_mgr = ListenerManager.get_instance()
        listener_mgr.add_observer('new_connection', self.on_new_connection)

        app_view = AppView.get_instance()
        app_view['notebook'].connect('switch-page', self.on_switch_page)

    def on_switch_page(self, notebook, page, page_num):
        if self._active_mgr != None:
            self.fire('page_mgr_deactivated', self._active_mgr)
            self._active_mgr = None
        if page_num > 0:
            self._active_mgr = self._page_mgrs[page_num-1]
            self.fire('page_mgr_activated', self._active_mgr)

    def on_new_connection(self, mgr, connection):
        """Handle the establishment of new DBGp connections.

        Binds new connections to page manager instances.
        """
        page_mgr = PageManager()
        page_mgr.setup(connection)
        self._page_mgrs.append(page_mgr)
