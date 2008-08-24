# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Parse and represent DBGp debugger engine responses."""

__version__ = "$Id$"

from lxml import etree
from StringIO import StringIO
from types import ClassType
from base64 import b64decode
from logging import getLogger
import re

_DEBUGGER_PROTOCOL_NS = 'urn:debugger_protocol_v1'
_DEBUGGER_PROTOCOL = '{%s}' % _DEBUGGER_PROTOCOL_NS
_XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'
_XSI = '{%s}' % _XSI_NS
_XSD_NS = 'http://www.w3.org/2001/XMLSchema'
_XSD = '{%s}' % _XSD_NS

_response_namespaces = {
     'dp': _DEBUGGER_PROTOCOL_NS, 
    'xsi': _XSI_NS, 
    'xsd': _XSD_NS
}

_property_req_fields = [
    'name',
    'fullname',
    'type',
]

class EngineResponseException(Exception):
    """An error occurred in the EngineResponse class."""
    pass

class EngineResponseProperty(dict):

    def __init__(self, xml_node):
        self._xml_node = xml_node
        self._logger = getLogger()
        self._children = []
        self._loaded_ok = False

        self['numchildren'] = 0
        self['children'] = False

        self._load_attribs()
        if self._loaded_ok:
            self._load_value()
            self._load_children()

    def _load_attribs(self):
        attrib = self._xml_node.attrib
        for req_attrib in _property_req_fields:
            if not attrib.has_key(req_attrib):
                self._logger.warning("property missing %s: %s", req_attrib, 
                    self._xml_node)
                return
        self._loaded_ok = True
        for key in attrib.keys():
            self[key] = attrib[key]
        if self.has_key('children'):
            self['children'] = (self['children'] == '1')
        if self.has_key('numchildren'):
            self['numchildren'] = int(self['numchildren'])

    def _load_value(self):
        if self.has_key('encoding'):
            if self['encoding'] == 'base64':
                self['value'] = b64decode(self._xml_node.text)
            else:
                logger = getLogger()
                logger.warning("Invalid encoding: %s", self['encoding'])
        else:
            self['value'] = self._xml_node.text

    def _load_children(self):
        if not self['children']:
            return
        for child in self._xml_node:
            prop = EngineResponseProperty(child)
            if prop.loaded_ok:
                self._children.append(prop)

    @property
    def loaded_ok(self):
        return self._loaded_ok

    def get_children(self):
        return self._children

class TypeMapElement(object):

    def __init__(self, name, type, xsi_type=None):
        self._name = name
        self._type = type
        self._xsi_type = xsi_type

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def xsi_type(self):
        return self._xsi_type

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
        try:
            return self.get_xpath_value('/dp:response/@success') == '1'
        except Exception, e:
            return len(self.xpath('/dp:response/dp:error')) == 0

    @property
    def error_code(self):
        """Return the integer error code of a failing command.

        Call the successful method to check if the command actually failed 
        before using this method.
        """
        return int(self.get_xpath_value('/dp:response/dp:error/@code'))

    @property
    def error_msg(self):
        return self.get_xpath_value('/dp:response/dp:error/dp:message')

    def xpath(self, query):
        """Execute an XPath query on the response XML root."""
        return self._xml_root.xpath(query, namespaces=_response_namespaces)

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

class StreamResponse(EngineResponse):
    """Represent stream data sent by a debugger engine."""

    @property
    def type(self):
        """Return the stream type (stdout or stderr)."""
        return self.get_xpath_value('/dp:stream/@type')

    @property
    def data(self):
        """Return the data streamed by the debugger engine."""
        return b64decode(self.get_xpath_value('/dp:stream'))

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

class TypemapGetResponse(EngineResponse):
    """Represent a response to a typemap_get command."""

    def get_type_map(self):
        results = self.xpath('/dp:response/dp:map')
        map = []

        for result in results:
            attrib = result.attrib
            if attrib.has_key(_XSI+'type'):
                xsi_type = attrib[_XSI+'type']
            else:
                xsi_type = None
            map.append(TypeMapElement(attrib['name'], attrib['type'], xsi_type))
        return map

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
            if element_dict.has_key('lineno'):
                element_dict['lineno'] = int(element_dict['lineno'])
            if element_dict.has_key('level'):
                element_dict['level'] = int(element_dict['level'])
            elements.append(element_dict)
        return elements

class BreakpointSetResponse(EngineResponse):
    """Represent a response to a breakpoint_set command."""

    @property
    def id(self):
        """Return the id of the breakpoint."""
        return self.get_xpath_value('/dp:response/@id')

class BreakpointRemoveResponse(EngineResponse):
    """Represent a response to a breakpoint_remove command."""

class ContextNamesResponse(EngineResponse):
    """Represent a response to a context_names command."""

    def get_names(self):
        """Return a list of context names and their ids"""
        xpath_results = self.xpath('/dp:response/dp:context')
        ret = []
        for xpath_result in xpath_results:
            attrib = xpath_result.attrib
            if not attrib.has_key('name') or not attrib.has_key('id'):
                raise EngineResponseException('Invalid context element')
            ret.append((attrib['name'], attrib['id']))
        return ret

class ContextGetResponse(EngineResponse):
    """Represent a response to a context_get command."""

    def get_properties(self):
        """Return a list of properties in the context"""
        query_results = self.xpath('/dp:response/dp:property')
        props = []
        for prop_node in query_results:
            prop = EngineResponseProperty(prop_node)
            if prop.loaded_ok:
                props.append(prop)
        return props

class PropertyGetResponse(EngineResponse):
    """Represent a response to a property_get command."""

    def get_property(self):
        """Return properties of a property"""
        query_results = self.xpath('/dp:response/dp:property')
        props = []
        if len(query_results) > 0:
            prop = EngineResponseProperty(query_results[0])
            if prop.loaded_ok:
                return prop
        return None

class PropertySetResponse(EngineResponse):
    """Represent a response to a property_set command."""

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
    elif response.xpath('/dp:stream'):
        return StreamResponse(response.xml_root)
    if not response.successful:
        return response
    class_name = _command_to_class_name(response.command)
    gbls = globals()
    if gbls.has_key(class_name):
        klass = gbls[class_name]
        if isinstance(klass, type):
            return klass(response.xml_root)
    return response
