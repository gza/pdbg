# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import gobject
import pango
from logging import getLogger
from pdbg.dbgp.engineresponse import *

(
    COLUMN_NAME,
    COLUMN_TYPE,
    COLUMN_VALUE
) = range(3)

# Ids are not used for display, that is why they are not wrapped by _().
_COLUMN_IDS = (
    'name',
    'type',
    'value'
)

_COLUMN_TYPES = (
    gobject.TYPE_STRING,
    gobject.TYPE_STRING,
    gobject.TYPE_STRING
)

def _get_prop_display_value(prop):
    if prop['type'] in ('string', 'int', 'float'):
        return prop['value']
    elif prop['type'] == 'bool':
        if prop['value'] in ('0', 'false'):
            return 'false'
        else:
            return 'true'
    elif prop['type'] == 'uninitialized':
        return 'uninitialized'
    else:
        return 'cannot render'

class PropertyPageModel(gtk.ListStore):

    def __init__(self):
        gtk.ListStore.__init__(self, *_COLUMN_TYPES)

    def get_property_iter(self, name):
        iter = self.get_iter_first()
        while iter:
            if self.get_value(iter, COLUMN_NAME) == name:
                return iter
            iter = self.iter_next(iter)
        return None

    def remove_invalid_properties(self, valid_names):
        iter = self.get_iter_first()
        valid_names = set(valid_names)
        # remove advances the iter to the next row. if no more rows remain,
        # remove returns False.
        while iter:
            name = self.get_value(iter, COLUMN_NAME)
            if name not in valid_names:
                if not self.remove(iter):
                    return
            else:
                iter = self.iter_next(iter)

    def set_property(self, name, type, value):
        iter = self.get_property_iter(name)
        if iter:
            self.set(iter, COLUMN_VALUE, value, COLUMN_TYPE, type)
        else:                
            self.append((name, type, value))

class PropertyPage(gtk.TreeView):

    def __init__(self):
        gtk.TreeView.__init__(self, PropertyPageModel())
        self.set_rules_hint(True)
        self.set_headers_clickable(True)
        self._add_columns()

    def _add_columns(self):
        name_renderer = gtk.CellRendererText()
        name_renderer.set_property('ellipsize', pango.ELLIPSIZE_END)

        name_col = gtk.TreeViewColumn(_('Name'), name_renderer,
            text=COLUMN_NAME)
        name_col.set_sort_column_id(COLUMN_NAME)
        name_col.set_resizable(True)
        name_col.id = _COLUMN_IDS[COLUMN_NAME]

        type_col = gtk.TreeViewColumn(_('Type'), gtk.CellRendererText(),
            text=COLUMN_TYPE)
        type_col.set_sort_column_id(COLUMN_TYPE)
        type_col.id = _COLUMN_IDS[COLUMN_TYPE]

        value_renderer = gtk.CellRendererText()
        value_renderer.set_property('ellipsize', pango.ELLIPSIZE_END)

        value_col = gtk.TreeViewColumn(_('Value'), value_renderer,
            text=COLUMN_VALUE)
        value_col.id = _COLUMN_IDS[COLUMN_VALUE]

        self.append_column(name_col)
        self.append_column(type_col)
        self.append_column(value_col)

class PropertyNotebook(gtk.Notebook):

    def __init__(self):
        gtk.Notebook.__init__(self)
        self.set_tab_pos(gtk.POS_BOTTOM)
        self._pages = {}

    def remove_invalid_pages(self, valid_ids):
        to_remove = set(self._pages.keys()) - set(valid_ids)
        for remove_id in to_remove:
            self.remove_page(self.page_num(self._pages[remove_id]))
            del self._pages[remove_id]

    def setup_property_page(self, page_id, label):
        if self._pages.has_key(page_id):
            page = self._pages[page_id]
            if self.get_tab_label_text(page) != label:
                page.get_child().get_model().clear()
        else:
            page = self._create_scrolled_property_page()
            page.get_child().connect('row-activated', self.on_row_activated, page_id)
            self.append_page(page, gtk.Label(label))
            page.show_all()
            self._pages[page_id] = page

    def refresh_properties(self, page_id, props):
        page  = self._pages[page_id]
        model = page.get_child().get_model()
        names = []
        for prop in props:
            value = _get_prop_display_value(prop)
            model.set_property(prop['fullname'], prop['type'], value)
            names.append(prop['fullname'])
        model.remove_invalid_properties(names)

    def update_property(self, page_id, prop):
        page  = self._pages[page_id]
        model = page.get_child().get_model()
        # TODO: maybe set_property shouldn't be used here, since it adds it
        # if it does not exist.
        value = _get_prop_display_value(prop)
        model.set_property(prop['fullname'], prop['type'], value)

    def on_row_activated(self, page, path, column, page_id):
        model = page.get_model()
        iter  = model.get_iter(path)
        cols  = model.get(iter, COLUMN_NAME, COLUMN_TYPE, COLUMN_VALUE)
        self.emit('property-clicked', column.id, page_id, *cols)

    def _create_scrolled_property_page(self):
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(PropertyPage())
        return scroll

gobject.type_register(PropertyNotebook)

PropertyNotebook.property_clicked = gobject.signal_new(
    'property-clicked',
    PropertyNotebook,
    gobject.SIGNAL_RUN_LAST,
    gobject.TYPE_NONE,
    (
        gobject.TYPE_STRING, 
        gobject.TYPE_STRING, 
        gobject.TYPE_STRING, 
        gobject.TYPE_STRING, 
        gobject.TYPE_STRING
    )
)
