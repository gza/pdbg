# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: Replace scaffolding."""

__version__ = "$Id$"

import os.path
import inspect
from patterns import Singleton

class Config(dict, Singleton):

    def __init__(self):
        d = os.path.dirname
        app_dir = d(d(d(os.path.abspath(__file__))))
        asset_dir = os.path.join(app_dir, 'assets')

        self.update({
            'win_width': 800,
            'win_height': 600,
            'app_title': 'pDBG - A DBGp Debugger Frontend (v0.0)',
            'app_dir': app_dir,
            'asset_dir': asset_dir
        })

    def get_image_path(self, name):
        return os.path.join(self['asset_dir'], name + '.png')
