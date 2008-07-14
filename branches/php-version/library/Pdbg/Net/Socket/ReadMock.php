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
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Socket_ReadMock extends Pdbg_Net_Socket
{
    /**
     * @var integer
     */
    protected $_amtRead = 0;

    /**
     * @var string
     */
    protected $_readBuffer = null;

    /**
     *
     */
    public function __construct($readBuffer)
    {
        $this->_readBuffer = $readBuffer;
    }

    /**
     * Mock read method.
     *
     * @param integer $length
     * @param string $readFn
     * @return string
     */
    public function read($length, $readFn='socket_read')
    {
        $data = substr($this->_readBuffer, $this->_amtRead, $length);
        $this->_amtRead = min(strlen($this->_readBuffer), $this->_amtRead + $length);

        return $data;
    }

    /**
     * Mock isDataAvailable method.
     *
     * @return boolean
     */
    public function isDataAvailable()
    {
        return ($this->_amtRead < strlen($this->_readBuffer));
    }
}
