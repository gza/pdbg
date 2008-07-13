# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of the toolbar ui."""

__version__ = "$Id$"

from ...app.patterns import Manager, Singleton
from ..view.app import AppView

class ToolbarManager(Manager, Singleton):

    """Management of the toolbar ui."""

    def __init__(self):
        """Construct an instance."""
        pass

    def setup(self):
        """Setup the manager."""
        pass
