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
 * Represents a debugger engine response.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse
{
    /**
     * @var DOMDocument
     */
    protected $_doc;

    /**
     * Constructs an instance.
     *
     * @param string|DOMDocument $xmlData
     * @return void
     */
    public function __construct($xmlData)
    {
        if ($xmlData instanceof DOMDocument) {
            $this->_doc = $xmlData;
        } else {
            $this->_doc = new DOMDocument();
            $this->_doc->loadXML($xmlData);
        }

        $this->_doc->formatOutput = true;
    }

    /**
     * Returns a DOMDocument containing the response XML.
     *
     * @return DOMDocument
     */
    public function getDocument()
    {
        return $this->_doc;
    }

    /**
     * Returns the raw XML of the response.
     *
     * @return string
     */
    public function getXml()
    {
        return $this->_doc->saveXML();
    }

    /**
     * Returns the transaction id of the command causing this response.
     *
     * @return integer
     * @throws Pdbg_Net_Dbgp_EngineResponse_Exception
     */
    public function getTransactionId()
    {
        $root = $this->_doc->documentElement;

        if (!$root->hasAttribute('transaction_id')) {
            throw new Pdbg_Net_Dbgp_EngineResponse_Exception("transaction_id attribute does not exist");
        } else {
            return intval($root->getAttribute('transaction_id'));
        }
    }

    /**
     * Returns the command causing this engine response.
     *
     * @return string
     */
    public function getCommand()
    {
        return self::getCommandFromDocument($this->_doc);
    }

    /**
     * Reads the command from a DOMDocument.
     *
     * @param DOMDocument $doc
     * @return string
     * @throws Pdbg_Net_Dbgp_EngineResponse_Exception
     */
    public static function getCommandFromDocument(DOMDocument $doc)
    {
        $root = $doc->documentElement;

        if (!$root->hasAttribute('command')) {
            throw new Pdbg_Net_Dbgp_EngineResponse_Exception("command attribute does not exist");
        } else {
            return $root->getAttribute('command');
        }
    }

    /**
     * Returns true if the ide command causing this response was executed
     * successfully be the debugger engine.
     *
     * @return boolean
     */
    public function commandSuccessful()
    {
        return self::commandSuccessfulFromDocument($this->_doc);
    }

    /**
     * Returns true if the ide command causing the response in the supplied
     * DOMDocument was executed successfully be the debugger engine.
     *
     * @param DOMDocument $doc
     * @return boolean
     */
    public static function commandSuccessfulFromDocument(DOMDocument $doc)
    {
        $root   = $doc->documentElement;
        $errors = $root->getElementsByTagName('error');

        return ($errors->length == 0);
    }
}
