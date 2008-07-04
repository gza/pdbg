# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Parse and represent DBGp debugger engine responses."""

__version__ = "$Id$"

from lxml import etree

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
