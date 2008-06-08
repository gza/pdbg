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
 * Represents a DGBp IDE command.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_IdeCommand
{
    /**
     * @var string
     */
    protected $_name = '';

    /**
     * @var array
     */
    protected $_arguments = array();

    /**
     * @var string
     */
    protected $_data = '';

    /**
     * Constructs an instance.
     *
     * @param string $name The name of the command
     * @param array $arguments The command argument string
     * @param string $data Optional data to send with the command
     * @return void
     */
    public function __construct($name, array $arguments = array(), $data = null)
    {
        $this->_name = $name;
        $this->_arguments = $arguments;
        $this->_data = $data;
    }

    /**
     * Constructs an DBGp IDE command.
     *
     * @return string
     */
    public function build()
    {
        $argStr = '';

        foreach ($this->_arguments as $label => $value) {
            $argStr .= ' ' . $label . ' ' . $value;
        }

        $cmdLine = $this->_name . $argStr;

        if (null !== $this->_data) {
            $cmdLine .= ' -- ' . base64_encode($this->_data);
        }

        $cmdLine .= "\x00";

        return $cmdLine;
    }

    /**
     * Returns a string representation of the command.
     *
     * @return string
     */
    public function __toString()
    {
        return $this->build();
    }
}
