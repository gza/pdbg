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

        // the initial response is a special case and must be handled specially.
        if ($doc->documentElement->nodeName == 'init') {
            return self::_instantiateClass('init', $doc);
        }

        if (!Pdbg_Net_Dbgp_EngineResponse::commandSuccessfulFromDocument($doc)) {
            return new Pdbg_Net_Dbgp_EngineResponse($doc);
        }

        $command = Pdbg_Net_Dbgp_EngineResponse::getCommandFromDocument($doc);

        return self::_instantiateClass($command, $doc);
    }

    /**
     * A simple response class loader and instantiator.
     *
     * @param string $type
     */
    protected static function _instantiateClass($type, $doc)
    {
        $capType   = ucfirst($type);
        $className = "Pdbg_Net_Dbgp_EngineResponse_{$capType}";
        $path      = str_replace('_', DIRECTORY_SEPARATOR, $className) . '.php';

        if (!class_exists($className) and self::_isIncludable($path)) {
            require_once $path;
        }
        if (!class_exists($className)) {
            $className = 'Pdbg_Net_Dbgp_EngineResponse';
        }

        return new $className($doc);
    }

    /**
     * Checks to see if $fileName, which is assumed to be a relative path, is
     * includable; that is, if it exists and is readable relative to the 
     * current include path.
     *
     * @param string $fileName
     * @return boolean
     */
    protected static function _isIncludable($fileName)
    {
        $paths = explode(PATH_SEPARATOR, get_include_path());

        foreach ($paths as $path) {
            $absPath = rtrim($path, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . $fileName;

            if (is_readable($absPath)) {
                return true;
            }
        }

        return false;
    }
}
