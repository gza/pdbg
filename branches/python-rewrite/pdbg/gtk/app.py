# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import os.path
import gobject
import gtk
from ..app.patterns import Observable, Singleton
from ..app.config import Config
from ..dbgp.socketwrapper import SocketWrapper
from ..dbgp.connectionlistener import ConnectionListener
from view.app import AppView
from view.about import AboutView
from mgr.pages import PagesManager

class App(Observable, Singleton):

    def __init__(self):
        super(App, self).__init__()

    def _init_ui(self):
        config = Config.get_instance()
        self._app_view = AppView.get_instance()
        self._about_view = AboutView()

        self._app_view['window'].connect('destroy', self.on_quit_app)
        self._app_view['quit_item'].connect('activate', self.on_quit_app)
        self._app_view['about_item'].connect('activate', self.on_activate_about)

    def _init_app(self):
        self._listener = ConnectionListener(SocketWrapper)

        # Interpolate the ip address/port into the placeholder label.
        info_lbl = self._app_view['info_page_label']
        info_lbl.set_text(info_lbl.get_text() % (self._listener.ip_address, \
            self._listener.port))

        config = Config.get_instance()
        gobject.timeout_add(config['timeout_interval'], self.on_timeout)

    def run(self):
        self._init_ui()
        self._init_app()
        self._app_view['window'].show_all()
        gtk.main()

    def on_activate_about(self, item):
        self._about_view['about_dialog'].run()
        self._about_view['about_dialog'].hide()

    def on_timeout(self):
        #connection = self._listener.accept()
        #if connection != None:
        #    pass
        return True

    def on_quit_app(self, *arguments):
        gtk.main_quit()
