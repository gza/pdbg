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
 * @see Pdbg_Net_Dbgp_EngineResponse_Factory
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Factory.php';

/**
 * Builds a debugger engine response from a data stream.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse_Builder
{
    /**
     * Builder state constants
     */
    const BUILDING_AMOUNT = 0;
    const BUILDING_DATA   = 1;
    const BUILT           = 2;

    /**
     * The current state of the builder.
     *
     * @var integer
     */
    protected $_state = 0;

    /**
     * The length of the engine response data.
     *
     * @var string
     */
    protected $_dataLength = '';

    /**
     * The response xml data.
     *
     * @var string
     */
    protected $_dataBuffer = '';

    /**
     * Returns the maximum amount of data to pass into the next call of addData.
     *
     * @return integer
     */
    public function getRequestedAmount()
    {
        if ($this->_state == self::BUILDING_AMOUNT) {
            return 1;
        } else {
            // Extra 1 is for the NULL after the data
            return 1 + ($this->_dataLength - strlen($this->_dataBuffer));
        }
    }

    /**
     * Buffers response data.  Callers should invoke getRequestedAmount before
     * calling this method to get the maximum length of data this method
     * expects.
     *
     * @param string $data
     * @return void
     */
    public function addData($data)
    {
        // TODO: if dataLength exceeds a certain size, this method should throw
        // an exception.

        if (strlen($data) == 0) {
            return;
        }

        if ($this->_state == self::BUILDING_AMOUNT) {
            if ($data == "\x00") {
                $this->_state = self::BUILDING_DATA;
            } else {
                $this->_dataLength .= $data;
            }
        } else {
            if ($data[strlen($data)-1] == "\x00") {
                $this->_dataBuffer .= substr($data, 0, -1);
                $this->_state = self::BUILT;
            } else {
                $this->_dataBuffer .= $data;
            }
        }
    }

    /**
     * Returns an EngineResponse object when all response data has been
     * supplied, or null if the supplied data is incomplete.
     *
     * @return Pdbg_Net_Dbgp_EngineResponse|null
     */
    public function getResponse()
    {
        if ($this->_state == self::BUILT) {
            return Pdbg_Net_Dbgp_EngineResponse_Factory::instantiate($this->_dataBuffer);
        } else {
            return null;
        }
    }
}
