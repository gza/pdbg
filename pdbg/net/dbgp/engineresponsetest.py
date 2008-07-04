# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the engineresponse module."""

__version__ = "$Id$"

import unittest
from engineresponse import EngineResponse, EngineResponseException

_init_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<init xmlns="urn:debugger_protocol_v1" 
      xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
      fileuri="file:///home/chris/tmp/test.php" 
      language="PHP" 
      protocol_version="1.0" 
      appid="14798" 
      idekey="xdebug">
  <engine version="2.0.3"><![CDATA[Xdebug]]></engine>
  <author><![CDATA[Derick Rethans]]></author>
  <url><![CDATA[http://xdebug.org]]></url>
  <copyright><![CDATA[Copyright (c) 2002-2008 by Derick Rethans]]></copyright>
</init>
"""

_status_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="status" 
          transaction_id="1" 
          status="starting" 
          reason="ok"/>
"""

_status_error_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="status">
  <error code="3">
    <message><![CDATA[invalid or missing options]]></message>
  </error>
</response>
"""

class TestEngineResponseClass(unittest.TestCase):
    """Test the EngineResponse class."""

    def test_get_xpath_value_node_value(self):
        r = EngineResponse(_init_response_xml)
        engine = r.get_xpath_value('/dp:init/dp:engine')
        self.assertEqual(engine, 'Xdebug')

    def test_get_xpath_value_attribute(self):
        r = EngineResponse(_init_response_xml)
        engine_version = r.get_xpath_value('/dp:init/dp:engine/@version')
        self.assertEqual(engine_version, '2.0.3')

    def test_get_xpath_value_missing(self):
        r = EngineResponse(_init_response_xml)
        try:
            r.get_xpath_value('/dp:init/dp:foobar')
        except EngineResponseException:
            return
        self.fail("EngineResponseException expected")

    def test_xml(self):
        r = EngineResponse(_status_response_xml)
        self.assertEqual(r.xml[0:5], '<?xml')

    def test_transaction_id(self):
        r = EngineResponse(_status_response_xml)
        self.assertEqual(r.transaction_id, 1)

    def test_successful(self):
        r = EngineResponse(_status_response_xml)
        self.assertEqual(r.successful, True)

    def test_unsuccessful(self):
        r = EngineResponse(_status_error_xml)
        self.assertEqual(r.successful, False)

    def test_error_code(self):
        r = EngineResponse(_status_error_xml)
        self.assertEqual(r.error_code, 3)

if __name__ == '__main__':
    unittest.main()