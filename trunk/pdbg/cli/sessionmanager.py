# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

from pdbg.app.patterns import *

class SessionManager(dict, Singleton):

    def __init__(self):
        super(SessionManager, self).__init__()

    def reset(self):
        self.update({
            'base_uri': None,

            'status': None,
            'reason': None,

            'file_uri': None,
            'line_num': None,

            'queue': [],

            'list_size': 10,
            'list_b': None,
            'list_e': None
        })

    def can_continue(self):
        return self['status'] not in ('stopping', 'stopped')

    def append_base_uri(self, uri):
        if self['base_uri'] != None:
            return self['base_uri'].rstrip('/') + '/' + uri.lstrip('/')
        else:
            return uri

    def input(self, prompt):
        if len(self['queue']) > 0:
            value = self['queue'][0]
            del self['queue'][0]
            return value
        else:
            return raw_input(prompt)

    def get(self, key, default=None):
        if self.has_key(key):
            return self[key]
        else:
            return default
