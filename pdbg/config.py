# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

from os.path import dirname

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
    def asset_directory(self):
        return dirname(dirname(__file__))
