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
 * @see Pdbg_Net_Dbgp_IdeCommand
 */
require_once 'Pdbg/Net/Dbgp/IdeCommand.php';

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
class Pdbg_Net_Dbgp_IdeCommandTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test to ensure that a command with no args/no data is built
     * correctly.
     *
     * @return void
     */
    public function testNoArgsNoData()
    {
        $command = new Pdbg_Net_Dbgp_IdeCommand('status');

        $this->assertEquals("status\x00", $command->build());
    }

    /**
     * Test to ensure that a command with one argument is built
     * correctly.
     *
     * @return void
     */
    public function testOneArg()
    {
        $command = new Pdbg_Net_Dbgp_IdeCommand('status', array('-i' => '1'));

        $this->assertEquals("status -i 1\x00", $command->build());
    }

    /**
     * Test to ensure that a command with many arguments is built
     * correctly.
     *
     * @return void
     */
    public function testManyArgs()
    {
        $command = new Pdbg_Net_Dbgp_IdeCommand('status', array(
            '-a' => 'hello',
            '-b' => 'world',
            '-c' => 'foo'
        ));

        $this->assertEquals("status -a hello -b world -c foo\x00", $command->build());
    }

    /**
     * Test to ensure that a command with args and data is built
     * correctly.
     *
     * @return void
     */
    public function testArgsData()
    {
        $command = new Pdbg_Net_Dbgp_IdeCommand('status', array(
            '-a' => 'A',
            '-b' => 'B',
        ), 'xyzzy');

        $b64 = base64_encode('xyzzy');

        $this->assertEquals("status -a A -b B -- $b64\x00", $command->build());
    }

    /**
     * Test to ensure that a command with no args but with data is built
     * correctly.
     *
     * @return void
     */
    public function testNoArgsData()
    {
        $command = new Pdbg_Net_Dbgp_IdeCommand('status', array(), 'xyzzy');

        $b64 = base64_encode('xyzzy');

        $this->assertEquals("status -- $b64\x00", $command->build());
    }

    /**
     * Test to ensure that the __toString magic method works.
     *
     * @return void
     */
    public function testToString()
    {
        $command = new Pdbg_Net_Dbgp_IdeCommand('status');
        $this->assertEquals("status\x00", (string) $command);
    }
}
