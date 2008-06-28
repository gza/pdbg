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
 * @version    SVN: $Id: ConnectionPage.php 13 2008-06-15 18:46:01Z baron314159@yahoo.com $
 * @link       http://pdbg.googlecode.com
 */

/**
 * @see Pdbg_Observable
 */
require_once 'Pdbg/Observable.php';

/**
 * @see Pdbg_Net_Dbgp_Connection
 */
require_once 'Pdbg/Net/Dbgp/Connection.php';

/**
 * @see Pdbg_App_Gtk_Widget_TextLog
 */
require_once 'Pdbg/App/Gtk/Widget/TextLog.php';

/**
 * @see Pdbg_App_Gtk_Widget_SourceView
 */
require_once 'Pdbg/App/Gtk/Widget/SourceView.php';

/**
 * Manages the ui of a single connection page.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id: ConnectionPage.php 13 2008-06-15 18:46:01Z baron314159@yahoo.com $
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_ConnectionPageManager extends Pdbg_Observable
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
     * @var Pdbg_App_Gtk_Widget_SourceView
     */
    protected $_sourceView;

    /**
     * @var GtkVPaned
     */
    protected $_sourceSplit;

    /**
     * @var GtkHPaned
     */
    protected $_fileSplit;

    /**
     * @var GtkLabel
     */
    protected $_tabLabel;

    /**
     * @var integer
     */
    protected $_pageIndex;

    /**
     *
     */
    public function __construct(Pdbg_App_ConnectionManager $connMgr)
    {
        parent::__construct();

        $this->_connMgr = $connMgr;
        $this->_initApp();
        $this->_initGui();
    }

    /**
     *
     */
    protected function _initApp()
    {
        $this->_connMgr->addObserver('response-read', 
            array($this, 'onResponseRead'));
        $this->_connMgr->addObserver('command-written',
            array($this, 'onCommandWritten'));
        $this->_connMgr->addObserver('init-packet',
            array($this, 'onInitPacket'));
        $this->_connMgr->addObserver('init-source',
            array($this, 'onInitSource'));
    }

    /**
     *
     */
    protected function _initGui()
    {
        $this->_commTextLog = new Pdbg_App_Gtk_Widget_TextLog();

        $logScroll = new GtkScrolledWindow();
        $logScroll->add($this->_commTextLog);

        $propNotebook = new GtkNotebook();
        $propNotebook->set_tab_pos(Gtk::POS_BOTTOM);
        $propNotebook->append_page($logScroll, new GtkLabel('Communications'));

        $this->_sourceView = new Pdbg_App_Gtk_Widget_SourceView();

        $sourceScroll = new GtkScrolledWindow();
        $sourceScroll->add($this->_sourceView);

        $sourceFrame = new GtkFrame();
        $sourceFrame->add($sourceScroll);
        $sourceFrame->set_shadow_type(Gtk::SHADOW_IN);

        $this->_sourceSplit = new GtkVPaned();
        $this->_sourceSplit->pack1($sourceFrame, true, false);
        $this->_sourceSplit->pack2($propNotebook, false, false);

        // Set the minimum requested height to 200px.
        $propNotebook->set_size_request(-1, 200);

        $this->_fileSplit = new GtkHPaned();
        $this->_fileSplit->pack1(new GtkLabel('Files'), false, false);
        $this->_fileSplit->pack2($this->_sourceSplit, true, false);

        $this->_tabLabel = new GtkLabel();

        $mainNotebook = Pdbg_App::getInstance()->getMainNotebook();
        $this->_pageIndex = $mainNotebook->append_page(
            $this->_fileSplit, $this->_tabLabel);
    }

    /**
     *
     */
    public function onResponseRead($response)
    {
        $this->_commTextLog->log('<<', $response->getXml());
    }

    /**
     *
     */
    public function onCommandWritten($command)
    {
        $this->_commTextLog->log('>>', $command->build(false));
    }

    /**
     *
     */
    public function onInitPacket($response, $ipAddress, $port)
    {
        list($engine, $version) = $response->getEngineInfo();
        $text = "[$ipAddress]";

        if ($engine) {
            $text .= ' ' . $engine;

            if ($version) {
                $text .= ' ' . $version;
            }
        }

        $this->_tabLabel->set_text($text);
    }

    /**
     *
     */
    public function onInitSource($response)
    {
        $this->_sourceView->get_buffer()
                          ->set_text($response->getSource());

        // The initial display of the page is setup, make the tab show up.
        $this->_fileSplit->show_all();

        // Make the page be on top.
        $mainNotebook = Pdbg_App::getInstance()->getMainNotebook();
        $mainNotebook->set_current_page($this->_pageIndex);
    }
}