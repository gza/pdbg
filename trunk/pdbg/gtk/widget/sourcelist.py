# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gobject
import pango
import gtk

COLUMN_URI = 0

class SourceModelException(Exception):
    pass

class SourceListModel(gtk.ListStore):

    def __init__(self):
        gtk.ListStore.__init__(self, gobject.TYPE_STRING)

    def has_source(self, source):
        iter = self.get_iter_first()
        file_uri = source.file_uri
        while iter != None:
            (iter_file_uri,) = self.get(iter, COLUMN_URI)
            if iter_file_uri == file_uri:
                return True
            iter = self.iter_next(iter)
        return False

    def add_source(self, source):
        self.append((source.file_uri,))

    def get_file_uri_from_path(self, path):
        iter = self.get_iter(path)
        if iter == None:
            raise SourceModelException("Invalid model path: %s" % (path,))
        return self.get(iter, COLUMN_URI)[0]

class SourceList(gtk.TreeView):

    def __init__(self):
        gtk.TreeView.__init__(self, SourceListModel())
        # Turn off zebra striping since there is only one column.
        self.set_rules_hint(False)
        self._add_columns()

    def _add_columns(self):
        renderer = gtk.CellRendererText()
        renderer.set_property('ellipsize', pango.ELLIPSIZE_START)
        column = gtk.TreeViewColumn(_('Known File URIs'), renderer, text=COLUMN_URI)
        column.set_sort_column_id(COLUMN_URI)
        column.set_clickable(False)
        self.append_column(column)

