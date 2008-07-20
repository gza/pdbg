# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of the toolbar ui."""

__version__ = "$Id$"

from ...app.patterns import Manager, Singleton
from ..view.toolbar import ToolbarView
from pages import PagesManager

_continuation_commands = (
    'run', 'detach', 'step_into', 'step_over', 'step_out'
)

class ToolbarManager(Manager, Singleton):

    """Management of the toolbar ui."""

    def __init__(self):
        """Construct an instance."""
        self._page_mgr = None
        pass

    def setup(self):
        """Setup the manager."""
        toolbar_view = ToolbarView.get_instance()
        for command in _continuation_commands:
            widget = toolbar_view[command]
            widget.connect('clicked', self.on_continuation_clicked, command)

        pages_mgr = PagesManager.get_instance()
        pages_mgr.add_observer( \
            page_mgr_deactivated=self.on_page_mgr_deactivated, \
            page_mgr_activated=self.on_page_mgr_activated)

    def on_continuation_clicked(self, button, command_name):
        """A toolbar button was clicked."""
        if self._page_mgr == None:
            raise ToolbarManagerException, "buttons should be desensitized."
        self._page_mgr.send_continuation(command_name)

    def on_page_mgr_deactivated(self, pages_mgr, page_mgr):
        """Called when a page manager is not the focus of the shared ui.
        
        Essentially, this means that the tab corresponding to the
        page_mgr parameter is no longer the current page.
        """
        if self._page_mgr != None:
            conn_mgr = self._page_mgr.conn_mgr
            conn_mgr.remove_observer('can_interact', \
                self.on_conn_can_interact)
        self._page_mgr = None
        toolbar_view = ToolbarView.get_instance()
        toolbar_view.sensitize_continuation_buttons(False)

    def on_page_mgr_activated(self, pages_mgr, page_mgr):
        """Called when a page manager becomes the focus of the shared ui.
        
        Essentially, this means that the tab corresponding to the
        page_mgr parameter is now the current page.
        """
        toolbar_view = ToolbarView.get_instance()
        toolbar_view.sensitize_continuation_buttons( \
            page_mgr.conn_mgr.can_interact)

        page_mgr.conn_mgr.add_observer('can_interact', \
            self.on_conn_can_interact)
        self._page_mgr = page_mgr

    def on_conn_can_interact(self, conn_mgr, can_interact):
        """Connection received a response."""
        toolbar_view = ToolbarView.get_instance()
        toolbar_view.sensitize_continuation_buttons(can_interact)
