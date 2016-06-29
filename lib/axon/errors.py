# coding: utf-8

# The MIT License (MIT)
# 
# Copyright (c) <2011-2015> <Shibzukhov Zaur, szport at gmail dot com>
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

class AxonError(Exception):
    #
    def __init__(self, msg, pos=None, chunk=''):
        self.msg = msg
        self.pos = pos
        self.chunk = chunk
    #
    def __str__(self):
        text = 'ERROR:: ' + self.msg
        if self.pos is not None:
            lnum, pos = self.pos
            text +=  ' line:%s pos:%s' % (lnum, pos)
        if self.chunk:
            text +=  ' chunk: %s' % self.chunk
        return text

def error(self, msg):
    e = AxonError(msg, (self.lnum, self.pos), self.line[self.pos:self.pos+16])
    if sys.flags.debug:
        self.errto.write(str(e))
    raise e
#
# def error_getvalue(self):
#     error(self, 'Invalid simple value')
#
def error_unexpected_end_complex_value(self):
    error(self, 'Unexpected end inside complex value')
#
def error_unexpected_end_list(self):
    error(self, 'Unexpected end inside list')
#
def error_unexpected_end_odict(self):
    error(self, 'Unexpected end inside ordered dict')
#
def error_unexpected_end_tuple(self):
    error(self, 'Unexpected end inside tuple')
#
def error_unexpected_end_string(self):
    error(self, 'Unexpected end of the string')
#
def error_unexpected_keyval(self):
    error(self, 'Unexpected key:val')
#
def error_expected_keyval(self):
    error(self, 'Expected key:val')
#
def error_expected_key(self):
    error(self, 'Expected key')
#
def error_expected_named_constant(self):
    error(self, 'Expected named constant')
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
    error(self, 'Invalid %s value' % vtype.__name__)
#
def error_invalid_odict(self, vtype=''):
    error(self, 'Invalid ordered dict')
#
def error_invalid_value_with_prefix(self, prefix):
    error(self, "Invalid value with prefix '%s'" % prefix)
#
def error_dict_value(self):
    error(self, 'dict can contain only key:value pairs')
#
def error_unexpected_attribute(self, name):
    error(self, 'Unexpected attribute %s:?' % name)
#
def error_expected_attribute(self):
    error(self, 'Expected attribute')
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

def error2(msg):
    e = AxonError(msg)
    if sys.flags.debug:
        self.errto.write(str(e))
    raise e

def error_no_handler(name):
    error2('Handler for name <%s> is not registered' % name)

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
