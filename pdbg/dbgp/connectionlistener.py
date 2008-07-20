# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Listen for incoming DBGp debugger engine connections."""

__version__ = "$Id$"

from connection import Connection
import socket

class ConnectionListener(object):
    """Listen for incoming DBGp debugger engine connections."""

    def __init__(self, socket_wrapper, ip_address='127.0.0.1', port=9000):
        """ Construct an instance.

        The socket_wrapper parameter is a class the listener will wrap around
        incoming sockets.  See the socketwrapper module for an example 
        implementation.
        """
        self._socket_wrapper = socket_wrapper
        self._ip_address = ip_address
        self._port = port
        self._init_socket()

    @property
    def ip_address(self):
        """Return the ip address the listener listens on."""
        return self._ip_address

    @property
    def port(self):
        """Return the port the listener listens on."""
        return self._port

    @property
    def socket(self):
        """Return the listening socket."""
        return self._socket

    def _init_socket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The setsockopt below prevents address already in use errors.
        # See http://www.unixguide.net/network/socketfaq/4.5.shtml
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._ip_address, self._port))
        # The parameter to listen is the max. number of connections that will
        # be backlogged. According to the python docs, this should not be more
        # than five.
        self._socket.listen(5)
        self._socket.setblocking(0)

    def accept(self):
        """Accept an incoming connection.

        Returns a Connection object if a connection was pending. Returns None
        if no connection was pending. This method does not block.
        """
        try:
            (in_s, remote_addr) = self._socket.accept()
            return Connection(self._socket_wrapper(in_s))
        except socket.error, (errno, msg):
            if errno == 11:
                # No connection was pending ... return None
                return None
            else:
                # An error occurred. Boo!
                raise ConnectionListenerException, \
                    "Error occurred on accept: %s (%s)" % (errno, msg)
