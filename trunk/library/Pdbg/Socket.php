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
 * A socket wrapper providing some convenience methods.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Socket
{
    /**
     * A socket resource handle.
     *
     * @var resource
     */
    protected $_socket = null;

    /**
     * Constructs an instance.
     *
     * @return void
     */
    public function __construct($socket)
    {
        $this->_socket = $socket;
    }

    /**
     * Destructs an instance.
     *
     * @return void
     */
    public function __destruct()
    {
        if (is_resource($this->_socket)) {
            socket_close($this->_socket);
        }
    }

    /**
     * Returns a string representation of the last error that occurred on the
     * socket.
     *
     * @return string
     */
    public function getErrorString()
    {
        return socket_strerror(socket_last_error($this->_socket));
    }

    /**
     * Returns the socket resource handle.
     *
     * @return resource
     */
    public function getHandle()
    {
        return $this->_socket;
    }

    /**
     * Writes all data in a string to the socket.
     *
     * @param string $data The data to write to the socket.
     * @return void
     * @throws Pdbg_Socket_Exception
     */
    public function writeAll($string)
    {
        $len = strlen($string);
        $amtWritten = 0;

        while ($amtWritten < $len) {
            $amt = socket_write($this->_socket, substr($string, $amtWritten));

            // TODO: check if connection was closed?

            if (false === $amt) {
                throw new Pdbg_Socket_Exception($this->getErrorString());
            }

            $amtWritten += $amt;
        }
    }
}
