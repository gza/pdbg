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
     * Manager state constants.
     */
    const AWAITING_INIT        = 'AwaitingInit';
    const AWAITING_INIT_SOURCE = 'AwaitingInitSource';
    const AWAITING_INIT_STATUS = 'AwaitingInitStatus';
    const CAN_INTERACT         = 'CanInteract';
    const CANNOT_INTERACT      = 'CannotInteract';

    /**
     * Continuation command constants.
     */
    const RUN       = 'run';
    const STEP_INTO = 'step_into';
    const STEP_OVER = 'step_over';
    const STEP_OUT  = 'step_out';
    const STOP      = 'stop';
    const DETACH    = 'detach';

    /**
     * The connection managed by this manager.
     *
     * @var Pdbg_Net_Dbgp_Connection
     */
    protected $_conn;

    /**
     * Value equals one of the manager state constants.
     *
     * @var string
     */
    protected $_mgrState;

    /**
     * The status value returned from the last status response.
     *
     * @var string
     */
    protected $_lastStatus = null;

    /**
     * The reason value return from the last status response.
     *
     * @var string
     */
    protected $_lastReason = null;

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
        $this->_mgrState = self::AWAITING_INIT;

        Pdbg_App::getInstance()->addObserver('timeout', array($this, 'onTimeout'));

        $this->addEvent(array(
             'response-read',
             'command-written',
             'init-packet',
             'init-source',
             'ready',
             'can-interact',
             'cannot-interact',
             'status',
        ));
    }

    /**
     * Returns the connection status as returned by the last status response.
     *
     * @return string
     */
    public function getEngineStatus()
    {
        return $this->_lastStatus;
    }

    /**
     * Returns the status change reason as returned by the last status response.
     *
     * @return string
     */
    public function getStatusReason()
    {
        return $this->_lastReason;
    }

    /**
     * Is the state of the ide/engine communications such that the ide can
     * interact with the engine?
     *
     * @return boolean
     */
    public function canInteract()
    {
        return ($this->_mgrState == self::CAN_INTERACT);
    }

    /**
     * Sends a continuation command (run, step_into, etc.)
     *
     * @param string $type One of the continuation command constants.
     * @return void
     */
    public function sendContinuation($type)
    {
        $this->_mgrState = self::CANNOT_INTERACT;

        $this->fire('command-written', $this->_conn->writeCommand($type));
        $this->fire('cannot-interact');
    }

    /**
     * Returns true if continuation commands can be sent over the connection.
     *
     * @return boolean
     */
    public function canSendContinuation()
    {
        return in_array($this->_lastStatus, array('starting', 'break')) and
               $this->_mgrState == self::CAN_INTERACT;
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
        $this->{'_run' . $this->_mgrState}($response);
    }

    /**
     * TODO: document
     */
    protected function _runAwaitingInit($response)
    {
        if ($response->getType() != 'Init') {
            throw new Pdbg_App_Exception("Expected init response (got {$response->getType()})");
        }

        // read the remote ip address and port.
        $sh = $this->_conn->getSocket()->getHandle();
        socket_getpeername($sh, $ipAddress, $port);

        $this->fire('init-packet', array($response, $ipAddress, $port));

        $cmd = $this->_conn->writeCommand('source', array(
            '-f' => $response->getFileUri()
        ));

        $this->fire('command-written', $cmd);

        $this->_mgrState = self::AWAITING_INIT_SOURCE;
    }

    /**
     * TODO: document
     */
    protected function _runAwaitingInitSource($response)
    {
        if (!$response->commandSuccessful()) {
            throw new Pdbg_App_Exception("Initial source command must be successful");
        }
        if ($response->getType() != 'Source') {
            throw new Pdbg_App_Exception("Expected source response (got {$response->getType()})");
        }

        $this->fire('init-source', $response);

        $cmd = $this->_conn->writeCommand('status');

        $this->fire('command-written', $cmd);

        $this->_mgrState = self::AWAITING_INIT_STATUS;
    }

    /**
     * Run by the manager after the initial source is received.
     *
     * @param Pdbg_Net_Dbgp_EngineResponse
     * @return void
     */
    protected function _runAwaitingInitStatus($response)
    {
        if (!$response->commandSuccessful()) {
            throw new Pdbg_App_Exception("Initial status command must be successful");
        }
        if ($response->getType() != 'Status') {
            throw new Pdbg_App_Exception("Expected status response (got {$response->getType()})");
        }

        $this->_lastStatus = $response->getStatus();
        $this->_lastReason = $response->getReason();

        // TODO: if status == break, we need to get the initial line information

        // Connection is now ready to be used by the application.
        $this->_mgrState = self::CAN_INTERACT;

        $this->fire('status', $response);
        $this->fire('ready');
        $this->fire('can-interact');

    }

    /**
     * Run by the manager when the IDE can submit commands to the engine.
     *
     * @param Pdbg_Net_Dbgp_EngineResponse
     * @return void
     */
    protected function _runCanInteract($response)
    {

    }

    /**
     * Run by the manager when the IDE cannot submit commands to the engine.
     *
     * @param Pdbg_Net_Dbgp_EngineResponse
     * @return void
     */
    protected function _runCannotInteract($response)
    {
        // The debugger engine is running code, and the IDE cannot send 
        // commands. Wait until a status response is received, then switch back
        // to CAN_INTERACT.
        if ($response->getType() != 'Status') {
            throw new Pdbg_App_Exception("Expected status response (got {$response->getType()})");
        }

        $this->_mgrState = self::CAN_INTERACT;

        $this->fire('status', $response);
        $this->fire('can-interact');
    }
}
