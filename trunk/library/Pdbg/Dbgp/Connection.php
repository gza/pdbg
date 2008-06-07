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
 * @see Pdbg_Socket
 */
require_once 'Pdbg/Socket.php';

/**
 * A DBGp connection made from a debugging engine.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Dbgp_Connection
{
    /**
     * @var Pdbg_Socket
     */
    protected $_socket = null;

    /**
     * Constructs an instance.
     *
     * @param $socket Pdbg_Socket
     * @return void
     */
    public function __construct(Pdbg_Socket $socket)
    {
        $this->_socket = $socket;
    }

    /**
     * Constructs an IDE command string.
     *
     * @param string $name The name of the command
     * @param array $arguments The command argument string
     * @param string $data Optional data to send in the command
     * @return string
     */
    public static function buildCommand($name, array $arguments = array(), $data = null)
    {
        $argStr = '';

        foreach ($arguments as $label => $value) {
            $argStr .= ' ' . $label . ' ' . $value;
        }

        $cmdLine = $name . $argStr;

        if (null !== $data) {
            $cmdLine .= ' -- ' . base64_encode($data);
        }

        $cmdLine .= "\x00";

        return $cmdLine;
    }

    public static function command($name, array $arguments = array(), $data = null)
    {
        $cmd = self::buildCommand($name, $arguments, $data);
        $this->_socket->writeAll($cmd);
    }
}
