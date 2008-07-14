# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import gtksourceview as sv
import pango
import time
import re

class SourceView(sv.SourceView):

    def __init__(self):
        sv.SourceView.__init__(self)

        lang_mgr = sv.SourceLanguagesManager()
        php_lang = lang_mgr.get_language_from_mime_type('application/x-php')

        buffer = sv.SourceBuffer()
        buffer.set_language(php_lang)
        buffer.set_highlight(True)

        self.set_show_line_numbers(True)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_buffer(buffer)
        self._set_font()

    def _set_font(self):
        desc = pango.FontDescription()
        desc.set_family('Mono')
        self.modify_font(desc)
