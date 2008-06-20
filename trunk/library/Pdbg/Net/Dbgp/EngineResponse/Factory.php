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
 * @see Pdbg_Net_Dbgp_EngineResponse_Exception
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Exception.php';

/**
 * @see Pdbg_Net_Dbgp_EngineResponse_Source
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Source.php';

/**
 * 
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse_Factory
{
    /**
     * Instantiates an engine response of the appropriate type based upon
     * the supplied XML.
     *
     * @param string $xml
     * @return Pdbg_Net_Dbgp_EngineResponse
     */
    public static function instantiate($xml)
    {
        $doc = new DOMDocument();
        $doc->loadXML($xml);

        if (!Pdbg_Net_Dbgp_EngineResponse::commandSuccessfulFromDocument($doc)) {
            return new Pdbg_Net_Dbgp_EngineResponse($doc);
        }

        $command = Pdbg_Net_Dbgp_EngineResponse::getCommandFromDocument($doc);

        switch ($command) {
            case 'source':
                return new Pdbg_Net_Dbgp_EngineResponse_Source($doc);
            default:
                return new Pdbg_Net_Dbgp_EngineResponse($doc);
        }
    }
}
