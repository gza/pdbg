# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Implement the observable pattern."""

__version__ = "$Id$"

class Observable(object):

    """Implement the observable pattern.

    Extend this class to add an event observing mechanism to subclasses.
    """

    def __init__(self):
        """Construct an instance."""
        self._events = {}

    def register_event(self, *names):
        """Register observable event(s).

        The number of arguments to this method is variable. Each argument must 
        be the name of an event to register as being observable.
        """
        for name in names:
            if not self._events.has_key(name):
                self._events[name] = []
        return self

    def fire(self, name, *arguments):
        """Fire an event.

        When called, this method will invoke all observer functions registered
        with the event. The first parameter passed to observer functions is the
        observable.  The 2nd and subsequent parameters to the observer 
        functions are the 2nd and subsequent arguments to this method.
        """
        if not self._events.has_key(name):
            raise LookupError, "Event %s not registered." % (name,)
        arguments = list(arguments)
        arguments.insert(0, self)
        for observer in self._events[name]:
            observer(*arguments)
        return self

    def add_observer(self, name=None, observer=None, **keywords):
        """Add an event observer.

        Keyword arguments for this method will be handled as follows: keys are
        event names and values are observer functions.
        """
        if name != None:
            if not self._events.has_key(name):
                raise LookupError, "Event %s not registered." % (name,)
            if callable(observer):
                self._events[name].append(observer)
        for (name, observer) in keywords.items():
            self.add_observer(name, observer)
        return self

    def remove_observer(self, name, observer):
        """Removes an event observer.

        Returns True if an observer was removed, False otherwise.
        """
        if not self._events.has_key(name):
            raise LookupError, "Event %s not registered." % (name,)
        for (idx, curr_observer) in enumerate(self._events[name]):
            if curr_observer == observer:
                del self._events[name][idx]
                return True
        return False


