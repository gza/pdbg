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
 * Represents a debugger engine init response.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse_Init extends Pdbg_Net_Dbgp_EngineResponse
{
    /**
     * Returns the uri of the script being debugged.
     *
     * @return string
     */
    public function getFileUri()
    {
        return $this->_doc->documentElement->getAttribute('fileuri');
    }

    /**
     * Returns information about the debugger engine, if present. This method
     * returns an array with two elements. The first is the engine name, if
     * present. The second is the engine version, if present.
     *
     * @return array
     */
    public function getEngineInfo()
    {
        $root = $this->_doc->documentElement;
        $list = $root->getElementsByTagName('engine');

        if ($list->length > 0) {
            $engine  = $list->item(0);
            $version = '';

            if ($engine->hasAttribute('version')) {
                $version = $engine->getAttribute('version');
            }

            return array($engine->nodeValue, $version);
        } else {
            return array(null, null);
        }
    }
}
