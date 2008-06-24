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
class Pdbg_App_Gtk_Widget_TextLog extends GtkTextView
{
    public function __construct()
    {
        parent::__construct();

        $buffer = new GtkTextBuffer();

        $this->set_buffer($buffer);
        $this->set_editable(false);
        $this->set_cursor_visible(false);
    }

    public function log($type, $text)
    {
        $time   = date('h:i:s A');
        $prefix = "[$time $type] ";
        // Place the prefix at the beginning of each line of text
        $text   = preg_replace('/^/m', $prefix, $text);
        // Ensure that there is a new line at the end of the text
        $text   = preg_replace('/[\r\n]*$/', "\r\n", $text);

        $buffer = $this->get_buffer();
        $buffer->place_cursor($buffer->get_end_iter());
        $buffer->insert_at_cursor($text);

        $this->_setFont();
    }

    /**
     * Sets up the control's font.
     * TODO: fix me!
     *
     * @return void
     */
    protected function _setFont()
    {
        $desc = new PangoFontDescription();
        $desc->set_family('Mono');

        $this->modify_font($desc);
    }
}
