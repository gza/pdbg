<?php
/**
 * PDbg, A DBGp debugger client
 * Copyright (C) 2008, Christopher Utz <cutz@chrisutz.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */

/**
 * @see Pdbg_Net_Dbgp_EngineResponse
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse.php';

/**
 * Tests for Pdbg_Net_Dbgp_EngineResponse
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponseTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test to ensure that constructing an instance with an xml string
     * works as expected.
     *
     * @return void
     */
    public function testConstruct()
    {
        $xml  = '<?xml version="1.0"?><x></x>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse($xml);

        $this->assertEquals('x', $resp->getDocument()->documentElement->nodeName);
    }

    /**
     * Test to ensure that the getXml method works as expected.
     *
     * @return void
     */
    public function testGetXml()
    {
        $xml  = '<?xml version="1.0"?><x></x>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse($xml);
        $out  = $resp->getXml();

        $this->assertRegExp('/^<\?xml/', $out);
    }

    /**
     * Test to ensure that the getTransactionId method works as expected.
     *
     * @return void
     */
    public function testGetTransactionId()
    {
        $xml  = '<?xml version="1.0"?><response transaction_id="2"/>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse($xml);

        $this->assertEquals('2', $resp->getTransactionId());
    }

    /**
     * Test to ensure that the expected exception is thrown when
     * trying to get a non-existent transaction id.
     *
     * @expectedException Pdbg_Net_Dbgp_EngineResponse_Exception
     * @return void
     */
    public function testGetTransactionIdInvalid()
    {
        $xml  = '<?xml version="1.0"?><x></x>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse($xml);

        $resp->getTransactionId();
    }

    /**
     * Test to ensure that the getCommandFromDocument method works.
     *
     * @return void
     */
    public function testGetCommandFromDocument()
    {
        $dom = new DOMDocument();
        $dom->loadXML('<?xml version="1.0"?><response command="x"/>');

        $cmd = Pdbg_Net_Dbgp_EngineResponse::getCommandFromDocument($dom);
        $this->assertEquals('x', $cmd);
    }

    /**
     * Test to ensure that the expected exception is thrown when
     * trying to get a non-existent command.
     *
     * @expectedException Pdbg_Net_Dbgp_EngineResponse_Exception
     * @return void
     */
    public function testGetCommandFromDocumentInvalid()
    {
        $dom = new DOMDocument();
        $dom->loadXML('<?xml version="1.0"?><response/>');

        Pdbg_Net_Dbgp_EngineResponse::getCommandFromDocument($dom);
    }

    /**
     * Test to ensure that the getCommand method works.
     *
     * @return void
     */
    public function testGetCommand()
    {
        $xml  = '<?xml version="1.0"?><response command="x"/>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse($xml);

        $this->assertEquals('x', $resp->getCommand());
    }

    /**
     * Data provider for testCommandSuccessfulFromDocument.
     *
     * @return array
     */
    public static function providerCommandSuccessfulFromDocument()
    {
        return array(
            array('1', true),
            array('0', false)
        );
    }

    /**
     * Test to ensure that the commandSuccessfulFromDocument method works.
     *
     * @param string $xmlValue
     * @param boolean $result
     * @return void
     * @dataProvider providerCommandSuccessfulFromDocument
     */
    public function testCommandSuccessfulFromDocument($xmlValue, $result)
    {
        $dom = new DOMDocument();
        $dom->loadXML('<?xml version="1.0"?><response success="'.$xmlValue.'" />');

        $r = Pdbg_Net_Dbgp_EngineResponse::commandSuccessfulFromDocument($dom);
        $this->assertEquals($result, $r);
    }

    /**
     * Test to ensure that the commandSuccessful method works when no success
     * attribute is present.
     *
     * @return void
     */
    public function testCommandSuccessfulFromDocumentNoAttr()
    {
        $dom = new DOMDocument();
        $dom->loadXML('<?xml version="1.0"?><response/>');

        $r = Pdbg_Net_Dbgp_EngineResponse::commandSuccessfulFromDocument($dom);
        $this->assertFalse($r);
    }

    /**
     * Test to ensure that the commandSuccessful method works.
     *
     * @return void
     */
    public function testCommandSuccessful()
    {
        $xml  = '<?xml version="1.0"?><response success="1"/>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse($xml);

        $this->assertTrue($resp->commandSuccessful());
    }
}
