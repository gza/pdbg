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
 * @see Pdbg_App_ConnectionManager
 */
require_once 'Pdbg/App/ConnectionManager.php';

/**
 * @see Pdbg_App_Gtk_ConnectionPageManager
 */
require_once 'Pdbg/App/Gtk/ConnectionPageManager.php';

/**
 * Manages the main ui notebook pages. This class is a singleton.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_ConnectionPagesManager extends Pdbg_Observable
{
    /**
     * @var array
     */
    protected $_connPages = array();

    /**
     * Constructs an instance.
     *
     * @param void
     */
    public function __construct()
    {
        Pdbg_App::getInstance()->addObserver('new-connection', 
            array($this, 'onNewConnection'));
    }

    /**
     *
     *  @param Pdbg_Net_Dbgp_Connection $conn
     *  @return void
     */
    public function onNewConnection(Pdbg_Net_Dbgp_Connection $conn)
    {
        $mgr = new Pdbg_App_ConnectionManager($conn);
        $this->_connPages[] = new Pdbg_App_Gtk_ConnectionPageManager($mgr);
    }
}
