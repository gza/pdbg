#!/usr/bin/python
# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""Invoke the command line application."""

__version__ = "$Id$"

from pdbg.cli.app import App

if __name__ == '__main__':
    App.get_instance().run()
