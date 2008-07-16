# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Parse and represent DBGp debugger engine responses."""

__version__ = "$Id$"

from lxml import etree
from StringIO import StringIO
from types import ClassType
from base64 import b64decode
import re

_response_namespaces = {
    'dp': 'urn:debugger_protocol_v1',
}

class EngineResponseException(Exception):
    """An error occurred in the EngineResponse class."""
    pass

class EngineResponse(object):

    def __init__(self, xml):
        """Construct an instance.
        
        The xml parameter can be either an XML string or an lxml Element.
        """
        if not isinstance(xml, str):
            self._xml_root = xml
        else:
            self._xml_root = etree.fromstring(xml)

    @property
    def xml(self):
        """Return the engine response XML.
        
        The returned XML contains an XML declaration with encoding=ASCII (non-
        ascii characters are represented using character entities).
        """
        return etree.tostring(self._xml_root, xml_declaration=True)

    @property
    def xml_root(self):
        """Return the lxml root Element."""
        return self._xml_root

    @property
    def transaction_id(self):
        """Return the unique id of the command that triggered this response."""
        return int(self.get_xpath_value('/dp:response/@transaction_id'))

    @property
    def command(self):
        return self.get_xpath_value('/dp:response/@command')

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

    def __str__(self):
        """Return a printable string representation of the instance."""
        return self.xml

class InitResponse(EngineResponse):
    """Represent the initial packet sent by a debugger engine."""

    @property
    def file_uri(self):
        """Return the uri of the script file being debugged."""
        return self.get_xpath_value('/dp:init/@fileuri')

    def get_engine_info(self):
        """Return information about the debugger engine.

        The information returned depends on the debugger engine 
        implementation.
        """
        info  = {}
        nodes = self.xpath('/dp:init/*')
        for node in nodes:
            # Remove the namespace from the tag name.
            info_type = re.sub('^\{.*\}', '', node.tag)
            info[info_type] = node.text
            for (key, value) in node.attrib.items():
                info[info_type+'_'+key] = value
        return info

class StatusResponse(EngineResponse):
    """Represent a response to a status command."""

    @property
    def status(self):
        """Return the status of the debugger engine.

        Value will be one of: starting, stopping, stopped, running, break.
        """
        return self.get_xpath_value('/dp:response/@status')

    @property
    def reason(self):
        """Return the status reason of the debugger engine.

        Value will be one of: ok, error, abort, exception.
        """
        return self.get_xpath_value('/dp:response/@reason')

class SourceResponse(EngineResponse):
    """Represent a response to a source command."""

    @property
    def source(self):
        """Return the source code of the requested script file."""
        return b64decode(self.get_xpath_value('/dp:response'))

class StackGetResponse(EngineResponse):
    """Represent a response to a stack_get command."""

    def get_stack_elements(self):
        """Return a list of stack elements.

        Each element of the list is a dict object, with properties such as 
        level, type, and filename.
        """
        results = self.xpath('/dp:response/dp:stack')
        elements = []
        for result in results:
            element_dict = {}
            element_dict.update(result.attrib)
            elements.append(element_dict)
        return elements

BUILDING_RESPONSE_AMOUNT = 0
BUILDING_RESPONSE_DATA   = 1
RESPONSE_BUILT = 2

class EngineResponseBuilder(object):

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
                self._data_buffer.close()
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
            data = self._data_buffer.getvalue()
            self._state = BUILDING_RESPONSE_AMOUNT
            self._data_length = 0
            self._data_buffer.close()
            self._data_buffer = StringIO()
            return factory(data)
        else:
            return None

def _underscore_to_caps(s):
    return re.sub('(^|_)([a-z])', lambda m: m.group(2).upper(), s)

def _command_to_class_name(command):
    status_cmds = ('run', 'step_into', 'step_over', 'step_out', 
        'stop', 'detach')
    if command in status_cmds:
        return 'StatusResponse'
    else:
        return _underscore_to_caps(command) + 'Response'

def factory(xml):
    """Instantiate an EngineResponse subclass given an xml string."""
    response = EngineResponse(xml)
    if response.xpath('/dp:init'):
        return InitResponse(response.xml_root)
    if not response.successful:
        return response
    class_name = _command_to_class_name(response.command)
    gbls = globals()
    if gbls.has_key(class_name):
        klass = gbls[class_name]
        if isinstance(klass, type):
            return klass(response.xml_root)
    return response
