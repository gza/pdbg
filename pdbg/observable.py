# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO"""

__version__ = "$Id$"

class Observable:

    def __init__(self):
        self._events = {}

    def register_event(self, *names):
        for name in names:
            if not self._events.has_key(name):
                self._events[name] = []
        return self

    def fire(self, name, *arguments):
        if not self._events.has_key(name):
            raise LookupError, "Event %s not registered." % (name,)
        arguments = list(arguments)
        arguments.insert(0, self)
        for observer in self._events[name]:
            observer(*arguments)
        return self

    def add_observer(self, name=None, observer=None, **keywords):
        if name != None:
            if not self._events.has_key(name):
                raise LookupError, "Event %s not registered." % (name,)
            if callable(observer):
                self._events[name].append(observer)
        for (name, observer) in keywords.items():
            self.add_observer(name, observer)
        return self

    def remove_observer(self, name, observer):
        if not self._events.has_key(name):
            raise LookupError, "Event %s not registered." % (name,)
        for (idx, curr_observer) in enumerate(self._events[name]):
            if curr_observer == observer:
                del self._events[name][idx]
                return True
        return False


