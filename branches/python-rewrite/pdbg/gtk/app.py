# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

import os.path
import gtk.glade
from ..app.observable import Observable
from ..app.config import Config
from ..dbgp.socketwrapper import SocketWrapper
from ..dbgp.connectionlistener import ConnectionListener

class App(Observable):

    _app = None

    def __init__(self):
        Observable.__init__(self)

    @classmethod
    def get_instance(klass):
        if klass._app == None:
            klass._app = klass()
        return klass._app

    @property
    def main_window_xml(self):
        return self._main_xml

    def _init_ui(self):
        config = Config.get_instance()

        # Setup the main ui 
        glade_file = os.path.join(config.asset_dir, 'mainwindow.glade')
        self._main_xml = gtk.glade.XML(glade_file)

        # Setup the about dialog ui
        glade_file = os.path.join(config.asset_dir, 'aboutdialog.glade')
        self._about_xml = gtk.glade.XML(glade_file)

        # Setup the main window signal handlers.
        self._main_window = self._main_xml.get_widget('main_window')
        self._main_window.connect('destroy', self.on_quit_app)

        # Setup the menu bar item signal handlers.
        quit_item = self._main_xml.get_widget('menubar_quit')
        quit_item.connect('activate', self.on_quit_app)

        about_item = self._main_xml.get_widget('menubar_about')
        about_item.connect('activate', self.on_activate_about)

    def _init_app(self):
        self._listener = ConnectionListener(SocketWrapper)

        # Interpolate the ip address/port into the placeholder label.
        info_lbl = self._main_xml.get_widget('main_notebook_info')
        info_lbl.set_text(info_lbl.get_text() % (self._listener.ip_address, \
            self._listener.port))

    def run(self):
        self._init_ui()
        self._init_app()
        self._main_window.show_all()
        gtk.main()

    def on_activate_about(self, item):
        dialog = self._about_xml.get_widget('about_dialog')
        dialog.run()
        dialog.hide()

    def on_quit_app(self, *arguments):
        gtk.main_quit()
