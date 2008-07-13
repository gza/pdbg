# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of the toolbar ui."""

__version__ = "$Id$"

from ...app.patterns import Manager, Singleton
from ..view.app import AppView

_continuation_commands = (
    'run', 'detach', 'step_into', 'step_over', 'step_out'
)

class ToolbarManager(Manager, Singleton):

    """Management of the toolbar ui."""

    def __init__(self):
        """Construct an instance."""
        pass

    def setup(self):
        """Setup the manager."""
        app_view = AppView.get_instance()
        for command in _continuation_commands:
            widget = app_view['toolbar_' + command]
            widget.connect('clicked', self.on_continuation_clicked, command)

    def on_continuation_clicked(self, button, command_name):
        pass
