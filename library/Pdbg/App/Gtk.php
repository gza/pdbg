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
 * @see Pdbg_App
 */
require_once 'Pdbg/App.php';

/**
 * @see Pdbg_Net_Dbgp_Connection_Listener
 */
require_once 'Pdbg/Net/Dbgp/Connection/Listener.php';

/**
 * @see Pdbg_App_Gtk_ToolbarManager
 */
require_once 'Pdbg/App/Gtk/ToolbarManager.php';

/**
 * @see Pdbg_App_Gtk_ConnectionPagesManager
 */
require_once 'Pdbg/App/Gtk/ConnectionPagesManager.php';

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
class Pdbg_App_Gtk extends Pdbg_App
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
     * Constructs an instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();

        $this->addEvent('timeout')
             ->addEvent('new-connection');
    }

    /**
     * Invokes the application.
     *
     * @return void
     */
    public function run()
    {
        $this->_init();
        $this->_mainWin->show_all();

        Gtk::main();
    }

    /**
     * Sets up the ui and application code.
     *
     * @return void
     */
    protected function _init()
    {
        // Set up the main window.
        $this->_mainWin = new GtkWindow();
        $this->_mainWin->set_title(PDBG_APP_TITLE);
        $this->_mainWin->connect_simple('destroy', array('gtk', 'main_quit'));
        $this->_mainWin->set_position(Gtk::WIN_POS_CENTER);
        // TODO: this size may need to change 
        $this->_mainWin->set_default_size(800, 600);

        // Setup the main notebook.
        $tabLabel  = new GtkLabel();
        $bodyLabel = new GtkLabel();
        $mainNotebook = new GtkNotebook();
        $mainNotebook->append_page($bodyLabel, $tabLabel);

        // Setup the main toolbar.
        $mainToolbar = new GtkToolbar();

        $vbox = new GtkVBox();
        $vbox->pack_start($mainToolbar, false, true);
        $vbox->pack_start($mainNotebook, true, true);

        $this->_mainWin->add($vbox);

        // Set up the connection listener.
        $this->_listener = new Pdbg_Net_Dbgp_Connection_Listener();

        Pdbg_App_Gtk_ConnectionPagesManager::getInstance()->init($mainNotebook);
        Pdbg_App_Gtk_ToolbarManager::getInstance()->init($mainToolbar);
        
        // Initialize the initial page labels.
        $ip   = $this->_listener->getIpAddress();
        $port = $this->_listener->getPort();
        $tabLabel->set_text("pDBG Information");
        $bodyLabel->set_text("Listening for connections on {$ip}:{$port} ...");

        // Set a timeout callback so that the app can do non-event based
        // processing, ie accepting debugger engine connections.
        // TODO: make the timeout value configurable.
        Gtk::timeout_add(500, array($this, 'onTimeout'));
    }

    /**
     * Called periodically by GTK so that the application can do processing
     * not resulting from UI events.
     * 
     * @return boolean 
     */
    public function onTimeout()
    {
        $conn = $this->_listener->acceptConnection();

        if (null !== $conn) {
            $this->fire('new-connection', $conn);
        }

        $this->fire('timeout');

        // Return true to continue calling this callback on the specified 
        // interval.
        return true;
    }
}
