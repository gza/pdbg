# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Management of a single ui tab page."""

__version__ = "$Id$"

from ...app.patterns import Manager
from ..view.app import AppView

class PageManager(Manager):

    def setup(self, connection):
        """Setup the manager."""
        self._connection = connection
