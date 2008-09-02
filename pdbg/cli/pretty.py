# Written by Christopher Utz <cutz@chrisutz.com>
# See LICENSE.txt for license information

"""TODO: document"""

__version__ = "$Id$"

from StringIO import StringIO
import math

def _calc_pad(max_num):
    return str(int(math.floor(math.log10(max_num)))+1)

def format_lines(code, start_num, highlight=None):
    lines = code.splitlines()
    io = StringIO()
    current_num = start_num
    pad = _calc_pad(start_num+len(lines)-1)
    fmt = "%"+pad+"s: %s\n"
    for line in lines:
        if highlight != None:
            if highlight == current_num:
                io.write('-> ')
            else:
                io.write('   ')
        io.write(fmt % (str(current_num), line))
        current_num += 1
    return io.getvalue().rstrip("\r\n")

def format_trace(stack_elems):
    io = StringIO()
    num = 0
    pad = _calc_pad(len(stack_elems))
    fmt1 = "#%-" + pad + "s %s\n"
    fmt2 = " %-" + pad + "s at %s:%s\n"
    fmt3 = "#%-" + pad + "s %s:%s\n"
    for elem in stack_elems:
        if elem.has_key('where'):
            io.write(fmt1 % (num, elem['where']))
            io.write(fmt2 % ('', elem['filename'], elem['lineno']))
        else:
            io.write(fmt3 % (num, elem['filename'], elem['lineno']))
        num += 1
    return io.getvalue().rstrip("\r\n")

def format_value(prop):
    if prop['type'] in ('string', 'int', 'float'):
        return prop['value']
    elif prop['type'] == 'bool':
        if prop['value'] == '1':
            return 'true'
        else:
            return 'false'
    elif prop['type'] == 'null':
        return 'null'
    elif prop['type'] == 'array':
        return 'array (length = %s)' % prop['numchildren']
    elif prop['type'] == 'object':
        return 'object'

def format_property(prop):
    io = StringIO()
    io.write("name: %s\n" % prop['fullname'])
    io.write("type: %s\n" % prop['type'])
    io.write(" val: %s\n" % format_value(prop))
    return io.getvalue().rstrip("\r\n")
