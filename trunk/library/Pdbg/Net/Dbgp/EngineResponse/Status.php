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
 * @see Pdbg_Net_Dbgp_EngineResponse
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse.php';

/**
 * @see Pdbg_Net_Dbgp_EngineResponse_Exception
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Exception.php';

/**
 * Represents a debugger engine response to the status command.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse_Status extends Pdbg_Net_Dbgp_EngineResponse
{
    /**
     * Returns the running status of the engine.
     *
     * @return string One of: starting, stopping, stopped, running, break
     */
    public function getStatus()
    {
        return $this->getXPathValue('/dp:response/@status');
    }

    /**
     * Returns the reason why the engine has sent the status response (only of
     * relevance with status break).
     *
     * @return string One of: ok, error, aborted, exception
     */
    public function getReason()
    {
        return $this->getXPathValue('/dp:response/@reason');
    }
}