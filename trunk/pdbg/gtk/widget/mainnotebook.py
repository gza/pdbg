# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk

class MainNotebook(gtk.Notebook):

    def __init__(self):
        gtk.Notebook.__init__(self)

    def append_page_with_button(self, child, tab_label, button):
        box = gtk.HBox()
        box.pack_start(tab_label, True, True)
        box.pack_end(button, False, False)
        box.show_all()

        return self.append_page(child, box)
