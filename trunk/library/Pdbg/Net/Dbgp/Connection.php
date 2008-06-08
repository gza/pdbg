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
class Pdbg_Net_Dbgp_Connection
{
    /**
     * @var Pdbg_Net_Socket
     */
    protected $_socket = null;

    /**
     * Constructs an instance.
     *
     * @param $socket Pdbg_Net_Socket
     * @return void
     */
    public function __construct(Pdbg_Net_Socket $socket)
    {
        $this->_socket = $socket;
    }

    /**
     * Writes an DBGp IDE command to the socket.
     *
     * @return void
     */
    public function writeCommand(Pdbg_Net_Dbgp_IdeCommand $command)
    {
        $this->_socket->writeAll((string) $command);
    }

    /**
     *
     */
    public function readResponse()
    {
        $dataLength = '';

        while ("\x00" !== ($ch = $this->_socket->readAll(1))) {
            $dataLength .= $ch;
        }

        $xml = $this->_socket->readAll($dataLength);

        // disregard the NULL byte after the XML
        $this->_socket->readAll(1);
    }
}
