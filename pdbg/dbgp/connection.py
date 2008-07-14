# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Manage connections to DBGp debugger engines."""

__version__ = "$Id$"

from idecommand import IdeCommand, build
from engineresponse import EngineResponseBuilder

class ConnectionClosed(Exception):
    """The connection was closed by the debugger engine.
    
    This exception is raised when the connection is unexpectedly closed by the
    debugger engine.
    """
    pass

class Connection(object):
    """Manage a socket-based connection to a debugger engine.
    
    The socket object managed by this class is expected to be an instance of a
    class that wraps a socket object from socket module. The wrapper class 
    needs to provide the following methods:

    is_data_available -- Can data be read from the socket without blocking?
    recv -- Equivalent to the socket recv method.
    send_all -- Equivalent to the socket sendall method.
    """

    def __init__(self, socket):
        """Construct an instance.

        See the class description for details about the socket object.
        """
        self._socket = socket
        self._builder = EngineResponseBuilder()

    @property
    def socket(self):
        """Return the socket object."""
        return self._socket

    def send_command(self, command, arguments=[], data=None):
        """Send an ide command to a debugger engine.
        
        The command parameter can be an IdeCommand class instance, in which
        case the arguments and data parameters are ignored.
        """
        if isinstance(command, IdeCommand):
            command_obj = command
        else:
            command_obj = IdeCommand(command, arguments, data)
        self._socket.send_all(command_obj.build())
        return command_obj

    def recv_response(self):
        """Receive a response from a debugger engine.

        The return value is an EngineResponse object or an instance of a 
        subclass of EngineResponse. If a response is not yet available, None
        is returned.
        """
        if not self._socket.is_data_available():
            return None
        while self._socket.is_data_available():
            data = self._socket.recv(self._builder.request_amount)
            if data == '':
                raise ConnectionClosed("connection closed by debugger engine")
            self._builder.add_data(data)
            response = self._builder.get_response()
            if response != None:
                return response
        return None
