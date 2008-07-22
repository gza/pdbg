# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import gtksourceview2 as gtksourceview
import pango
import time
import re

def _get_language_for_mime_type(mime):
    lang_manager = gtksourceview.language_manager_get_default()
    lang_ids = lang_manager.get_language_ids()
    for i in lang_ids:
        lang = lang_manager.get_language(i)
        for m in lang.get_mime_types():
            if m == mime:
                return lang
    return None

class SourceView(gtksourceview.View):

    def __init__(self):
        gtksourceview.View.__init__(self)

        self._current_line = None

        lang_mgr = gtksourceview.LanguageManager()
        php_lang = _get_language_for_mime_type('application/x-php')

        buffer = gtksourceview.Buffer()
        buffer.set_language(php_lang)
        buffer.set_highlight_syntax(True)

        mgr = gtksourceview.style_scheme_manager_get_default()
        style_scheme = mgr.get_scheme('classic')
        if style_scheme:
            buffer.set_style_scheme(style_scheme)

        self.set_show_line_numbers(True)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_buffer(buffer)
        self._set_font()
        self._add_tags()

    def set_current_line(self, line_num):
        self.unset_current_line()
        buffer = self.get_buffer()
        buffer.apply_tag_by_name('current_line', *self._get_line_iters(line_num))
        self._current_line = line_num

    def unset_current_line(self):
        if self._current_line != None:
            (iter1, iter2) = self._get_line_iters(self._current_line)
            buffer = self.get_buffer()
            buffer.remove_tag_by_name('current_line', iter1, iter2)
        self._current_line = None


    def _get_line_iters(self, line_num):
        buffer = self.get_buffer()
        iter1 = buffer.get_iter_at_line(line_num)
        iter2 = iter1.copy()
        iter2.forward_line()
        return (iter1, iter2)

    def _add_tags(self):
        tag = gtk.TextTag('current_line')
        tag.set_property('foreground', '#ffffff')
        tag.set_property('foreground-set', True)
        tag.set_property('paragraph-background', '#444466')
        tag.set_property('paragraph-background-set', True)
        self.get_buffer().get_tag_table().add(tag)

    def _set_font(self):
        desc = pango.FontDescription()
        desc.set_family('Mono')
        self.modify_font(desc)
