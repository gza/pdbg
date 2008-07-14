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
 * @see Pdbg_Net_Dbgp_IdeCommand
 */
require_once 'Pdbg/Net/Dbgp/IdeCommand.php';

/**
 * @see Pdbg_Net_Dbgp_EngineResponse_Builder
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Builder.php';

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
     * @var Pdbg_Net_Dbgp_EngineResponse_Builder
     */
    protected $_responseBuilder = null;

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
     * Returns the connection's socket.
     *
     * @return Pdbg_Net_Socket
     */
    public function getSocket()
    {
        return $this->_socket;
    }

    /**
     * Writes an DBGp IDE command to the socket.
     *
     * @param string|Pdbg_Net_Dbgp_IdeCommand $command
     * @param array|null $args
     * @param string|null $data
     * @return Pdbg_Net_Dbgp_IdeCommand
     */
    public function writeCommand($command, $args = array(), $data = null)
    {
        if ($command instanceof Pdbg_Net_Dbgp_IdeCommand) {
            $this->_socket->writeAll((string) $command);
            return $command;
        } else {
            $obj = new Pdbg_Net_Dbgp_IdeCommand($command, $args, $data);
            $this->_socket->writeAll((string) $obj);
            return $obj;
        }
    }

    /**
     * Reads a response from the socket, or returns null if more data is
     * pending before a response can be built.
     *
     * @return Pdbg_Net_Dbgp_EngineResponse|null
     */
    public function readResponse()
    {
        if (!$this->_socket->isDataAvailable()) {
            return null;
        }

        if (null === $this->_responseBuilder) {
            $this->_responseBuilder = new Pdbg_Net_Dbgp_EngineResponse_Builder();
        }

        while ($this->_socket->isDataAvailable()) {
            $reqAmt = $this->_responseBuilder->getRequestedAmount();
            $data   = $this->_socket->read($reqAmt);

            $this->_responseBuilder->addData($data);

            $response = $this->_responseBuilder->getResponse();

            if (null !== $response) {
                $this->_responseBuilder = null;
                return $response;
            }
        }

        return null;
    }
}
