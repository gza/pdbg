# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

from os.path import dirname
from ..observable import Observable
from ..config import Config

class App(Observable):

    _app = None

    def __init__(self):
        Observable.__init__(self)

    @classmethod
    def get_instance(klass):
        if klass._app == None:
            klass._app = klass()
        return klass._app

    def _init(self):
        config = Config.get_instance()

    def run(self):
        self._init()
        #self._window.show_all()
        #gtk.main()
