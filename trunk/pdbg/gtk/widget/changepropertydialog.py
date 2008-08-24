# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk

_DIALOG_FLAGS = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT

_DIALOG_BUTTONS = (
    gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT
)

_SETTABLE_TYPES = set((
    'int',
    'bool',
    'float',
    'string'
))

class ChangePropertyDialog(gtk.Dialog):

    def __init__(self, parent, current_type, display_names):
        gtk.Dialog.__init__(self, _('Change Property Value'), parent, 
            _DIALOG_FLAGS, _DIALOG_BUTTONS)
        display_names = [i for i in display_names.items() if i[0] in _SETTABLE_TYPES]
        display_names.sort(lambda a, b: cmp(a[1], b[1]))
        type_idxs = [idx for (idx, n) in enumerate(display_names) if n[0] == current_type]
        if len(type_idxs) > 0:
            self._current_idx = type_idxs[0]
        else:
            self._current_idx = None
        self._display_names = display_names
        self._setup_controls()

    def get_value(self):
        return self._value_entry.get_text()

    def get_type(self):
        active_idx = self._type_combo.get_active()
        return self._display_names[active_idx][0]

    def _setup_controls(self):
        type_label = gtk.Label(_('Type:'))
        type_combo = gtk.combo_box_new_text()

        for (type, display) in self._display_names:
            type_combo.append_text(display)
        if self._current_idx != None:
            type_combo.set_active(self._current_idx)
        else:
            type_combo.set_active(0)

        value_label = gtk.Label(_('Value:'))
        value_entry = gtk.Entry()

        prop_table = gtk.Table(rows=2, columns=2)
        prop_table.attach(type_label, 0, 1, 0, 1, gtk.FILL, xpadding=4, ypadding=2)
        prop_table.attach(type_combo, 1, 2, 0, 1, xpadding=4, ypadding=2)
        prop_table.attach(value_label, 0, 1, 1, 2, gtk.FILL, xpadding=4, ypadding=2)
        prop_table.attach(value_entry, 1, 2, 1, 2, xpadding=4, ypadding=2)
        prop_table.show_all()

        outer_box = self.get_child()
        outer_box.pack_start(prop_table, False, False)

        self._type_combo = type_combo
        self._value_entry = value_entry

