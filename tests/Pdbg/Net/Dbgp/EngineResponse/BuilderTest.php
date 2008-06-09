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
 * @see Pdbg_Net_Dbgp_EngineResponse_Builder
 */
require_once 'Pdbg/Net/Dbgp/EngineResponse/Builder.php';

/**
 * Tests for Pdbg_Net_Socket
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Net_Dbgp_EngineResponse_BuilderTest extends PHPUnit_Framework_TestCase
{
    /**
     * @var Pdbg_Net_Dbgp_EngineResponse_Builder
     */
    protected $_builder;

    /**
     * Sets up the environment before a test case.
     *
     * @return void
     */
    public function setUp()
    {
        $this->_builder = new Pdbg_Net_Dbgp_EngineResponse_Builder();
    }

    /**
     * Test to ensure that response objects are built correctly.
     *
     * @return void
     */
    public function testBuild()
    {
        $data = "34\x00<?xml version=\"1.0\"?><root></root>\x00";
        $amtAdded = 0;

        while (true) {
            $reqAmt = $this->_builder->getRequestedAmount();
            $this->_builder->addData(substr($data, $amtAdded, $reqAmt));
            $amtAdded += $reqAmt;

            if (null !== ($r = $this->_builder->getResponse())) {
                break;
            }
        }

        $doc = $r->getDocument();
        $this->assertEquals('root', $doc->documentElement->nodeName);
    }

    /**
     * Test to ensure that response objects are built correctly when data
     * is passed in in smaller chunks than is ideal.
     *
     * @return void
     */
    public function testBuildByOne()
    {
        $data = "34\x00<?xml version=\"1.0\"?><root></root>\x00";
        $amtAdded = 0;

        while (true) {
            $reqAmt = $this->_builder->getRequestedAmount();
            $this->_builder->addData(substr($data, $amtAdded, 1));
            $amtAdded += 1;

            if (null !== ($r = $this->_builder->getResponse())) {
                break;
            }
        }

        $doc = $r->getDocument();
        $this->assertEquals('root', $doc->documentElement->nodeName);
    }
}
