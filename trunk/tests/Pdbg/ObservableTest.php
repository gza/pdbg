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
 * Tests for Pdbg_Observable
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_ObservableTest extends PHPUnit_Framework_TestCase
{
    /**
     * Test to ensure that addEvent allows method chaining.
     *
     * @return void
     */
    public function testAddEvent()
    {
        $observable = new Pdbg_Observable();
        $this->assertType('Pdbg_Observable', $observable->addEvent('foo'));
    }

    /**
     * Test to ensure that addObserver allows method chaining.
     *
     * @return void
     */
    public function testAddObserver()
    {
        $observable = new Pdbg_Observable();
        $observable->addEvent('foo');

        $fn = create_function('', '');

        $this->assertType('Pdbg_Observable', $observable->addObserver('foo', $fn));
    }

    /**
     * Test to ensure that firing events works as expected with a single
     * argument.
     *
     * @return void
     */
    public function testFireOneArg()
    {
        $observable = new Pdbg_Observable();

        $fn = create_function('$a', 'echo $a;');
        
        $observable->addEvent('foo')
            ->addEvent('bar')
            ->addObserver('foo', $fn)
            ->addObserver('foo', $fn)
            ->addObserver('bar', $fn);

        ob_start();
        $observable->fire('foo', '-');
        $result = ob_get_clean();

        $this->assertEquals('--', $result);
    }

    /**
     * Test to ensure that firing events works as expected with multiple
     * arguments.
     *
     * @return void
     */
    public function testFireArgs()
    {
        $observable = new Pdbg_Observable();

        $fn = create_function('$a, $b', 'echo $a . $b;');
        
        $observable->addEvent('foo')->addObserver('foo', $fn);

        ob_start();
        $observable->fire('foo', array('-', '>'));
        $result = ob_get_clean();

        $this->assertEquals('->', $result);
    }
}
