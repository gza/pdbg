# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import gtksourceview2 as gtksourceview
import pango
import gobject
from pdbg.app.config import Config

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
        self._current_source = None

        buffer = gtksourceview.Buffer()
        php_lang = _get_language_for_mime_type('application/x-php')
        if php_lang:
            buffer.set_language(php_lang)
        buffer.set_highlight_syntax(True)
        buffer.set_highlight_matching_brackets(False)

        config = Config.get_instance()

        mgr = gtksourceview.style_scheme_manager_get_default()
        style_scheme = mgr.get_scheme(config['style_scheme'])
        if style_scheme:
            buffer.set_style_scheme(style_scheme)

        self.set_show_line_numbers(True)
        self.set_show_line_marks(True)
        self.set_editable(False)
        self.set_cursor_visible(False)
        self.set_buffer(buffer)
        self._set_font()
        self._add_tags()
        self._add_marks()

    def refresh_breakpoints(self):
        buffer = self.get_buffer()
        buffer.remove_source_marks(*buffer.get_bounds())
        if self._current_source != None:
            breakpoints = self._current_source.get_breakpoints()
            for id in breakpoints:
                breakpoint = breakpoints[id]
                if breakpoint['line_num'] != None:
                    iter = buffer.get_iter_at_line(breakpoint['line_num'])
                    buffer.create_source_mark(None, 'breakpoint', iter)

    def refresh_current_line(self):
        current_line = self._current_source.current_line
        if current_line != None:
            self._set_current_line(current_line - 1)
        else:
            self._unset_current_line()

    def scroll_to_current_line(self, defer_scroll=False):
        if self._current_line == None:
            return
        (iter1, iter2) = self._get_line_iters(self._current_line)
        def scroll_func():
            self.scroll_to_iter(iter1, 0)
            return False
        if defer_scroll:
            # The call to scroll_to_iter needs to be deferred because the 
            # sourceview must be redrawn before the call will work if the
            # source file changed.
            gobject.idle_add(scroll_func)
        else:
            scroll_func()

    def get_iter_of_pressed_line_number(self, event):
        left_gutter = self.get_window(gtk.TEXT_WINDOW_LEFT)
        if event.window == left_gutter:
            (x_buf, y_buf) = self.window_to_buffer_coords(
                gtk.TEXT_WINDOW_LEFT, int(event.x), int(event.y))
            return self.get_line_at_y(y_buf)[0]
        else:
            return None

    def set_current_source(self, source):
        self._current_source = source
        self._unset_current_line()
        self.get_buffer().set_text(self._current_source.text)
        self.refresh_breakpoints()
        self.refresh_current_line()
        self.scroll_to_current_line(defer_scroll=True)

    def get_current_source(self):
        return self._current_source

    current_source = property(get_current_source, set_current_source)

    @property
    def current_file_uri(self):
        if self._current_source == None:
            return None
        else:
            return self._current_source.file_uri

    def _set_current_line(self, line_num):
        self._unset_current_line()
        buffer = self.get_buffer()
        (iter1, iter2) = self._get_line_iters(line_num)
        buffer.apply_tag_by_name('current_line', iter1, iter2)
        self._current_line = line_num

    def _unset_current_line(self):
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
        if iter1.get_line() == iter2.get_line():
            iter2.forward_to_end()
        return (iter1, iter2)

    def _add_tags(self):
        config = Config.get_instance()
        tag = gtk.TextTag('current_line')
        tag.set_property('foreground', config['current_line_foreground'])
        tag.set_property('foreground-set', True)
        tag.set_property('paragraph-background', \
            config['current_line_background'])
        tag.set_property('paragraph-background-set', True)
        self.get_buffer().get_tag_table().add(tag)

    def _add_marks(self):
        config = Config.get_instance()
        img = gtk.gdk.pixbuf_new_from_file(config.get_image_path('breakpoint'))
        self.set_mark_category_pixbuf('breakpoint', img)

    def _set_font(self):
        desc = pango.FontDescription()
        desc.set_family('Mono')
        self.modify_font(desc)
