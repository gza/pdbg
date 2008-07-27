# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Unit tests for the engineresponse module."""

__version__ = "$Id$"

import unittest
from StringIO import StringIO
from engineresponse import *

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

_stream_response_xml = \
"""
<stream xmlns="urn:debugger_protocol_v1" 
        xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
        type="stdout" 
        encoding="base64">Zm9v</stream>
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

_source_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="source" 
          transaction_id="1" 
          encoding="base64"><![CDATA[Zm9v]]></response>
"""

_stack_get_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="stack_get" 
          transaction_id="1">
    <stack where="{main}" 
           level="0" 
           type="file" 
           filename="file:///home/chris/tmp/test.php" 
           lineno="3" />
    <stack level="1" 
           type="file" 
           filename="file:///home/chris/tmp/test2.php" 
           lineno="3" />
</response>
"""

_breakpoint_set_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="breakpoint_set" 
          transaction_id="3" 
          id="122490001"/>
"""

_unknown_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="does_not_exist" 
          transaction_id="1" />
"""

_status_response_str = str(len(_status_response_xml)) + "\x00" + \
    _status_response_xml + "\x00"

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

    def test_xml_root(self):
        r = EngineResponse(_status_response_xml)
        self.assertEqual(r.xml_root.tag, '{urn:debugger_protocol_v1}response') 

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

class TestInitResponseClass(unittest.TestCase):
    """Test the InitResponse class."""

    def test_file_uri(self):
        r = InitResponse(_init_response_xml)
        self.assertEqual(r.file_uri, 'file:///home/chris/tmp/test.php')

    def test_get_engine_info(self):
        r = InitResponse(_init_response_xml)
        info = r.get_engine_info()
        self.assertEqual(info['engine'], 'Xdebug')
        self.assertEqual(info['engine_version'], '2.0.3')

class TestStreamResponseClass(unittest.TestCase):
    """Test the StreamResponse class."""

    def test_type(self):
        r = StreamResponse(_stream_response_xml)
        self.assertEqual(r.type, 'stdout')

    def test_get_engine_info(self):
        r = StreamResponse(_stream_response_xml)
        self.assertEqual(r.data, 'foo')

class TestStatusResponseClass(unittest.TestCase):
    """Test the StatusResponse class."""

    def test_status(self):
        r = StatusResponse(_status_response_xml)
        self.assertEqual(r.status, 'starting')

    def test_reason(self):
        r = StatusResponse(_status_response_xml)
        self.assertEqual(r.reason, 'ok')

class TestSourceResponseClass(unittest.TestCase):
    """Test the SourceResponse class."""

    def test_source(self):
        r = SourceResponse(_source_response_xml)
        self.assertEqual(r.source, 'foo')

class TestStackGetResponseClass(unittest.TestCase):
    """Test the StackGetResponse class."""

    def test_get_stack_elements(self):
        r = StackGetResponse(_stack_get_response_xml)
        stack = r.get_stack_elements()
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack[0]['where'], '{main}')
        self.assertEqual(stack[0]['lineno'], 3)
        self.assertEqual(stack[1]['level'], 1)

class TestBreakpointSetResponseClass(unittest.TestCase):
    """Test the BreakpointSetResponse class."""

    def test_id(self):
        r = BreakpointSetResponse(_breakpoint_set_response_xml)
        self.assertEqual(r.id, '122490001')

class TestEngineResponseBuilderClass(unittest.TestCase):
    """Test the EngineResponseBuilder class."""

    def _build_response(self, builder, amt_fn):
        io = StringIO(_status_response_str)
        while True:
            response = builder.get_response()
            if response != None:
                break
            builder.add_data(io.read(amt_fn(builder)))
        return response

    def test_build(self):
        builder = EngineResponseBuilder()
        r = self._build_response(builder, lambda x: x.request_amount)
        self.assertEqual(r.xml[0:5], '<?xml')
        self.assertEqual(r.successful, True)

    def test_build_by_one(self):
        builder = EngineResponseBuilder()
        r = self._build_response(builder, lambda x: 1)
        self.assertEqual(r.xml[0:5], '<?xml')
        self.assertEqual(r.successful, True)

    def test_build_twice(self):
        builder = EngineResponseBuilder()
        r = self._build_response(builder, lambda x: 1)
        self.assertEqual(r.xml[0:5], '<?xml')
        self.assertEqual(r.successful, True)
        r = self._build_response(builder, lambda x: x.request_amount)
        self.assertEqual(r.xml[0:5], '<?xml')
        self.assertEqual(r.successful, True)

class TestModuleFunctions(unittest.TestCase):
    """Test the engineresponse module functions."""

    def test_factory(self):
        r = factory(_status_response_xml)
        self.assertEqual(isinstance(r, StatusResponse), True)

    def test_factory_error(self):
        r = factory(_status_error_xml)
        self.assertEqual(r.__class__, EngineResponse)

    def test_factory_unknown(self):
        r = factory(_unknown_response_xml)
        self.assertEqual(r.__class__, EngineResponse)

    def test_factory_init(self):
        r = factory(_init_response_xml)
        self.assertEqual(isinstance(r, InitResponse), True)

if __name__ == '__main__':
    unittest.main()
