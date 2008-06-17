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
    const AWAITING_INITIAL_RESPONSE = 'AwaitingInitialResponse';

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
        $this->_state = self::AWAITING_INITIAL_RESPONSE;

        Pdbg_App::getInstance()->addObserver('timeout', array($this, 'onTimeout'));

        $this->addEvent('response-read');
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
    protected function _runAwaitingInitialResponse($response)
    {
    }
}
