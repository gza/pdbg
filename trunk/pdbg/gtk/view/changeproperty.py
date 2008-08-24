# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
from pdbg.gtk.widget.changepropertydialog import ChangePropertyDialog
from pdbg.gtk.view.app import AppView
from pdbg.gtk.view.base import View, widget

class ChangePropertyView(View):

    def __init__(self, current_type, display_names):
        self._current_type = current_type
        self._display_names = display_names
        super(ChangePropertyView, self).__init__()

    @widget
    def _prop_dialog(self):
        app_view = AppView.get_instance()
        dialog = ChangePropertyDialog(app_view['window'], self._current_type, 
            self._display_names)
        dialog.set_default_size(300, -1)
        return dialog

    def _setup(self):
        self._prop_dialog()
