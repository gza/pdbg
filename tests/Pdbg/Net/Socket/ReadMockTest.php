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
 * @see Pdbg_Net_Socket_ReadMock
 */
require_once 'Pdbg/Net/Socket/ReadMock.php';

/**
 * Tests for Pdbg_Net_Socket_ReadMock
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Socket_ReadMockTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test to ensure that the mock behaves correctly with no data.
     *
     * @return void
     */
    public function testNoData()
    {
        $socket = new Pdbg_Net_Socket_ReadMock('');

        $this->assertFalse($socket->isDataAvailable());
        $this->assertEquals('', $socket->read(100));
    }

    /**
     * Test to ensure that reading data from the mock 1 byte at a time works
     * as expected.
     *
     * @return void
     */
    public function testReadByOne()
    {
        $socket = new Pdbg_Net_Socket_ReadMock('xyz');

        $this->assertTrue($socket->isDataAvailable());
        $this->assertEquals('x', $socket->read(1));
        $this->assertTrue($socket->isDataAvailable());
        $this->assertEquals('y', $socket->read(1));
        $this->assertTrue($socket->isDataAvailable());
        $this->assertEquals('z', $socket->read(1));
        $this->assertFalse($socket->isDataAvailable());
    }

    /**
     * Test to ensure that the mock behaves correctly when more data than is
     * available is requested.
     *
     * @return void
     */
    public function testReadAll()
    {
        $socket = new Pdbg_Net_Socket_ReadMock('xyzzy');
        $this->assertEquals('xyzzy', $socket->read(1000));
        $this->assertFalse($socket->isDataAvailable());
    }
}
