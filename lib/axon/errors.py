# coding: utf-8

# The MIT License (MIT)
# 
# Copyright (c) <2011-2014> <Shibzukhov Zaur, szport at gmail dot com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import unicode_literals

import sys

class LoaderError(Exception):
    #
    def __init__(self, lnum, pos, msg, chunk):
        self.msg = msg
        self.lnum = lnum
        self.pos = pos
        self.chunk = chunk
    #
    def __str__(self):
        return 'ERROR:: %s. line:%s pos:%s chunk: %s\n' % \
                    (self.msg, self.lnum, self.pos+1, repr(self.chunk))

def error(self, msg):
    e = LoaderError(self.lnum, self.pos, msg, self.line[self.pos:self.pos+16])
    self.errto.write(str(e))
    raise e
#
# def error_getvalue(self):
#     error(self, 'Invalid simple value')
#
def error_unexpected_end(self):
    error(self, 'Unexpected end')
#
def error_unexpected_end_string(self):
    error(self, 'Unexpected end of the string')
#
def error_getnumber(self):
    error(self, 'Invalid number')
#
def error_getint_part(self):
    error(self, 'Invalid int part or value')
#
def error_invalid_date(self):
    error(self, 'Invalid date')
#
def error_invalid_time(self):
    error(self, 'Invalid time')
#
def error_invalid_datetime(self):
    error(self, 'Invalid datetime')
#
def error_invalid_value(self, vtype=''):
    error(self, 'Invalid %s value' % vtype)
#
def error_invalid_value_with_prefix(self, prefix):
    error(self, "Invalid value with prefix '%s'" % prefix)
#
def error_invalid_value_star(self):
    error(self, 'Invalid value before *')
#
def error_dict_value(self):
    error(self, 'dict can contain only key:value pairs')
#
def error_unexpected_attribute(self, name):
    error(self, 'Unexpected attribute %s:?' % name)
#
def error_unexpected_value(self, context=''):
    error(self, 'Unexpected value: %s' % context)
#
def error_end_item(self):
    error(self, "Expected space character, '[', '}' or ')' here")
#
def error_star(self):
    error(self, 'Invalid usage of symbol *')
#
def error_undefined_name(self, name):
    error(self, 'Undefined name %r' % name )
#
def error_indentation(self, idn):
    error(self, 'Invalid indentation: current position=%s ident position=%s' % (self.pos, idn))
#
def error_expected_name(self):
    error(self, 'Expected name here')
#
def error_expected_same_name(self, name):
    error(self, "Element must have same name as '%s'" % name)
#
def error_expected_complex_value(self):
    error(self, "Expected complex here")
#
def error_expected_label(self):
    error(self, "Expected label of the value")
#

def error_no_handler(name):
    sys.stderr.write('Handler for name <%s> is not registered' % name)


def error2(msg):
    sys.stderr.write('ERROR::' + msg)

def error_no_reducer(tp):
    error2('There is no reducer for this type: %r' % tp)
#
def error_reducer_wrong_type(tp):
    error2('Reducer return wrong type: %r' % tp)
#
    
def error_no_attributes(tp):
    error2('The type %r does not contain attributes' % tp)

def error_no_children(tp):
    error2('The type %r does not contain child values' % tp)
