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
 * @see Pdbg_Observable
 */
require_once 'Pdbg/Observable.php';

/**
 * @see Pdbg_App
 */
require_once 'Pdbg/App.php';

/**
 * @see Pdbg_App_Exception
 */
require_once 'Pdbg/App/Exception.php';

/**
 * @see Pdbg_Net_Dbgp_Connection
 */
require_once 'Pdbg/Net/Dbgp/Connection.php';

/**
 * Manages the application's communications with the debugger engine.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_ConnectionManager extends Pdbg_Observable
{
    /**
     * Connection state constants.
     */
    const AW_INIT     = 'AwaitingInit';
    const AW_INIT_SRC = 'AwaitingInitSrc';
    const AW_INIT_STA = 'AwaitingInitStatus';

    /**
     * The connection managed by this manager.
     *
     * @var Pdbg_Net_Dbgp_Connection
     */
    protected $_conn;

    /**
     * Value equals one of the connection state constants.
     *
     * @var string
     */
    protected $_state;

    /**
     * Constructs an instance.
     *
     * @param Pdbg_Net_Dbgp_Connection $conn
     * @return void
     */
    public function __construct(Pdbg_Net_Dbgp_Connection $conn)
    {
        parent::__construct();

        $this->_conn  = $conn;
        $this->_state = self::AW_INIT;

        Pdbg_App::getInstance()->addObserver('timeout', array($this, 'onTimeout'));

        $this->addEvent(array(
             'response-read',
             'command-written',
             'init-packet',
             'init-source',
             'status'
        ));
    }

    /**
     * Processes responses and sends commands.
     *
     * @return void
     */
    public function onTimeout()
    {
        if (null === ($response = $this->_conn->readResponse())) {
            // nothing to do, return ...
            return;
        }

        $this->fire('response-read', $response);

        $this->{'_run' . $this->_state}($response);
    }

    /**
     *
     */
    protected function _runAwaitingInit($response)
    {
        if ($response->getType() != 'Init') {
            throw new Pdbg_App_Exception("expected init response");
        }

        // read the remote ip address and port.
        $sh = $this->_conn->getSocket()->getHandle();
        socket_getpeername($sh, $ipAddress, $port);

        $this->fire('init-packet', array($response, $ipAddress, $port));

        $cmd = $this->_conn->writeCommand('source', array(
            '-f' => $response->getFileUri()
        ));

        $this->fire('command-written', $cmd);

        $this->_state = self::AW_INIT_SRC;
    }

    /**
     *
     */
    protected function _runAwaitingInitSrc($response)
    {
        if (!$response->commandSuccessful()) {
            throw new Pdbg_App_Exception("initial source command must be successful");
        }
        if ($response->getType() != 'Source') {
            throw new Pdbg_App_Exception("expected source response");
        }

        $this->fire('init-source', $response);

        $cmd = $this->_conn->writeCommand('status');

        $this->fire('command-written', $cmd);

        $this->_state = self::AW_INIT_STA;
    }

    protected function _runAwaitingInitStatus($response)
    {
        if (!$response->commandSuccessful()) {
            throw new Pdbg_App_Exception("initial status command must be successful");
        }
        if ($response->getType() != 'Status') {
            throw new Pdbg_App_Exception("expected status response");
        }

        $this->fire('status', $response);
    }
}
