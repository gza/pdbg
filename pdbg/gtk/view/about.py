# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
from base import View, widget

class AboutView(View):

    @widget
    def _about_dialog(self):
        dialog = gtk.AboutDialog()
        dialog.set_name('pDBG')
        dialog.set_version('0.01')
        dialog.set_website('http://pdbg.googlecode.com')
        return dialog

    def _setup(self):
        self._about_dialog()
