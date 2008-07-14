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
 * @see Pdbg_Net_Socket
 */
require_once 'Pdbg/Net/Socket.php';

/**
 * Tests for Pdbg_Net_Socket
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_SocketTest extends PHPUnit_Framework_TestCase
{
    /**
     * @var Pdbg_Net_Socket
     */
    protected $_socket;

    /**
     * @var string
     */
    protected $_testIp = '';

    /**
     * Sets up the environment for test cases.
     *
     * @return void
     */
    public function setUp()
    {
        $sh = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        $this->_socket = new Pdbg_Net_Socket($sh);

        $this->_testIp = gethostbyname('www.google.com');
    }

    /**
     * Test to ensure that the getErrorString method works.
     *
     * @return void
     */
    public function testGetErrorString()
    {
        $this->assertEquals('Success', $this->_socket->getErrorString());
    }

    /**
     * Test to ensure that the getErrorCode method works.
     *
     * @return void
     */
    public function testGetErrorCode()
    {
        $this->assertEquals(0, $this->_socket->getErrorCode());
    }

    /**
     * Test to ensure that the writeAll method works.
     *
     * @return void
     */
    public function testWriteAll()
    {
        socket_connect($this->_socket->getHandle(), $this->_testIp, 80);

        $this->assertEquals(0, $this->_socket->getErrorCode());
        $this->_socket->writeAll("GET / HTTP/1.1\r\n\r\n");

        $response = socket_read($this->_socket->getHandle(), 12);
        $this->assertEquals('HTTP/1.1 200', $response);
    }

    /**
     * Simulates the case were socket_write does not write all the data in one
     * go, in order to ensure that the looping logic of writeAll works as
     * expected.
     *
     * @return void
     */
    public function testWriteAllLimited()
    {
        $fn = create_function('$a,$b', 'return socket_write($a,$b,1);');

        socket_connect($this->_socket->getHandle(), $this->_testIp, 80);

        $this->assertEquals(0, $this->_socket->getErrorCode());
        $this->_socket->writeAll("GET / HTTP/1.1\r\n\r\n", $fn);

        $response = socket_read($this->_socket->getHandle(), 12);
        $this->assertEquals('HTTP/1.1 200', $response);
    }

    /**
     * Simulates the case were socket_write returns an error.
     *
     * @return void
     * @expectedException Pdbg_Net_Socket_Exception
     */
    public function testWriteAllError()
    {
        $fn = create_function('$a,$b', 'return false;');

        socket_connect($this->_socket->getHandle(), $this->_testIp, 80);

        $this->assertEquals(0, $this->_socket->getErrorCode());
        $this->_socket->writeAll('foo', $fn);
    }

    /**
     * Test to ensure that the read method works.
     *
     * @return void
     */
    public function testRead()
    {
        socket_connect($this->_socket->getHandle(), $this->_testIp, 80);

        $this->assertEquals(0, $this->_socket->getErrorCode());
        $this->_socket->writeAll("GET / HTTP/1.1\r\n\r\n");

        $response = $this->_socket->read(12);
        $this->assertEquals('HTTP/1.1 200', $response);
    }

    /**
     * Simulates the case were socket_read returns an error.
     * 
     * @expectedException Pdbg_Net_Socket_Exception
     */
    public function testReadError()
    {
        $fn = create_function('$a,$b', 'return false;');

        $response = $this->_socket->read(1, $fn);
    }

    /**
     * Test to ensure that isDataAvailable works correctly when no data is
     * available.
     *
     * @return void
     */
    public function testNoDataAvailable()
    {
        socket_connect($this->_socket->getHandle(), $this->_testIp, 80);
        $this->assertEquals(0, $this->_socket->getErrorCode());

        $this->assertFalse($this->_socket->isDataAvailable());
    }

    /**
     * Test to ensure that isDataAvailable works correctly when data is 
     * available. NB - this method assumes that if 1 bytes is available
     * then at least 1 more is also available, which is a safe assumption
     * in most cases.
     *
     * @return void
     */
    public function testDataAvailable()
    {
        socket_connect($this->_socket->getHandle(), $this->_testIp, 80);
        $this->assertEquals(0, $this->_socket->getErrorCode());

        $this->assertEquals(0, $this->_socket->getErrorCode());
        $this->_socket->writeAll("GET / HTTP/1.1\r\n\r\n");

        $data = $this->_socket->read(1);
        $this->assertTrue($this->_socket->isDataAvailable());
    }
}
