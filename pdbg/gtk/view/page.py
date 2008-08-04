# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

import gtk
import re
from base import View, widget
from ..widget.textlog import TextLog
from ..widget.sourceview import SourceView
from ..widget.sourcelist import SourceList

def _build_tab_label(info):
    label = '[' + info['remote_ip'] + ']'
    if info.has_key('engine'):
        label += ' ' + info['engine']
    if info.has_key('engine_version'):
        label += ' ' + info['engine_version']
    return label

class PageView(View):

    def append_page_on_init(self, conn_info, notebook):
        self['tab_label'].set_text(_build_tab_label(conn_info))
        return notebook.append_page_with_button(
            self['outer_box'], 
            self['tab_label'],
            self['tab_button'])

    def remove_stderr_page(self):
        num = self['notebook'].page_num(self['stderr_scroll'])
        if num != None:
            self['notebook'].remove_page(num)

    def update_source(self, source):
        source_view = self['source_view']
        source_view.current_source = source

        model = self['source_list'].get_model()
        if not model.has_source(source):
            model.add_source(source)

        source_view.refresh_current_line()

        self['uri_entry'].set_text(source.file_uri)

    def get_file_uri_from_list_path(self, path):
        return self['source_list'].get_model().get_file_uri_from_path(path)

    @widget
    def _source_list(self):
        source_list = SourceList()
        return source_list

    @widget
    def _source_list_scroll(self):
        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(self._source_list())
        return scroll

    @widget
    def _tab_label(self):
        return gtk.Label('')

    @widget
    def _tab_button(self):
        button = gtk.Button()
        button.set_relief(gtk.RELIEF_NONE)

        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        button.set_image(img)

        return button

    @widget
    def _uri_entry_label(self):
        label = gtk.Label()
        label.set_text_with_mnemonic(_('Remote _URI:'))
        return label

    @widget
    def _uri_entry(self):
        return gtk.Entry()

    @widget
    def _get_uri_button(self):
        button = gtk.Button(_('Request File'))
        button.set_tooltip_text(_('Request a file from the debugger engine'))
        
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU)
        button.set_image(img)

        return button

    @widget
    def _open_uri_box(self):
        box = gtk.HBox()
        box.pack_start(self._uri_entry_label(), False, False, 2)
        box.pack_start(self._uri_entry(), True, True)

        box.pack_start(self._get_uri_button(), False, False)
        self['uri_entry_label'].set_mnemonic_widget(self['uri_entry'])
        return box

    @widget
    def _source_view(self):
        return SourceView()

    @widget
    def _source_scroll(self):
        scroll = gtk.ScrolledWindow()
        scroll.add(self._source_view())
        return scroll

    @widget
    def _source_frame(self):
        frame = gtk.Frame()
        frame.add(self._source_scroll())
        frame.set_shadow_type(gtk.SHADOW_IN)
        return frame

    @widget
    def _source_box(self):
        box = gtk.VBox()
        box.pack_start(self._open_uri_box(), False, False)
        box.pack_start(self._source_frame(), True, True)
        return box

    @widget
    def _stderr(self):
        return TextLog()

    @widget
    def _stderr_scroll(self):
        scroll = gtk.ScrolledWindow()
        scroll.add(self._stderr())
        return scroll

    @widget
    def _stdout(self):
        return TextLog()

    @widget
    def _stdout_scroll(self):
        scroll = gtk.ScrolledWindow()
        scroll.add(self._stdout())
        return scroll

    @widget
    def _log(self):
        return TextLog()

    @widget
    def _log_scroll(self):
        scroll = gtk.ScrolledWindow()
        scroll.add(self._log())
        return scroll

    @widget
    def _notebook(self):
        comm_label = gtk.Label(_('Communication Log'))
        stdout_label = gtk.Label(_('Standard Out'))
        stderr_label = gtk.Label(_('Standard Error'))

        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_BOTTOM)
        notebook.append_page(self._log_scroll(), comm_label)
        notebook.append_page(self._stdout_scroll(), stdout_label)
        notebook.append_page(self._stderr_scroll(), stderr_label)
        # Set the minimum requested size
        notebook.set_size_request(-1, 200)
        return notebook

    @widget
    def _inner_box(self):
        box = gtk.VPaned()
        box.pack1(self._source_box(), True, False)
        box.pack2(self._notebook(), False, False)
        return box

    @widget
    def _outer_box(self):
        box = gtk.HPaned()
        box.pack1(self._source_list_scroll(), False, False)
        box.pack2(self._inner_box(), True, False)
        box.set_position(200)
        return box

    def _setup(self):
        self._tab_label()
        self._tab_button()
        self._outer_box()
