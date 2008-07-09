# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Build DBGp protocol ide command strings."""

__version__ = "$Id$"

from base64 import b64encode

_next_trans_id = 1

def allocate_transaction_id():
    """Allocate and return a unique transaction id."""
    global _next_trans_id
    result_id = _next_trans_id
    _next_trans_id = _next_trans_id + 1
    return result_id

def build(name, arguments=[], data=None, append_null=True):
    """Build an ide command string using the specified parameters.
    
    Invoking this function is equivalent to creating an IdeCommand instance and
    calling its build method.
    """
    command = IdeCommand(name, arguments, data)
    return command.build(append_null)

class IdeCommand(object):

    """Represent a DBGp protocol IDE command.
    
    Call the build method to get a string representation suitable for 
    transmitting to a debugger engine.
    """

    def __init__(self, name, arguments=[], data=None):
        """Construct an instance."""
        self._name = name
        if isinstance(arguments, dict):
            self._arguments = arguments.items()
        else:
            self._arguments = list(arguments)
        self._data = data
        if self.has_argument("-i"):
            self._trans_id = int(self.get_argument("-i"))
        else:
            self._trans_id = allocate_transaction_id()
            self._arguments.append(("-i", self._trans_id))

    def has_argument(self, argument):
        """Return True if the argument exists, False otherwise."""
        for (name, value) in self._arguments:
            if name == argument:
                return True
        return False

    def get_argument(self, argument):
        """Return the value of the specified argument."""
        for (name, value) in self._arguments:
            if name == argument:
                return value
        raise LookupError, "argument %s not found" % (argument)

    @property
    def name(self):
        """Return the command name."""
        return self._name
    @property
    def arguments(self):
        """Return the argument list."""
        return list(self._arguments)
    @property
    def data(self):
        """Return the command data."""
        return self._data
    @property
    def transaction_id(self):
        """Return the transaction id."""
        return self._trans_id

    def build(self, append_null=True):
        """Return a string representation of the instance.

        If append_null is True, the string returned is suitable to be sent to a
        debugger engine.  Use append_null=False to get a printable 
        representation.
        """
        spacify   = lambda x: str(x[0]) + ' ' + str(x[1])
        cmd_parts = [self._name] + map(spacify, self._arguments)
        if self._data != None:
            cmd_parts.append('--')
            cmd_parts.append(b64encode(self._data))
        result = ' '.join(cmd_parts)
        if append_null:
            result = result + "\x00"
        return result

    def __str__(self):
        """Return a printable string representation of the instance."""
        return self.build(False)
