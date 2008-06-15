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
 * Manages the main ui notebook pages. 
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_ConnectionPageManager
{
    /**
     * @var Pdbg_App_Gtk_ConnectionPageManager
     */
    protected static $_singleton = null;

    /**
     * @var GtkNotebook
     */
    protected $_notebook;

    /**
     * @var array
     */
    protected $_connPages = array();

    /**
     * Constructs an instance.
     *
     * @param void
     */
    private function __construct()
    {
    }

    protected static function getInstance()
    {
        if (null === $this->_singleton) {
            $this->_singleton = new Pdbg_App_Gtk_ConnectionPageManager();
        }

        return $this->_singleton;
    }

    /**
     * @param GtkNotebook $notebook
     * @return void
     */
    public function setNotebook(GtkNotebook $notebook)
    {
        $this->_notebook = $notebook;
    }

    /**
     * @return GtkNotebook
     */
    public function getNotebook()
    {
        return $this->_notebook;
    }

    /**
     * 
     */
    public function addPageForConnection(Pdbg_Net_Dbgp_Connection $conn)
    {
        $this->_connPages[] = new Pdbg_App_Gtk_ConnectionPage($conn);
    }
}
