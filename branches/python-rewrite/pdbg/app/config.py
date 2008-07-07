# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

import os.path

class Config:

    _config = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(klass):
        if klass._config == None:
            klass._config = klass()
        return klass._config

    @property
    def app_dir(self):
        d = os.path.dirname
        return d(d(d(__file__)))

    @property
    def asset_dir(self):
        return os.path.join(self.app_dir, 'assets')
