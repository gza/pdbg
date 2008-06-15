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
 * 
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_Widget_TextLog extends GtkScrolledWindow
{
    protected $_textView;

    protected $_textBuf;

    public function __construct()
    {
        parent::__construct();

        $this->_textView = new GtkTextView();
        $this->_textBuf  = new GtkTextBuffer();

        $this->_textView->set_buffer($this->_textBuf);
        $this->_textView->set_editable(false);
        $this->_textView->set_cursor_visible(false);

        $this->add($this->_textView);
    }

    public function getTextView()
    {
        return $this->_textView;
    }

    public function getTextBuffer()
    {
        return $this->_textBuffer;
    }

    public function appendText($text)
    {
        $this->_textBuf->place_cursor($this->_textBuf->get_end_iter());
        $this->_textBuf->insert_at_cursor($text);
    }
}
