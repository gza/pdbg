# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: Document"""

__version__ = "$Id$"

from ..patterns import Manager, Singleton
from ...dbgp.socketwrapper import SocketWrapper
from ...dbgp.connectionlistener import ConnectionListener

class ListenerManager(Manager, Singleton):

    def __init__(self):
        super(Manager, self).__init__()
        self.register_event('new_connection')

    @property
    def listener(self):
        return self._listener

    def setup(self):
        self._listener = ConnectionListener(SocketWrapper) 

    def accept_connection(self):
        connection = self._listener.accept()
        if connection != None:
            self.fire('new_connection', connection)
            return connection
        return None
