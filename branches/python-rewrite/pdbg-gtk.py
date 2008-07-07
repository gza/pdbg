#!/usr/bin/python
# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Invoke the GTK application."""

__version__ = "$Id$"

from pdbg.gtk.app import App

if __name__ == '__main__':
    App.get_instance().run()
