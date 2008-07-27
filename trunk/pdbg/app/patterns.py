# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Design patterns used throughout the application."""

__version__ = "$Id$"

def bind_params(func, *outer_args):
    """Make a new function with outer_args passed in."""
    def new_func(*inner_args, **keywords):
        return func(*(inner_args+outer_args), **keywords)
    return new_func

class SingletonException(Exception):
    """Thrown on error by the Singleton class."""

    pass

class Singleton(object):

    """Implement the singleton pattern.

    Extend this class to implement the singleton pattern."""

    @classmethod
    def get_instance(klass):
        """Get the singleton instance of the class.

        This method creates an instance if one does not yet exist.
        """
        if klass == Singleton:
            raise SingletonException, "Cannot call get_instance on class Singleton."
        if not klass.__dict__.has_key('_singleton'):
            klass._singleton = klass()
        return klass._singleton

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
        keep = []
        for curr in self._events[name]:
            called = False
            if curr['condition'] != None:
                if curr['condition'](*arguments):
                    curr['observer'](*arguments)
                    called = True
            else:
                curr['observer'](*arguments)
                called = True
            if not called or not curr['once']:
                keep.append(curr)
        self._events[name] = keep
        return self

    def add_observer(self, name=None, observer=None, condition=None, \
        once=False, **keywords):
        """Add an event observer.

        Keyword arguments for this method will be handled as follows: keys are
        event names and values are observer functions.
        """
        if name != None:
            if not self._events.has_key(name):
                raise LookupError, "Event %s not registered." % (name,)
            if callable(observer):
                self._events[name].append({
                    'observer': observer,
                    'condition': condition,
                    'once': once
                })
        for (name, observer) in keywords.items():
            self.add_observer(name, observer)
        return self

    def remove_observer(self, name, observer):
        """Removes an event observer.

        Returns True if an observer was removed, False otherwise.
        """
        if not self._events.has_key(name):
            raise LookupError, "Event %s not registered." % (name,)
        for (idx, curr) in enumerate(self._events[name]):
            if curr['observer'] == observer:
                del self._events[name][idx]
                return True
        return False

class Manager(Observable):
    pass
