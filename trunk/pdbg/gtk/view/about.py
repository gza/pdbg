# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
from pdbg.gtk.view.base import View, widget
from pdbg.app.config import Config
from pdbg.app.patterns import Singleton

_license_text = \
"""pDBG is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

pDBG is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with pDBG.  If not, see <http://www.gnu.org/licenses/>.
"""

class AboutView(View, Singleton):

    @widget
    def _about_dialog(self):
        config = Config.get_instance()

        dialog = gtk.AboutDialog()
        dialog.set_name('pDBG')
        dialog.set_version('0.01')
        dialog.set_website('http://pdbg.googlecode.com')
        dialog.set_authors(['Christopher Utz <cutz@chrisutz.com>'])
        dialog.set_copyright(u'\u00A92008 Christopher Utz')
        dialog.set_comments('A frontend for DBGp protocol based debugging engines')
        dialog.set_license(_license_text)
        dialog.set_wrap_license(True)
        return dialog

    def _setup(self):
        self._about_dialog()
