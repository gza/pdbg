# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import os.path
from base import View, widget
from ...app.config import Config
from ...app.patterns import Singleton

_button_info = (
    ('run', _('Run'), _('Start or resume a script')),
    ('detach', _('Detach'), _('Stop interaction with the debugger engine')),
    ('-', '-', '-'),
    ('step_into', _('Step Into'), _('Step to the next statement')),
    ('step_over', _('Step Over'), _('Step to the next statement in the same scope')),
    ('step_out', _('Step Out'), _('Step to the next statement out of the current scope'))
)

class ToolbarView(View, Singleton):

    def sensitize_continuation_buttons(self, sensitize):
        for (name, label, tip) in _button_info:
            if name != '-':
                self[name].set_sensitive(sensitize)

    def _setup_toolbar(self, toolbar):
        asset_dir = Config.get_instance()['asset_dir']

        for (name, label, tip) in _button_info:
            if name != '-':
                img = gtk.image_new_from_file(os.path.join(asset_dir, name + '.png'))
                self[name] = gtk.ToolButton(img, label)
                self[name].set_sensitive(False)
                self[name].set_tooltip_text(tip)
                item = self[name]
            else:
                item = gtk.SeparatorToolItem()
            toolbar.insert(item, -1)

    @widget
    def _toolbar(self):
        toolbar = gtk.Toolbar()
        self._setup_toolbar(toolbar)
        return toolbar

    def _setup(self):
        self._toolbar()
