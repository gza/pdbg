# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import os.path
from base import View, widget
from ...app.config import Config
from ...app.patterns import Singleton
from ..widget.mainnotebook import MainNotebook
from toolbar import ToolbarView

_dialog_messages = {
    'error_req_source': _('Request for %s failed: %s'),
    'conn_closed': _('Connection to debugger engine closed unexpectedly!'),
}

class AppView(View, Singleton):

    def show_ok_message_dialog(self, type, title, msg_id, *args):
        dialog = gtk.MessageDialog(self['window'],
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            type,
            gtk.BUTTONS_OK,
            _dialog_messages[msg_id] % args)
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

    def show_warning(self, msg_id, *args):
        self.show_ok_message_dialog(gtk.MESSAGE_WARNING, 
            _('Whoops!'),
            msg_id, *args)

    def show_error(self, msg_id, *args):
        self.show_ok_message_dialog(gtk.MESSAGE_ERROR,
            _('An Error Occurred!'),
            msg_id, *args)

    @widget
    def _quit_item(self):
        item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        return item

    @widget
    def _about_item(self):
        item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        return item

    @widget
    def _file_menu(self):
        menu = gtk.Menu()
        menu.add(self._quit_item())
        return menu

    @widget
    def _help_menu(self):
        menu = gtk.Menu()
        menu.add(self._about_item())
        return menu

    @widget
    def _file_menu_item(self):
        item = gtk.MenuItem(_("_File"))
        item.set_submenu(self._file_menu())
        return item

    @widget
    def _help_menu_item(self):
        item = gtk.MenuItem(_("_Help"))
        item.set_submenu(self._help_menu())
        return item

    @widget
    def _menu_bar(self): 
        menu_bar = gtk.MenuBar()
        menu_bar.append(self._file_menu_item())
        menu_bar.append(self._help_menu_item())
        return menu_bar

    @widget
    def _info_page_label(self):
        return gtk.Label(_('Listening for connections on %s:%s ...'))

    @widget
    def _info_tab_label(self):
        return gtk.Label(_('pDBG Information'))

    @widget
    def _notebook(self):
        notebook = MainNotebook()
        notebook.append_page(self._info_page_label(), self._info_tab_label())
        return notebook

    @widget
    def _outer_vbox(self):
        toolbar_view = ToolbarView.get_instance()

        vbox = gtk.VBox()
        vbox.pack_start(self._menu_bar(), False, True)
        vbox.pack_start(toolbar_view['toolbar'], False, True)
        vbox.pack_start(self._notebook(), True, True)
        return vbox

    @widget
    def _window(self):
        config = Config.get_instance()

        win = gtk.Window()
        win.set_title(config['app_title'])
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_default_size(config['win_width'], config['win_height'])
        win.add(self._outer_vbox())
        return win

    def _setup(self):
        self._window()
