# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import os.path
from view import View, widget
from ...app.config import Config

class AppView(View):

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
        item = gtk.MenuItem("_File")
        item.set_submenu(self._file_menu())
        return item

    @widget
    def _help_menu_item(self):
        item = gtk.MenuItem("_Help")
        item.set_submenu(self._help_menu())
        return item

    @widget
    def _menu_bar(self): 
        menu_bar = gtk.MenuBar()
        menu_bar.append(self._file_menu_item())
        menu_bar.append(self._help_menu_item())
        return menu_bar

    def _setup_tool_bar(self, tool_bar):
        asset_dir = Config.get_instance()['asset_dir']

        button_data = (
            ('run', 'Run'),
            ('detach', 'Detach'),
            ('-', '-'),
            ('step_into', 'Step Into'),
            ('step_over', 'Step Over'),
            ('step_out', 'Step Out')
        )

        for (name, label) in button_data:
            if name != '-':
                key = 'toolbar_' + name
                img = gtk.image_new_from_file(os.path.join(asset_dir, name + '.png'))
                self[key] = gtk.ToolButton(img, label)
                item = self[key]
            else:
                item = gtk.SeparatorToolItem()
            tool_bar.insert(item, -1)

    @widget
    def _tool_bar(self):
        tool_bar = gtk.Toolbar()
        self._setup_tool_bar(tool_bar)
        return tool_bar

    @widget
    def _info_page_label(self):
        return gtk.Label("Listening for connections on %s:%s ...")

    @widget
    def _info_tab_label(self):
        return gtk.Label('pDBG Information')

    @widget
    def _notebook(self):
        notebook = gtk.Notebook()
        notebook.append_page(self._info_page_label(), self._info_tab_label())
        return notebook

    @widget
    def _outer_vbox(self):
        vbox = gtk.VBox()
        vbox.pack_start(self._menu_bar(), False, True)
        vbox.pack_start(self._tool_bar(), False, True)
        vbox.pack_start(self._notebook(), True, True)
        return vbox

    @widget
    def _window(self):
        win = gtk.Window()
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_default_size(800, 600)
        win.add(self._outer_vbox())
        return win

    def _setup(self):
        self._window()
