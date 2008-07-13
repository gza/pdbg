# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
from base import View, widget
from ..widget.textlog import TextLog

def _build_tab_label(info):
    label = '[' + info['remote_ip'] + ']'
    if info.has_key('engine'):
        label += ' ' + info['engine']
    if info.has_key('engine_version'):
        label += ' ' + info['engine_version']
    return label

class PageView(View):

    def set_connection_info(self, conn_info):
        self['tab_label'].set_text(_build_tab_label(conn_info))

    @widget
    def _tab_label(self):
        return gtk.Label('')

    @widget
    def _log(self):
        log = TextLog()
        return log

    @widget
    def _log_scroll(self):
        scroll = gtk.ScrolledWindow()
        scroll.add(self._log())
        return scroll

    @widget
    def _notebook(self):
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_BOTTOM)
        notebook.append_page(self._log_scroll(), gtk.Label('Log'))
        # Set the minimum requested size
        notebook.set_size_request(-1, 200)
        return notebook

    @widget
    def _inner_box(self):
        box = gtk.VPaned()
        box.pack1(gtk.Label('TOP'), True, False)
        box.pack2(self._notebook(), False, False)
        return box

    @widget
    def _outer_box(self):
        box = gtk.HPaned()
        box.pack1(gtk.Label('LEFT'), False, False)
        box.pack2(self._inner_box(), True, False)
        return box

    def _setup(self):
        self._tab_label()
        self._outer_box()
