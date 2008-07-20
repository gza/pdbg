# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

from select import select
import socket

class SocketWrapper:

    def __init__(self, socket):
        self._socket = socket

    @property
    def handle(self):
        return self._socket

    def send_all(self, data):
        return self._socket.sendall(data)

    def recv(self, buf_size):
        return self._socket.recv(buf_size)

    def is_data_available(self):
        (r, w, e) = select([self._socket], [], [], 0)
        return len(r) > 0

    def close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
