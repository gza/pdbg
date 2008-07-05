# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Parse and represent DBGp debugger engine responses."""

__version__ = "$Id$"

from lxml import etree
from StringIO import StringIO

_response_namespaces = {
    'dp': 'urn:debugger_protocol_v1',
}

class EngineResponseException(Exception):
    """Thrown by the EngineResponse class on error."""
    pass

class EngineResponse:

    def __init__(self, xml):
        """Construct an instance."""
        self._xml_root = etree.fromstring(xml)

    @property
    def xml(self):
        """Return the engine response XML.
        
        The returned XML contains an XML declaration with encoding=ASCII (non-
        ascii characters are represented using character entities).
        """
        return etree.tostring(self._xml_root, xml_declaration=True)

    @property
    def transaction_id(self):
        """Return the unique id of the command that triggered this response."""
        return int(self.get_xpath_value('/dp:response/@transaction_id'))

    @property
    def successful(self):
        """Return True if the command was successful, False otherwise."""
        return len(self.xpath('/dp:response/dp:error')) == 0

    @property
    def error_code(self):
        """Return the integer error code of a failing command.

        Call the successful method to check if the command actually failed 
        before using this method.
        """
        return int(self.get_xpath_value('/dp:response/dp:error/@code'))

    def xpath(self, query):
        """Execute an XPath query on the response XML root."""
        return self._xml_root.xpath(query, _response_namespaces)

    def get_xpath_value(self, query):
        """Returns the string value of the first result of an XPath query."""
        result = self.xpath(query)
        if len(result) == 0:
            raise EngineResponseException, \
                "XPath query %s returned no results." % (query,)
        else:
            if isinstance(result[0], str):
                return result[0]
            else:
                return result[0].text

BUILDING_RESPONSE_AMOUNT = 0
BUILDING_RESPONSE_DATA   = 1
RESPONSE_BUILT = 2

class EngineResponseBuilder:

    """Build an EngineResponse instance from debugger engine data.

    Debugger engines send responses in the following format:

    DATA_LENGTH<NULL>DATA<NULL>

    This class expects data of the above format passed into its add_data 
    method. When a complete response is received, the get_response method
    will return an instance instead of None.
    """
    
    def __init__(self):
        """Constructs an instance."""
        self._state = BUILDING_RESPONSE_AMOUNT
        self._data_length = 0
        self._data_buffer = StringIO()

    @property
    def request_amount(self):
        """Returns the maximum amount of data to be passed into add_data.
        
        Call this method when reading from a socket to find out how much data
        should be supplied to the next add_data call.
        """
        if self._state == BUILDING_RESPONSE_AMOUNT:
            return 1
        else:
            data_len = len(self._data_buffer.getvalue())
            return 1 + self._data_length - data_len

    def add_data(self, data):
        """Add data to the buffer.
        
        Data passed into this method is accumlated and used to instantiate a
        EngineResponse object when all data has been added.
        """
        if len(data) == 0:
            return
        if self._state == BUILDING_RESPONSE_AMOUNT:
            if data[0] == "\x00":
                self._data_length = int(self._data_buffer.getvalue())
                self._data_buffer = StringIO()
                self._state = BUILDING_RESPONSE_DATA
            else:
                self._data_buffer.write(data[0])
        else:
            if data[-1] == "\x00":
                self._data_buffer.write(data[:-1])
                self._state = RESPONSE_BUILT
            else:
                self._data_buffer.write(data)
    
    def get_response(self):
        """Return a response object if all data has been received."""
        if self._state == RESPONSE_BUILT:
            return EngineResponse(self._data_buffer.getvalue())
        else:
            return None
