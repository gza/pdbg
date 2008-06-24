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
 * @see Pdbg_Net_Dbgp_EngineResponse_Source
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Source.php';

/**
 * Tests for Pdbg_Net_Dbgp_EngineResponse_Source
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse_SourceTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test to ensure that the getSource method works as expected.
     *
     * @return void
     */
    public function testGetSource()
    {
        $xml  = '<?xml version="1.0"?><response success="1">Zm9v</response>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse_Source($xml);

        $this->assertEquals('foo', $resp->getSource());
    }

    /**
     * Test to ensure that an exception is thrown when using getSource on an
     * unsuccessful response.
     *
     * @return void
     * @expectedException Pdbg_Net_Dbgp_EngineResponse_Exception
     */
    public function testGetSourceNotSuccessful()
    {
        $xml  = '<?xml version="1.0"?><response success="0">Zm9v</response>';
        $resp = new Pdbg_Net_Dbgp_EngineResponse_Source($xml);

        $resp->getSource();
    }
}
