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
 * @see Pdbg_Net_Dbgp_Connection
 */
require_once 'Pdbg/Net/Dbgp/Connection.php';

/**
 * @see Pdbg_App_Gtk_Widget_TextLog
 */
require_once 'Pdbg/App/Gtk/Widget/TextLog.php';

/**
 * Manages the ui of a single connection page.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_ConnectionPage
{
    /**
     * @var Pdbg_App_ConnectionManager
     */
    protected $_connMgr;

    /**
     * @var Pdbg_App_Gtk_Widget_TextLog
     */
    protected $_commTextLog;

    /**
     *
     */
    public function __construct(Pdbg_App_ConnectionManager $connMgr)
    {
        $this->_connMgr = $connMgr;
        $this->_initGui();

        Gtk::timeout_add(500, array($this, 'onTimeout'));
    }

    /**
     *
     */
    protected function _initGui()
    {
        $this->_commTextLog = new Pdbg_App_Gtk_Widget_TextLog();

        $propNotebook = new GtkNotebook();
        $propNotebook->set_tab_pos(Gtk::POS_BOTTOM);
        $propNotebook->append_page($this->_commTextLog, new GtkLabel('Communications'));

        $sourceSplit = new GtkVPaned();
        $sourceSplit->add1(new GtkLabel('Source'));
        $sourceSplit->add2($propNotebook);

        $fileSplit = new GtkHPaned();
        $fileSplit->add1(new GtkLabel('Files'));
        $fileSplit->add2($sourceSplit);

        $connPgMgr = Pdbg_App_Gtk_ConnectionPageManager::getInstance();
        $mainNotebook = $connPgMgr->getNotebook();
        $mainNotebook->append_page($fileSplit);
        $mainNotebook->show_all();
    }

    public function onTimeout()
    {
        /*
        if (null !== $response = $this->_conn->readResponse()) {
            $this->_commTextLog->appendText($response->getXml());
        }
        */
        $this->_connMgr->run();

        return true;
    }
}
