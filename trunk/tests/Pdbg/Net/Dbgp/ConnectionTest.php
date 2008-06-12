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
 * @see Pdbg_Net_Dbgp_Connection
 */
require_once 'Pdbg/Net/Dbgp/Connection.php';

/**
 * @see Pdbg_Net_Socket_ReadMock
 */
require_once 'Pdbg/Net/Socket/ReadMock.php';

/**
 * @see Pdbg_Net_Socket_WriteMock
 */
require_once 'Pdbg/Net/Socket/WriteMock.php';

/**
 * Tests for Pdbg_Net_Dbgp_Connection
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_ConnectionTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test the writeCommand method.
     *
     * @return void
     */
    public function testWriteCommand()
    {
        $socket = new Pdbg_Net_Socket_WriteMock();
        $conn   = new Pdbg_Net_Dbgp_Connection($socket);
        $cmd    = new Pdbg_Net_Dbgp_IdeCommand('status');

        $conn->writeCommand($cmd);

        $this->assertEquals("status\x00", $socket->getDataWritten());
    }

    /**
     * Test to ensure that readResponse behaves correctly when no data is
     * available.
     *
     * @return void
     */
    public function testReadResponseNoData()
    {
        $socket = new Pdbg_Net_Socket_ReadMock('');
        $conn   = new Pdbg_Net_Dbgp_Connection($socket);
        $resp   = $conn->readResponse();

        $this->assertEquals(null, $resp);
    }

    /**
     * Test to ensure that responses are read correctly.
     *
     * @return void
     */
    public function testReadResponse()
    {
        $data   = "34\x00<?xml version=\"1.0\"?><root></root>\x00";
        $socket = new Pdbg_Net_Socket_ReadMock($data);
        $conn   = new Pdbg_Net_Dbgp_Connection($socket);
        $resp   = $conn->readResponse();

        $this->assertType('Pdbg_Net_Dbgp_EngineResponse', $resp);
        $this->assertEquals('root', $resp->getDocument()->documentElement->nodeName);
    }

    /**
     * Test to ensure that the boundaries between responses are handled 
     * correctly.
     *
     * @return void
     */
    public function testReadTwoResponses()
    {
        $data   = "34\x00<?xml version=\"1.0\"?><root></root>\x00";
        $data  .= "28\x00<?xml version=\"1.0\"?><a></a>\x00";

        $socket = new Pdbg_Net_Socket_ReadMock($data);
        $conn   = new Pdbg_Net_Dbgp_Connection($socket);
        $resp   = $conn->readResponse();

        $this->assertType('Pdbg_Net_Dbgp_EngineResponse', $resp);
        $this->assertEquals('root', $resp->getDocument()->documentElement->nodeName);

        $resp = $conn->readResponse();

        $this->assertType('Pdbg_Net_Dbgp_EngineResponse', $resp);
        $this->assertEquals('a', $resp->getDocument()->documentElement->nodeName);
    }
}
