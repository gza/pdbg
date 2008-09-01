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
            'file_uri': None,
            'line_num': None,
        })

    def can_continue(self):
        return self['status'] not in ('stopping', 'stopped')
