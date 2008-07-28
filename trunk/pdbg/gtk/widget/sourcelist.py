# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gobject
import pango
import gtk

COLUMN_URI = 0

class SourceList(gtk.TreeView):

    def __init__(self):
        model = self._create_model()
        gtk.TreeView.__init__(self, model)
        # Turn off zebra striping since there is only one column.
        self.set_rules_hint(False)
        self._add_columns()

    def _create_model(self):
        list_store = gtk.ListStore(gobject.TYPE_STRING)
        for i in range(0, 20):
            iter = list_store.append()
            list_store.set(iter, COLUMN_URI, 'Line ' + str(i+1))
        return list_store

    def _add_columns(self):
        renderer = gtk.CellRendererText()
        renderer.set_property('ellipsize-set', True)
        renderer.set_property('ellipsize', pango.ELLIPSIZE_END)
        column = gtk.TreeViewColumn('File URI', renderer, \
            text=COLUMN_URI)
        column.set_sort_column_id(COLUMN_URI)
        column.set_clickable(False)
        self.append_column(column)



