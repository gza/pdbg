# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

from select import select
import socket
import errno

class SocketWrapperException(Exception):
    pass

class SocketWrapper:

    def __init__(self, socket):
        self._socket = socket
        self._closed = False

    @property
    def handle(self):
        return self._socket

    def send_all(self, data):
        return self._socket.sendall(data)

    def recv(self, buf_size):
        return self._socket.recv(buf_size)

    def is_data_available(self):
        if self._closed:
            return False
        try:
            (r, w, e) = select([self._socket], [], [], 0)
            return len(r) > 0
        except socket.error, (code, msg):
            if code == errno.EBADF:
                return False
            else:
                raise SocketWrapperException, \
                    "Socket error: %s (%s)" % (code, msg)

    def close(self):
        if not self._closed:
            self._closed = True
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
