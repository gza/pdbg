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
 * @see Pdbg_Net_Dbgp_Connection
 */
require_once 'Pdbg/Net/Dbgp/Connection.php';

/**
 * @see Pdbg_Net_Dbgp_Connection_Exception
 */
require_once 'Pdbg/Net/Dbgp/Connection/Exception.php';

/**
 * Listens for incoming DBGp connections.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_Connection_Listener
{
    /**
     * The ip address to listen on for connections from debugger engines.
     *
     * @var string
     */
    protected $_ipAddress = '';

    /**
     * The port to listen on for connections from debugger engines.
     */
    protected $_port = '';

    /**
     * @var Pdbg_Net_Socket
     */
    protected $_socket = null;

    /**
     * Constructs an instance.
     *
     * @param string $ipAddress The ip address to listen on.
     * @param integer $port The port to listen on.
     * @return void
     */
    public function __construct($ipAddress='127.0.0.1', $port=9000)
    {
        $this->_ipAddress = $ipAddress;
        $this->_port = $port;

        $this->_initListeningSocket();
    }

    /**
     * Initializes the listening socket.
     *
     * @return void
     */
    protected function _initListeningSocket()
    {
        if (!function_exists('socket_create')) {
            throw new Pdbg_Net_Dbgp_Connection_Exception("socket extension is not available");
        }

        $sh = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        $socket = new Pdbg_Net_Socket($sh);

        if (!$sh) {
            throw new Pdbg_Net_Dbgp_Connection_Exception($socket->getErrorString());
        }

        // bind the socket to the supplied ip/port
        if (!socket_bind($sh, $this->_ipAddress, $this->_port)) {
            throw new Pdbg_Net_Dbgp_Connection_Exception($socket->getErrorString());
        }

        // make the socket listen for incoming connections
        if (!socket_listen($sh)) {
            throw new Pdbg_Net_Dbgp_Connection_Exception($socket->getErrorString());
        }

        // make the socket asyncronous
        socket_set_nonblock($sh);

        $this->_socket = $socket;
    }

    /**
     * Accepts a new connection on the listening socket, or returns null if 
     * there are no pending connections.
     *
     * @return Pdbg_Net_Dbgp_Connection|null
     */
    public function acceptConnection()
    {
        // socket_accept issues a warning message when a connection is not 
        // waiting.
        if (false !== ($inSocket = @socket_accept($this->_socket->getHandle()))) {
            return new Pdbg_Net_Dbgp_Connection(new Pdbg_Net_Socket($inSocket));
        } else {
            return null;
        }
    }
}
