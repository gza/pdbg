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
    ('run', 'Run'),
    ('detach', 'Detach'),
    ('-', '-'),
    ('step_into', 'Step Into'),
    ('step_over', 'Step Over'),
    ('step_out', 'Step Out')
)

class ToolbarView(View, Singleton):

    def sensitize_continuation_buttons(self, sensitize):
        for (name, label) in _button_info:
            if name != '-':
                self[name].set_sensitive(sensitize)

    def _setup_toolbar(self, toolbar):
        asset_dir = Config.get_instance()['asset_dir']

        for (name, label) in _button_info:
            if name != '-':
                img = gtk.image_new_from_file(os.path.join(asset_dir, name + '.png'))
                self[name] = gtk.ToolButton(img, label)
                self[name].set_sensitive(False)
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
