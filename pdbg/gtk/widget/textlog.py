# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import pango
import time
import re

class TextLog(gtk.TextView):

    def __init__(self):
        gtk.TextView.__init__(self)
        self.set_buffer(gtk.TextBuffer())
        self.set_editable(False)
        self.set_cursor_visible(False)
        self._set_font()

    def log(self, type, text):
        prefix = '[%s %s] ' % (time.strftime('%X'), type)
        text = re.compile('^', re.MULTILINE).sub(prefix, text)
        text = re.sub('[\r\n]*$', '\r\n', text)
        buffer = self.get_buffer()
        buffer.place_cursor(buffer.get_end_iter())
        buffer.insert_at_cursor(text)

    def _set_font(self):
        desc = pango.FontDescription()
        desc.set_family('Mono')
        self.modify_font(desc)
