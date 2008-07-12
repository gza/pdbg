# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

def widget(fn):
    def store(self, *arguments, **keywords):
        name = fn.__name__[1:]
        self[name] = fn(self, *arguments, **keywords)
        return self[name]
    return store

class View(dict):

    def __init__(self):
        self._setup()

    def _setup(self):
        pass
