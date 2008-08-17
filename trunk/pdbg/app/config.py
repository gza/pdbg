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
            'logging_level': 10,
            'win_width': 800,
            'win_height': 600,
            'current_line_background': '#444466',
            'current_line_foreground': '#ffffff',
            'style_scheme': 'classic',
            'app_title': 'pDBG - v0.1',
            'app_dir': app_dir,
            'asset_dir': asset_dir,
            'listener_timeout_ms': 100
        })

    def get_image_path(self, name):
        return os.path.join(self['asset_dir'], name + '.png')
