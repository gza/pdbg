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
 * Constructs a GtkSourceView object configured as needed for this app.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Gtk_Widget_SourceView extends GtkSourceView
{
    /**
     * Constructs an instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();

        $langMgr = new GtkSourceLanguagesManager();
        $phpLang = $langMgr->get_language_from_mime_type('application/x-php');
        $buffer  = GtkSourceBuffer::new_with_language($phpLang);

        $buffer->set_highlight(true);

        $this->set_show_line_numbers(true);
        $this->set_editable(false);
        $this->set_cursor_visible(false);
        $this->set_buffer($buffer);

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
