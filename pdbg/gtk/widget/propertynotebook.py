# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import gobject
import pango
from pdbg.dbgp.engineresponse import *

(
    COLUMN_NAME,
    COLUMN_VALUE
) = range(2)

COLUMN_TYPES = (
    gobject.TYPE_STRING,
    gobject.TYPE_STRING
)

class PropertyPageSourceModel(gtk.ListStore):

    def __init__(self):
        gtk.ListStore.__init__(self, *COLUMN_TYPES)

class PropertyPage(gtk.TreeView):

    def __init__(self):
        gtk.TreeView.__init__(self, PropertyPageSourceModel())
        self.set_rules_hint(True)
        self._add_columns()

    def _add_columns(self):
        name_col = gtk.TreeViewColumn(_('Name'), gtk.CellRendererText(), 
            text=COLUMN_NAME)
        name_col.set_clickable(False)

        value_renderer = gtk.CellRendererText()
        value_renderer.set_property('ellipsize', pango.ELLIPSIZE_END)

        value_col = gtk.TreeViewColumn(_('Value'), value_renderer,
            text=COLUMN_VALUE)
        value_col.set_clickable(False)

        self.append_column(name_col)
        self.append_column(value_col)

class PropertyNotebook(gtk.Notebook):

    def __init__(self):
        gtk.Notebook.__init__(self)
        self.set_tab_pos(gtk.POS_BOTTOM)
        self._pages = {}

    def remove_all_pages(self):
        while self.get_n_pages() > 0:
            self.remove_page(0)
        self._pages.clear()

    def append_property_page(self, page_id, label):
        page = PropertyPage()
        self.append_page(page, gtk.Label(label))
        page.show_all()
        self._pages[page_id] = page

    def update_property_page(self, page_id, props):
        page = self._pages[page_id]
        model = page.get_model()
        for prop in props:
            if prop['type'] in ('string', 'int', 'float'):
                value = prop['value']
            elif prop['type'] == 'uninitialized':
                value = 'uninitialized'
            else:
                value = 'cannot render'
            model.append((prop['fullname'], value))
