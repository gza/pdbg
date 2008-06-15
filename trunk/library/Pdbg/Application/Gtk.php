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
 * @see Pdbg_Net_Dbgp_Connection_Listener
 */
require_once 'Pdbg/Net/Dbgp/Connection/Listener.php';

/**
 * @see Pdbg_App_Gtk_ConnectionPageManager
 */
require_once 'Pdbg/App/Gtk/ConnectionPageManager.php';

/**
 * The main gtk application class.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk
{
    /**
     * @var Pdbg_Net_Dbgp_Connection_Listener
     */
    protected $_listener;

    /**
     * @var GtkWindow
     */
    protected $_mainWin;

    /**
     * Invokes the application.
     *
     * @return void
     */
    public function run()
    {
        $this->_initApp();
        $this->_initGui();

        $this->_mainWin->show_all();

        Gtk::timeout_add(500, array($this, 'onTimeout'));
        Gtk::main();
    }

    /**
     *
     */
    protected function _initApp()
    {
        $this->_listener = new Pdbg_Net_Dbgp_Connection_Listener();
    }

    /**
     *
     */
    protected function _initGui()
    {
        $this->_mainWin = new GtkWindow();
        $this->_mainWin->set_title(PDBG_APP_TITLE);
        $this->_mainWin->connect_simple('destroy', array('gtk', 'main_quit'));
        $this->_mainWin->set_position(Gtk::WIN_POS_CENTER);
        // TODO: this may need to change ...
        $this->_mainWin->set_size_request(800, 600);

        $this->_mainNotebook = new GtkNotebook();

        $ip   = $this->_listener->getIpAddress();
        $port = $this->_listener->getPort();

        $tabLbl  = new GtkLabel("Welcome!");
        $bodyLbl = new GtkLabel("Listening for connections on {$ip}:{$port} ...");
        $this->_mainNotebook->append_page($bodyLbl, $tabLbl);

        $this->_mainWin->add($this->_mainNotebook);

        Pdbg_App_Gtk_ConnectionPageManager::getInstance()
            ->setNotebook($this->_mainNotebook);
    }

    /**
     * Called periodically by GTK so that the application can handle its
     * DBGp connections.
     * 
     * @return boolean 
     */
    public function onTimeout()
    {
        $conn = $this->_listener->acceptConnection();

        if (null !== $conn) {
            // A connection has been made, make a new notebook page for it.
            $mgr = Pdbg_App_Gtk_ConnectionPageManager::getInstance();
            $mgr->addPageForConnection($conn);
        }

        // Return true to continue calling this callback on the specified 
        // interval.
        return true;
    }
}
