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
 * @see Pdbg_Exception
 */
require_once 'Pdbg/Exception.php';

/**
 * Class that can be extended to add a simple event handling system to
 * instances.
 *
 * @category   Development
 * @package    Pdbg
 * @author     Christopher Utz <cutz@chrisutz.com>
 * @copyright  2008 Christopher Utz <cutz@chrisutz.com>
 * @license    http://www.gnu.org/licenses/gpl.html GPLv3
 * @version    SVN: $Id$
 * @link       http://pdbg.googlecode.com
 */
class Pdbg_Observable
{
    /**
     * An array where the keys are event types and the values are arrays
     * of observers of that type.
     *
     * @var array
     */
    private $_events = array();

    /**
     * Registers a new event type, which observers can bind to via the
     * addObserver method.
     *
     * @param string $name
     * @return Pdbg_Observable
     */
    public function addEvent($name)
    {
        if (!array_key_exists($name, $this->_events)) {
            $this->_events[$name] = array();
        }

        return $this;
    }

    /**
     * Fires all the observer functions observing the event $eventName, passing 
     * in the elements of $args as arguments. If $args is not an array, the 
     * observing functions will be called with $args as the single argument.
     *
     * @param string $eventName
     * @param mixed $args
     * @return Pdbg_Observable
     * @throws Pdbg_Exception
     */
    public function fire($eventName, $args)
    {
        $args = (array) $args;

        if (!array_key_exists($eventName, $this->_events)) {
            throw new Pdbg_Exception("unknown event: {$eventName}");
        }

        foreach ($this->_events[$eventName] as $observerFn) {
            call_user_func_array($observerFn, $args);
        }

        return $this;
    }

    /**
     * Adds the observer function $observerFn to the event $eventName.
     *
     * @param string $eventName
     * @param mixed $observerFn
     * @return Pdbg_Observable
     * @throws Pdbg_Exception
     */
    public function addObserver($eventName, $observerFn)
    {
        if (!array_key_exists($eventName, $this->_events)) {
            throw new Pdbg_Exception("unknown event: {$eventName}");
        }

        $this->_events[$eventName][] = $observerFn;

        return $this;
    }
}
