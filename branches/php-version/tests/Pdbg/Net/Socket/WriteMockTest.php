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
 * @see Pdbg_Net_Socket_WriteMock
 */
require_once 'Pdbg/Net/Socket/WriteMock.php';

/**
 * Tests for Pdbg_Net_Socket_WriteMock
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Socket_WriteMockTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test to ensure that the mock behaves correctly when no data has been
     * written.
     *
     * @return void
     */
    public function testNoData()
    {
        $socket = new Pdbg_Net_Socket_WriteMock();
        $this->assertEquals('', $socket->getDataWritten());
    }

    /**
     * Test to ensure that the writeAll mock behaves correctly.
     *
     * @return void
     */
    public function testWriteAll()
    {
        $socket = new Pdbg_Net_Socket_WriteMock();
        $socket->writeAll('xyz');

        $this->assertEquals('xyz', $socket->getDataWritten());
    }

    /**
     * Test to ensure that the writeAll mock behaves correctly when
     * called repeatedly.
     *
     * @return void
     */
    public function testWriteAllMany()
    {
        $socket = new Pdbg_Net_Socket_WriteMock();

        $socket->writeAll('xyz');
        $this->assertEquals('xyz', $socket->getDataWritten());

        $socket->writeAll('123');
        $this->assertEquals('xyz123', $socket->getDataWritten());
    }
}