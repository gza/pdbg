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

_typemap_get_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
          command="typemap_get" 
          transaction_id="2">
  <map name="bool" 
       type="bool" 
       xsi:type="xsd:boolean" />
  <map name="int" 
       type="int" 
       xsi:type="xsd:decimal" />
  <map name="float" 
       type="float" 
       xsi:type="xsd:double" />
  <map name="string" 
       type="string" 
       xsi:type="xsd:string" />
  <map name="null" 
       type="null" />
  <map name="array" 
       type="hash" />
  <map name="object" 
       type="object" />
  <map name="resource" 
       type="resource" />
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

_context_names_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="context_names" 
          transaction_id="2">
  <context name="Locals" id="0"/>
  <context name="Superglobals" id="1"/>
</response>
"""

_context_get_response_xml = \
"""<?xml version="1.0" encoding="iso-8859-1"?>
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="context_get" 
          transaction_id="1" 
          context="0">
  <property name="a" 
            fullname="$a" 
            address="142182836" 
            type="object" 
            children="1" 
            classname="A" 
            numchildren="1">
    <property name="x" 
              fullname="$a-&gt;x" 
              facet="public" 
              address="142184784" 
              type="array" 
              children="1" 
              numchildren="3" />
  </property>
  <property name="x" 
            fullname="$x" 
            address="142184296" 
            type="string" 
            size="8" 
            encoding="base64">aGkgd29ybGQ=</property>
</response>
"""

_property_get_response_xml = \
"""
<response xmlns="urn:debugger_protocol_v1" 
          xmlns:xdebug="http://xdebug.org/dbgp/xdebug" 
          command="property_get" 
          transaction_id="17">
  <property name="$x" 
            fullname="$x" 
            address="142362792" 
            type="int">2</property>
</response>
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

class TestTypemapGetResponseClass(unittest.TestCase):
    """Test the TypemapGetResponse class."""

    def test_typemap_get(self):
        r = TypemapGetResponse(_typemap_get_xml)
        type_map = r.get_type_map()
        self.assertEqual(len(type_map), 8)
        self.assertEqual(type_map[2].name, 'float')
        self.assertEqual(type_map[2].type, 'float')
        self.assertEqual(type_map[2].xsi_type, 'xsd:double')
        self.assertEqual(type_map[4].xsi_type, None)
        self.assertEqual(type_map[5].type, 'hash')

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

class TestContextNamesResponseClass(unittest.TestCase):
    """Test the ContextNamesResponse class."""

    def test_get_names(self):
        r = ContextNamesResponse(_context_names_response_xml)
        exp_ret = [('Locals', '0'), ('Superglobals', '1')]
        self.assertEqual(r.get_names(), exp_ret)

class TestContextGetResponseClass(unittest.TestCase):
    """Test the ContextGetResponse class."""

    def test_get_properties(self):
        r = ContextGetResponse(_context_get_response_xml)
        
        props = r.get_properties()
        self.assertEqual(len(props), 2)

        self.assertEqual(props[0]['name'], 'a')
        self.assertEqual(props[0]['children'], True)
        self.assertEqual(props[0]['numchildren'], 1)

        children = props[0].get_children()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0]['name'], 'x')
        self.assertEqual(children[0]['fullname'], '$a->x')
        self.assertEqual(children[0]['numchildren'], 3)

        self.assertEqual(props[1]['name'], 'x')
        self.assertEqual(props[1]['children'], False)

        children = props[1].get_children()
        self.assertEqual(len(children), 0)

class TestPropertyGetResponseClass(unittest.TestCase):
    """Test the PropertyGetResponse class."""

    def test_get_property(self):
        r = PropertyGetResponse(_property_get_response_xml)
        prop = r.get_property()

        self.assertEqual(prop['fullname'], '$x')
        self.assertEqual(prop['value'], '2')

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
