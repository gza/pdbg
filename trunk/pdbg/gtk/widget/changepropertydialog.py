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

_TYPE_COMBO_NAMES = (
    _('Automatic'),
    _('Boolean'),
    _('Float'),
    _('Integer'),
    _('String'),
)

(
    TYPE_AUTO,
    TYPE_BOOLEAN,
    TYPE_FLOAT,
    TYPE_INT,
    TYPE_STRING
) = range(5)

class ChangePropertyDialog(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, _('Change Property Value'), parent, 
            _DIALOG_FLAGS, _DIALOG_BUTTONS)
        self._setup_controls()

    def get_value(self):
        return self._value_entry.get_text()

    def get_type(self):
        return self._type_combo.get_active()

    def _setup_controls(self):
        type_label = gtk.Label(_('Type:'))
        type_combo = gtk.combo_box_new_text()

        for name in _TYPE_COMBO_NAMES:
            type_combo.append_text(name)
        type_combo.set_active(TYPE_AUTO)

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

