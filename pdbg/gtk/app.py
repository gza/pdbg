# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gettext
gettext.install('pdbg')

import gobject
import gtk
import logging
from pdbg.app.patterns import Observable, Singleton
from pdbg.app.config import Config
from pdbg.app.mgr.listener import ListenerManager
from pdbg.gtk.mgr.pages import PagesManager
from pdbg.gtk.mgr.toolbar import ToolbarManager
from pdbg.gtk.view.app import AppView
from pdbg.gtk.view.about import AboutView

_gtk_styles = \
"""
style "tab-close-button-style" {
    xthickness = 0
    ythickness = 0
}
widget "*.tab-close-button" style "tab-close-button-style"
"""

class App(Observable, Singleton):

    def __init__(self):
        super(App, self).__init__()

    def _setup(self):
        config = Config.get_instance()

        logging.basicConfig(
            level=config['logging_level'], 
            format='%(asctime)s %(levelname)s %(message)s')

        # Override some of the theme styles.
        gtk.rc_parse_string(_gtk_styles)

        # Connect application signal handlers.
        app_view = AppView.get_instance()
        app_view['window'].connect('destroy', self.on_quit_app)
        app_view['quit_item'].connect('activate', self.on_quit_app)
        app_view['about_item'].connect('activate', self.on_activate_about)

        # Setup singleton managers.
        ListenerManager.get_instance().setup()
        PagesManager.get_instance().setup()
        ToolbarManager.get_instance().setup()

        # Interpolate the ip address/port into the placeholder label.
        app_view = AppView.get_instance()
        info_lbl = app_view['info_page_label']
        listener = ListenerManager.get_instance().listener
        info_lbl.set_text(info_lbl.get_text() % (listener.ip_address, \
            listener.port))

        # Register a function to poll for incoming connections.
        gobject.timeout_add(config['listener_timeout_ms'], self.on_timeout)

    def run(self):
        self._setup()
        AppView.get_instance()['window'].show_all()
        gtk.main()

    def on_activate_about(self, item):
        about_view = AboutView.get_instance()
        about_view['about_dialog'].run()
        about_view['about_dialog'].hide()

    def on_timeout(self):
        ListenerManager.get_instance().accept_connection()
        return True

    def on_quit_app(self, *arguments):
        gtk.main_quit()
