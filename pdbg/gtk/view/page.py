# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
from base import View, widget

def _build_tab_label(info):
    label = '[' + info['remote_ip'] + ']'
    if info.has_key('engine'):
        label += ' ' + info['engine']
    if info.has_key('engine_version'):
        label += ' ' + info['engine_version']
    return label

class PageView(View):

    def __init__(self, connection_info):
        self._connection_info = connection_info
        super(PageView, self).__init__()

    @widget
    def _tab_label(self):
        return gtk.Label('XXX')

    @widget
    def _outer_box(self):
        box = gtk.HPaned()
        box.pack1(gtk.Label('LEFT'), False, False)
        box.pack2(gtk.Label('RIGHT'), True, False)
        return box

    def _setup(self):
        self._tab_label()
        self._outer_box()
