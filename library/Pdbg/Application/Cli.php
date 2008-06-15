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
 * The main cli application class.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_App_Cli
{
    /**
     * @var Pdbg_Net_Dbgp_Connection
     */
    protected $_conn;

    public function readlineCallback($line)
    {
        $line = trim($line);

        if ($line == 'quit') {
            exit;
        } else if ($line == '') {
            return;
        }

        readline_add_history($line);

        $this->_conn->getSocket()->writeAll($line . "\x00");
    }

    public function run()
    {
        echo "Waiting for connection ...\n";

        $listener = new Pdbg_Net_Dbgp_Connection_Listener();

        while (true) {
            // Check for a connection, then sleep.
            if (null !== ($this->_conn = $listener->acceptConnection())) {
                break;
            }
            sleep(1);
        }

        readline_callback_handler_install('> ', array($this, 'readlineCallback'));

        while (1) {
            // See if any data has been entered on STDIN.
            list($r, $w, $e) = array(array(STDIN), null, null);
            $n = stream_select($r, $w, $e, 0, 1000);

            if (count($r) > 0) {
                // If yes, have readline process it.
                readline_callback_read_char();
            }

            $response = $this->_conn->readResponse();

            if (null !== $response) {
                echo "\n", $response->getDocument()->saveXML(), "\n";
                readline_on_new_line();
                readline_redisplay();
            }
        }
    }
}
