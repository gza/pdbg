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
 * Manages the toolbar ui.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_ToolbarManager extends Pdbg_Observable
{
    protected static $_buttonNames = array(
        'continue' => 'Continue',
        'break'    => 'Break',
        'stop'     => 'Stop',
        '-0'       => '-',
        'stepInto' => 'Step Into',
        'stepOver' => 'Step Over',
        'stepOut'  => 'Step Out',
    );

    /**
     * The toolbar button widgets.
     *
     * @var array
     */
    protected $_buttons = array();

    /**
     * Constructs an instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->_init();
    }    

    /**
     * Initializes the toolbar buttons and event handlers.
     *
     * @return void
     */
    protected function _init()
    {
        $toolbar = Pdbg_App::getInstance()->getMainToolbar();

        foreach (self::$_buttonNames as $name => $label) {
            if ($label == '-') {
                $sep = new GtkSeparatorToolItem();
                $toolbar->insert($sep, -1);
            } else {
                $img = GtkImage::new_from_file(APP_PATH . "/images/{$name}.png");

                $btn = new GtkToolButton($img, $label);
                //$btn->set_sensitive(false);
                $btn->connect_simple('clicked', array($this, 'on' . ucfirst($name)));

                $toolbar->insert($btn, -1);

                $this->_buttons[$name] = $btn;
            }
        }
    }

    /**
     *
     */
    public function onContinue()
    {
    }

    /**
     *
     */
    public function onBreak()
    {
    }

    /**
     *
     */
    public function onStop()
    {
    }

    /**
     *
     */
    public function onStepInto()
    {
    }

    /**
     *
     */
    public function onStepOver()
    {
    }

    /**
     *
     */
    public function onStepOut()
    {
    }
}
