# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: Replace scaffolding."""

__version__ = "$Id$"

import os.path
import inspect
from patterns import Singleton

class Config(dict, Singleton):

    def __init__(self):
        self.update({
            'timeout_interval': 400
        })

    def __getitem__(self, key):
        method_name = '_prop_' + str(key)
        all_methods = inspect.getmembers(self, inspect.ismethod)
        methods = [m for (n, m) in all_methods if n == method_name]
        if len(methods) > 0:
            return methods[0]()
        else:
            return dict.__getitem__(self, key)

    def _prop_app_dir(self):
        d = os.path.dirname
        return d(d(d(os.path.abspath(__file__))))

    def _prop_asset_dir(self):
        return os.path.join(self['app_dir'], 'assets')
