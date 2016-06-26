############################################################################# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3
#cython: embedsignature=True

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

import axon.types as types
from axon.types import builtins
import axon.errors as errors
from axon.objects import keyval

from collections import OrderedDict as odict
from collections import MutableMapping 

IS_NAME=1
IS_KEY=0


unicode_type = types.unicode_type
str_type = types.str_type
int_type = types.int_type
long_type = types.long_type
decimal_type = types.decimal_type
bool_type = types.bool_type
float_type = types.float_type
bytes_type = types.bytes_type
bytearray_type = types.bytearray_type
none_type = types.none_type
date_type = types.date_type
time_type = types.time_type
datetime_type = types.datetime_type

simple_types = {
    unicode_type,
    str_type,
    int_type,
    long_type,
    decimal_type,
    bool_type,
    float_type,
    bytes_type,
    bytearray_type,
    none_type,
    date_type,
    time_type,
    datetime_type,
}

try:
    import cdecimal as _decimal
except:
    import decimal as _decimal

default_decimal_context = _decimal.getcontext()
_decimal2str = default_decimal_context.to_eng_string

import datetime

try:
    from base64 import encodebytes, decodebytes
except:
    from base64 import encodestring as encodebytes, decodestring as decodebytes

class PyInt:

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)
        
#
# Reducers
#

def node_reduce(o):
    return o
#
def attribute_reduce(o):
    return attribute(o.name, o.value)

_c_type_reducers = {
    Node: node_reduce,
    Attribute: attribute_reduce

    #set: set_reduce,
    #tuple: tuple_reduce,
    #list: list_reduce,
    #dict: dict_reduce,
}

c_reduce_dict = _c_type_reducers.copy()

def reset_reduce():
    c_reduce_dict = _c_type_reducers.copy()

#class Namespace(dict):
#    def __init__(self, **kw):
#        self.__dict__.update(kw)

def reduce(type_, reduce_func = None):
    if reduce_func is None:
        def _factory(factory_func):
            c_reduce_dict[type_] = factory_func
            return factory_func
        return _factory
    else:
        c_reduce_dict[type_] = reduce_func

reduce_dict = c_reduce_dict

#
#
#############################################################################
#


#import datetime

class PyPointer:
    pass

def c_new_pyptr(p):
    pyptr = PyPointer.__new__(PyPointer)
    pyptr.ptr = p
    return pyptr

# cdef unicode _dump_Name(object o):
#     return unicode(o)

def dump_default(v):
    return c_object_to_unicode(v)

c_simple_dumpers = {}

class SimpleDumper:

    def __call__(self, o):
        otype = type(o)
        if otype is unicode_type:
            return self.dump_unicode(o)
        elif otype is str_type:
            return self.dump_str(o)
        elif otype is long_type or otype is int_type:
            return self.dump_int(o)
        elif otype is float_type:
            return self.dump_float(o)
        elif otype is decimal_type:
            return self.dump_decimal(o)
        elif otype is none_type:
            return self.dump_none(o)
        elif otype is bytes_type or otype is bytearray_type:
            return self.dump_bytes(o)
        elif otype is date_type:
            return self.dump_date(o)
        elif otype is time_type:
            return self.dump_time(o)
        elif otype is datetime_type:
            return self.dump_datetime(o)
        elif otype is bool_type:
            return self.dump_bool(o)
        else:
            _dumper = c_simple_dumpers.get(otype, None)
            if _dumper is None:
                return '???'
            else:
                if type(_dumper) is PyPointer:
                    ptr = _dumper
                    text = ptr.ptr(o)
                else:
                    text = _dumper(o)
                return text

    def dump_int(self, o):
        return c_int_tostring(o)

    def dump_float(self, o):
        d = PyFloat_AS_DOUBLE(o)
        if Py_IS_FINITE(d):
            return c_object_to_unicode(o)

        if Py_IS_NAN(d):
            return '?'

        if Py_IS_INFINITY(d):
            if copysign(1.0, d) < 0:
                return '-∞'
            else:
                return '∞'

        if copysign(1.0, d) < 0:
            return '-0'

        return '0'

    def dump_decimal(self, d):
        if d.is_finite():
            val  = c_object_to_unicode(_decimal2str(d))

        elif d.is_nan():
            val = '?'

        elif d.is_infinite():
            if d.is_signed():
                val = '-∞'
            else:
                val = '∞'

        elif d.is_signed():
            val = '-0'
        else:
            val = '0'

        return val + 'D'

    def dump_bytes(self, o):
        text = PyUnicode_FromEncodedObject(encodebytes(o), 'ascii', 'strict')
        return c_as_unicode('|' + text)

    def dump_str(self, o):
        return self.dump_unicode(c_as_unicode(o))

    def dump_unicode(self, line):
        pos0 = 0
        pos = 0
        text = ''
        flag = 0

        n = c_unicode_length(line)

        if n == 0:
            return '""'
            
        while pos < n:
            ch = c_unicode_char(line, pos)
                
            if ch == '"':
                if pos != pos0:
                    text += c_unicode_substr(line, pos0, pos)
                text += '\\"'
                pos += 1
                pos0 = pos
                flag = 1
            else:
                pos += 1
            
        if pos != pos0:
            if flag:
                text += c_unicode_substr(line, pos0, pos)
            else:
                text = c_unicode_substr(line, pos0, pos)
        
        return '"' + text + '"'

    def dump_bool(self, o):
        return 'true' if o else 'false'

    def dump_date(self, o):
        d = "^%d-%02d-%02d" % (o.year, o.month, o.day)
        return d

    def _dump_tzinfo(self, o):
        offset = o.utcoffset(None)
        seconds = offset.seconds + offset.days * 86400 # 24 * 60 * 60

        if seconds < 0:
            seconds = -seconds
            sign = '-'
        else:
            sign = '+'

        minutes, seconds = builtins.divmod(seconds, 60)
        hours, minutes = builtins.divmod(minutes, 60)

        if minutes:
            return '%s%02d:%02d' % (sign, hours, minutes)
        else:
            return '%s%02d' % (sign, hours)

    def dump_time(self, o):
        if o.second:
            if o.microsecond:
                t = "^%02d:%02d:%02d.%06d" % (o.hour, o.minute, o.second, o.microsecond)
            else:
                t = "^%02d:%02d:%02d" % (o.hour, o.minute, o.second)
        else:
                t = "^%02d:%02d" % (o.hour, o.minute)

        tzinfo = o.tzinfo
        if tzinfo is not None:
            t += self._dump_tzinfo(tzinfo)

        return t

    def dump_datetime(self, o):
        if o.second:
            if o.microsecond:
                t = "^%d-%02d-%02dT%02d:%02d:%02d.%06d" % (o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond)
            else:
                t = "^%d-%02d-%02dT%02d:%02d:%02d" % (o.year, o.month, o.day, o.hour, o.minute, o.second)
        else:
                t = "^%d-%02d-%02dT%02d:%02d" % (o.year, o.month, o.day, o.hour, o.minute)

        tzinfo = o.tzinfo
        if tzinfo is not None:
            t += self._dump_tzinfo(tzinfo)

        return c_as_unicode(t)

    def dump_none(self, o):
        return 'null'

_simple_dumper = SimpleDumper()

class SimpleDumpers:
    #cdef dict c_mapping

    def __init__(self):
        self.mapping = c_simple_dumpers.copy()

    def add(self, tp, ptr):
        self.mapping[tp] = c_new_pyptr(ptr)

    def update(self, o):
        if type(o) is dict:
            self.mapping.update(o)
        elif type(o) is SimpleDumpers:
            sd = o
            self.mapping.update(sd.mapping)

def dump_as_str(tp=None):
    if tp is None:
        def _dump_as_str(func):
            c_simple_dumpers[tp] = func
            return func
        return _dump_as_str
    else:
        c_simple_dumpers[tp] = c_new_pyptr(dump_default)


#
# Dumping
#

def _dump_name(ob):
    name = ob
    pos0 = 0
    pos = 0
    text = None
    is_qname = 0

    n = len(name)
    if n == 0:
        return name
        #raise ValueError('Empty name')
        

    ch = name[pos]
    if ch.isalpha() or ch == '_':
        pos += 1
    else:
        is_qname = 1
        pos += 1

    while pos < n:
        ch = name[pos]
        if ch.isalnum() or ch == '_' or ch == '.':
            pos += 1
        elif ch == "`":
            pos += 1
            pos0 = pos
            if text is None:
                text = "\\`"
            else:
                text += "\\`"
        else:
            pos += 1
            is_qname = 1

    if pos != pos0:
        if text is None:
            text = name[pos0: pos]
        else:
            text += name[pos0: pos]
        if is_qname:
            text = "`" + text + "`"
    else:
        text = ''

    return text

def _dump_key(ob):
    pos0 = 0
    pos = 0
    text = None
    is_qname = 0
    text = None

    n = c_unicode_length(ob)
    ch = c_unicode_char(ob, pos)
    if '0' <= ch <= '9':
        pos += 1
        is_qname = 1
        
    while pos < n:
        ch = c_unicode_char(ob, pos)
        if ch.isalnum() or ch == '_':
            pos += 1
        elif ch == '"':
            if pos != pos0:
                if text is None:
                    text = c_unicode_substr(ob, pos0, pos)
                else:
                    text += c_unicode_substr(ob, pos0, pos)
            if text is None:
                text = '\\"'
            else:
                text += '\\"'
            pos += 1
            pos0 = pos
            is_qname = 1
        else:
            pos += 1
            is_qname = 1

    if pos != pos0:
        if text is None:
            text = c_unicode_substr(ob, pos0, pos)
        else:
            text += c_unicode_substr(ob, pos0, pos)

    if is_qname:
        return '"' + text + '"'
    else:
        return text

_simple_types = {
    types.unicode_type, types.str_type, types.int_type, types.long_type,
    types.float_type, types.decimal_type, types.bool_type,
    types.date_type, types.time_type, types.datetime_type}


class Dumper:
    '''
    Dumper class.
    '''
    #
    def __init__(self, fd, pretty=0, braces=0, sorted=1, hsize=0, crossref=0):

        self.crossref = 1 if crossref else 0
        self.crossref_set = None
        self.crossref_set2 = None
        self.crossref_dict = None
        self.collected = 0

        self.pretty = 0
        if pretty:
            self.pretty = 1
            if braces:
                self.pretty = 2
        #self.offset = '  '
        if self.pretty and hsize <= 0:
            self.hsize = 65000
        else:
            self.hsize = hsize
            
        self.sorted = sorted

        self.c_simple_dumpers = c_simple_dumpers
        self.c_type_reducers = c_reduce_dict

        self.fd = fd
        self.sfd = None
        if type(fd) is StringWriter:
            self.sfd = self.fd

        self.sdumper = SimpleDumper()
    #
    def is_simple_type(self, o):
        return type(o) in _simple_types or \
               (self.crossref and id(o) in self.crossref_set2)
    #
    def is_all_simple_list(self, l, n):
        for i in range(n):
            v = l[i]
            if not self.is_simple_type(v):
                return 0
        return 1
    #
    def is_all_simple_tuple(self, l, n):
        for i in range(n):
            v = l[i]
            if not self.is_simple_type(v):
                return 0
        return 1
    #
    def is_all_simple_set(self, l, n):
        for v in l:
            if not self.is_simple_type(v):
                return 0
        return 1
    #
    def write(self, sval):
        if self.sfd is None:
            self.fd.write(sval)
        else:
            self.sfd.write(sval)
    #
    def pretty_dump_crossref(self, o):
        o_id = id(o)
        if o_id in self.crossref_set:
            self.write(' &')
            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
    #
    def dump_crossref(self, o):
        o_id = id(o)
        if o_id in self.crossref_set:
            self.write('&')
            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
    #
    def dump_label(self, o):
        o_id = id(o)
        if o_id in self.crossref_set2:
            self.write('*')
            label = self.crossref_dict[o_id]
            self.write(label)
            return 1
        elif o_id in self.crossref_set:
            self.write('&')
            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
            self.crossref_set.remove(o_id)
            return 2
        else:
            return -1
    #
    def dump_value(self, o):

        flag = self.dump_simple_value(o)
        if not flag:
            otype = type(o)
            if otype is list:
                self.dump_list(o)
            elif otype is dict:
                self.dump_dict(o)
            elif otype is tuple:
                self.dump_tuple(o)
            elif otype is set:
                self.dump_set(o)
            elif otype is Node:
                self.dump_node(o)
            elif otype is axon_odict or otype is odict:
                self.dump_odict(o)
            elif otype is Attribute:
                self.dump_attribute(o)
            elif otype is KeyVal:
                self.dump_keyval(o)
            else:
                reducer = self.c_type_reducers.get(otype, None)
                if reducer is None:
                    errors.error_no_reducer(otype)
                else:
                    ob = reducer(o)
                    obtype = type(ob)
                    if obtype is list:
                        self.dump_list(ob)
                    elif obtype is dict:
                        self.dump_dict(ob)
                    elif obtype is tuple:
                        self.dump_tuple(ob)
                    elif obtype is set:
                        self.dump_set(ob)
                    elif obtype is Node:
                        self.dump_node(ob)
                    elif otype is axon_odict or obtype is odict:
                        self.dump_odict(ob)
                    elif obtype is Attribute:
                        self.dump_attribute(ob)
                    elif obtype is KeyVal:
                        self.dump_keyval(ob)
                    else:
                        errors.error_reducer_wrong_type(obtype)
    #
    def pretty_dump_value(self, o, offset, use_offset):
        new_offset = offset + '  '
        
        flag = self.dump_simple_value(o)
        if not flag:

            otype = type(o)
            if otype is list:
                self.pretty_dump_list(o, new_offset, use_offset)
            elif otype is dict:
                self.pretty_dump_dict(o, new_offset, use_offset)
            elif otype is tuple:
                self.pretty_dump_tuple(o, new_offset, use_offset)
            elif otype is set:
                self.pretty_dump_set(o, new_offset, use_offset)
            elif otype is Node:
                self.pretty_dump_node(o, new_offset, 1)
            elif otype is axon_odict or otype is odict:
                self.pretty_dump_odict(o, new_offset, use_offset)
            elif otype is Attribute:
                self.pretty_dump_attribute(o, offset, 1)
            elif otype is KeyVal:
                self.pretty_dump_keyval(o, offset, 1)
            else:
                reducer = self.c_type_reducers.get(otype, None)

                if reducer is None:
                    errors.error_no_reducer(otype)
                else:
                    ob = reducer(o)
                    obtype = type(ob)

                    if obtype is dict:
                        self.pretty_dump_dict(ob, new_offset, use_offset)
                    elif obtype is list:
                        self.pretty_dump_list(ob, new_offset, use_offset)
                    elif obtype is tuple:
                        self.pretty_dump_tuple(ob, new_offset, use_offset)
                    elif obtype is set:
                        self.pretty_dump_set(ob, new_offset, use_offset)
                    elif obtype is Node:
                        self.pretty_dump_node(ob, new_offset, 1)
                    elif otype is axon_odict or otype is odict:
                        self.pretty_dump_odict(o, new_offset, use_offset)
                    elif obtype is Attribute:
                        self.pretty_dump_attribute(ob, offset, 1)
                    elif obtype is KeyVal:
                        self.pretty_dump_keyval(ob, offset, 1)
                    else:
                        errors.error_reducer_wrong_type(obtype)
    #
    def dump_simple_value(self, o):
    
        if self.crossref:
            if self.dump_label(o) == 1:
                return 1
    
        otype = type(o)
        dumper = self.sdumper
        if otype is unicode_type:
            text = dumper.dump_unicode(o)
            self.write(text)
            return 1
        elif otype is str_type:
            text = dumper.dump_str(o)
            self.write(text)
            return 1
        elif otype is long_type or otype is int_type:
            text = dumper.dump_int(o)
        elif otype is float_type:
            text = dumper.dump_float(o)
        elif otype is decimal_type:
            text = dumper.dump_decimal(o)
        elif otype is none_type:
            text = dumper.dump_none(o)
        elif otype is bytes_type or otype is bytearray_type:
            text = dumper.dump_bytes(o)
        elif otype is date_type:
            text = dumper.dump_date(o)
        elif otype is time_type:
            text = dumper.dump_time(o)
        elif otype is datetime_type:
            text = dumper.dump_datetime(o)
        elif otype is bool_type:
            text = dumper.dump_bool(o)
        else:
            _dumper = c_simple_dumpers.get(otype, None)
            if _dumper is None:
                return 0
            else:
                if type(_dumper) is PyPointer:
                    ptr = _dumper
                    text = ptr.ptr(o)
                else:
                    text = _dumper(o)

        self.write(text)
        return 1
    #
    def dump_attribute(self, attr):
        self.write(_dump_name(attr.name))
        self.write(':')
        self.dump_value(attr.val)

    def pretty_dump_attribute(self, attr, offset, use_offset):
        self.write(_dump_name(attr.name))
        self.write(': ')
        self.pretty_dump_value(attr.val, offset, 1)
    #
    def dump_keyval(self, attr):
        self.write(_dump_key(attr.key))
        self.write(':')
        self.dump_value(attr.val)

    def pretty_dump_keyval(self, attr, offset, use_offset):
        self.write(_dump_key(attr.key))
        self.write(': ')
        self.pretty_dump_value(attr.val, offset, 1)
    #
    def dump_dict_values(self, d):
        i = 0

        items = d.items()        
        if self.sorted:
            items = sorted(items)

        for k,v in items:
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))

            self.write(':')

            self.dump_value(v)
            i += 1
    #
    def dump_attrs_sequence(self, d):
        i = 0

        for k,v in d.items():
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_name(text))

            self.write(':')

            self.dump_value(v)
            i += 1
    #
    def dump_list_sequence(self, l):
        i = 0
        for v in l:
            if i > 0:
                self.write(' ')
            self.dump_value(v)
            i += 1
    #
    def dump_set_sequence(self, l):
        i = 0
        for v in l:
            if i > 0:
                self.write(' ')
            self.dump_value(v)
            i += 1
    #
    def dump_tuple_sequence(self, l):
        i = 0
        for v in l:
            if i > 0:
                self.write(' ')
            self.dump_value(v)
            i += 1
    #
    def dump_node(self, o):
        if reserved_name_dict.get(o.name, c_undefined) is not c_undefined:
            self.write("'")
            self.write(_dump_name(o.name))
            self.write("'")
        else:
            self.write(_dump_name(o.name))
        self.write('{')
        if o.attrs:
            self.dump_attrs_sequence(o.attrs)
        if o.vals:
            if o.attrs:
                self.write(' ')
            self.dump_list_sequence(o.vals)
        self.write('}')
    #
    def dump_list(self, l):
        self.write('[')
        self.dump_list_sequence(l)
        self.write(']')
    #
    def dump_set(self, l):
        if not l:
            self.write('∅')
        else:
            self.write('{')
            self.dump_set_sequence(l)
            self.write('}')
    #    
    def dump_dict(self, d):
        self.write('{')
        self.dump_dict_values(d)
        self.write('}')
    #
    def dump_odict(self, d):
        self.write('[')
        if d:
            self.dump_dict_values(d)
        else:
            self.write(':')
        self.write(']')
    #
    def dump_tuple(self, d):
        self.write('(')
        self.dump_tuple_sequence(d)
        self.write(')')
    #
    def pretty_dump_node(self, o, w, use_offset):
        if reserved_name_dict.get(o.name, c_undefined) is not c_undefined:
            self.write("`")
            self.write(_dump_name(o.name))
            self.write("`")
        else:
            self.write(_dump_name(o.name))

        n, m = 0, 0
        if o.attrs is not None:
            m = len(o.attrs)
        if o.vals is not None:
            n = len(o.vals)

        if m == 0:
            if n == 0:
                if self.pretty == 2:
                    self.write(' {}')
                return
            elif n == 1:
                v = o.vals[0]
                if self.is_simple_type(v):
                    self.write(' {')
                    self.dump_value(v)
                    self.write('}')
                    return
            
        if self.pretty == 1:
            if n > 0 or m > 0:
                self.write('\n')
                self.write(w)
            # else:
            #     self.write(':')
        elif self.pretty == 2:
            self.write(' {')
            if m == 0 and n <= self.hsize and self.is_all_simple_list(o.vals, n):
                use_offset = 0
            elif m == 0 and n == 1 and self.is_simple_type(o.vals[0]):
                use_offset = 0
            if use_offset:
                self.write('\n')
                self.write(w)

        if o.attrs:
            self.pretty_dump_node_attrs(o.attrs, w, use_offset)
        if o.vals:
            if o.attrs:
                self.write('\n')
                self.write(w)                
            self.pretty_dump_node_sequence(o.vals, w, use_offset)

        if self.pretty == 2:
            self.write('}')
    #
    def pretty_dump_node_sequence(self, l, w, use_offset):
        n = len(l)
        if n == 0:
            return
        elif n == 1:
            v = l[0]
            if self.is_simple_type(v):
                self.dump_simple_value(v)
            else:
                self.pretty_dump_value(v, w, 0)
            return
        elif n <= self.hsize and self.is_all_simple_list(l, n):
            for i in range(n):
                v = l[i]
                if i > 0:
                    self.write(' ')
                self.dump_simple_value(v)
            return

        j = 0
        flag = 0
        for i in range(n):
        
            v = l[i]

            use_offset = 0
            if i > 0:
                if not flag or j >= self.hsize:
                    use_offset = 1
                    j = 0
                
                flag = self.is_simple_type(v)
                if not flag:
                    use_offset = 1
            else:
                flag = self.is_simple_type(v)

            if use_offset:
                self.write('\n')
                self.write(w)
            else:
                if j > 0:
                    self.write(' ')
                                
            self.pretty_dump_value(v, w, 0)

            j += 1
    #
    def pretty_dump_node_attrs(self, attrs, w, use_offset):
        n = len(attrs)
        if n == 0:
            return
        elif n == 1:
            for name, val in attrs.items():            
                if self.is_simple_type(val):
                    text = c_as_unicode(name)
                    self.write(_dump_name(text))
                    self.write(': ')
                    self.dump_simple_value(val)
                    return
                else:
                    break

        j = 0
        for name, val in attrs.items():
            if j > 0:
                self.write('\n')
                self.write(w)
                                        
            text = c_as_unicode(name)
            self.write(_dump_name(text))
            
            self.write(': ')
            
            self.pretty_dump_value(val, w, 1)

            j += 1
    #
    def pretty_dump_set(self, l, w, use_offset):
        if not l:
            self.write('∅')
        else:
            self.write('{')
            self.pretty_dump_set_sequence(l, w, use_offset)
            self.write('}')
    #    
    def pretty_dump_set_sequence(self, l, w, use_offset):
        n = len(l)
        if n == 0:
            return
        elif n == 1:
            for v in l:
                if self.is_simple_type(v):
                    self.dump_simple_value(v)
                else:
                    self.pretty_dump_value(v, w, 0)
            return
            
        if n <= self.hsize and self.is_all_simple_set(l, n):
            i = 0
            for v in l:
                if i > 0:
                    self.write(' ')
                self.dump_simple_value(v)
                i += 1
            return

        j = 0
        flag = 0
        i = 0
        for v in l:
        
            if i > 0:
                if not flag or j >= self.hsize:
                    use_offset = 1
                    j = 0
                
                flag = self.is_simple_type(v)
                if not flag:
                    use_offset = 1

            else:
                flag = self.is_simple_type(v)

            if use_offset:
                self.write('\n')
                self.write(w)
            else:
                self.write(' ')
                                
            self.pretty_dump_value(v, w, 0)

            j += 1
    #    
    def pretty_dump_list(self, l, w, use_offset):
        self.write('[')
        self.pretty_dump_list_sequence(l, w, use_offset)
        self.write(']')
    #    
    def pretty_dump_list_sequence(self, l, w, use_offset):
        n = len(l)
        if n == 0:
            return
        elif n == 1:
            v = l[0]
            if self.is_simple_type(v):
                self.dump_simple_value(v)
            else:
                self.pretty_dump_value(v, w, 0)
            return
            
        if n <= self.hsize and self.is_all_simple_list(l, n):
            for i in range(n):
                v = l[i]
                if i > 0:
                    self.write(' ')
                self.dump_simple_value(v)
            return

        j = 0
        flag = 0
        for i in range(n):
        
            v = l[i]

            if i > 0:
                if not flag or j >= self.hsize:
                    use_offset = 1
                    j = 0
                
                flag = self.is_simple_type(v)
                if not flag:
                    use_offset = 1

            else:
                flag = self.is_simple_type(v)

            if use_offset:
                self.write('\n')
                self.write(w)
            else:
                self.write(' ')
                                
            self.pretty_dump_value(v, w, 0)

            j += 1
    #
    def pretty_dump_dict(self, d, w, use_offset):
        self.write('{')
        self.pretty_dump_dict_values(d, w, use_offset)
        self.write('}')
    #
    def pretty_dump_odict(self, d, w, use_offset):
        self.write('[')
        if d:
            self.pretty_dump_dict_values(d, w, use_offset)
        else:
            self.write(':')
        self.write(']')
    #
    def pretty_dump_dict_values(self, d, w, use_offset):
        n = len(d)
        if n == 0:
            return
        elif n == 1:
            for key, val in d.items():            
                if self.is_simple_type(val):
                    text = c_as_unicode(key)
                    self.write(_dump_key(text))
                    self.write(': ')
                    self.dump_simple_value(val)
                    return
                else:
                    break

        items = d.items()        
        if self.sorted:
            items = sorted(items)

        i = 0
        for k, v in items:
        
            if i > 0:
                use_offset = 1

            if use_offset:
                self.write('\n')
                self.write(w)
            else:
                if n > 1:
                  self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))
            
            self.write(': ')
            
            self.pretty_dump_value(v, w, 1)

            i += 1
    #
    def pretty_dump_tuple(self, l, w, use_offset):
        self.write('(')
        self.pretty_dump_list_sequence(list(l), w, use_offset)
        self.write(')')
    #
    def dump(self, seq):
        '''
        Main dumping method.

        :param seq:

            Sequence of values to dump

        :param pretty:

            Flag indicates whether to use pretty dumping mode. Default is `False` (i.e. no pretty dumping)

        '''

        if self.crossref:
            self.collect(seq)
            self.apply_crossref()
        
        is_mapping = 0
        if isinstance(seq, MutableMapping):
            is_mapping = 1
            
        if is_mapping:
            if self.sorted and seq is dict:
                iterseq = iter(sorted(seq.items()))
            else:
                iterseq = iter(seq.items())
        else:
            iterseq = iter(seq)

        v = next(iterseq)
        if is_mapping:
            v = keyval(*v)

        if self.pretty:
            self.pretty_dump_value(v, '', 0)
        else:
            self.dump_value(v)

        if self.pretty:
            for v in iterseq:
                if is_mapping:
                    v = keyval(*v)
                self.write('\n')
                self.pretty_dump_value(v, '', 0)
        else:
            for v in iterseq:
                if is_mapping:
                    v = keyval(*v)
                self.write('\n')
                self.dump_value(v)
    #
    def apply_crossref(self):
        crossref_set = set()
        for o_ref, count in self.crossref_dict.items():
            if count.val > 1:
                crossref_set.add(o_ref)

        crossref_dict = {}
        i = 0
        for o_ref in crossref_set:
            i += 1
            crossref_dict[o_ref] = unicode(i)

        self.crossref_set = crossref_set
        self.crossref_dict = crossref_dict
        self.crossref_set2 = set()
    #
    def collect_value(self, o):

        otype = type(o)
        if otype in simple_types:
            return 0

        ref_o = id(o)
        count = self.crossref_dict.get(ref_o, None)
        if count is None:
            count = PyInt(1)
            self.crossref_dict[ref_o] = count
        else:
            count.val += 1
            self.crossref_dict[ref_o] = count
            # if count.val == 2:
            #     print(o)
            return 0

        if otype is list:
            self.collect_list(o)
        elif otype is dict:
            self.collect_dict(o)
        elif otype is axon_odict:
            self.collect_odict(o)
        elif otype is tuple:
            self.collect_tuple(o)
        elif otype is set:
            self.collect_set(o)
        elif otype is Node:
            self.collect_node(o)
        elif otype is Attribute:
            self.collect_attribute(o)
        elif otype is KeyVal:
            self.collect_keyval(o)
        else:
            reducer = self.c_type_reducers.get(otype, None)
            if reducer is None:
                errors.error_no_reducer(otype)
            else:
                ro = reducer(o)
                rotype = type(ro)
                if rotype is Node:
                    self.collect_node(ro)
                elif rotype is Attribute:
                    self.collect_attribute(ro)
                elif rotype is KeyVal:
                    self.collect_keyval(o)
                else:
                    errors.error_reducer_wrong_type(rotype)
    #
    def collect_list(self, lst):
        for v in lst:
            self.collect_value(v)
    #
    def collect_tuple(self, lst):
        for v in lst:
            self.collect_value(v)
    #
    def collect_set(self, lst):
        for v in lst:
            self.collect_value(v)
    #
    def collect_dict(self, d):
        for v in d.values():
            self.collect_value(v)
    #
    def collect_odict(self, d):
        for v in d.values():
            self.collect_value(v)
    #
    def collect_attribute(self, ob):
        self.collect_value(ob.val)
    #
    def collect_keyval(self, ob):
        self.collect_value(ob.val)
    #
    def collect_node(self, ob):
        if ob.attrs:
            self.collect_odict(ob.attrs)
        if ob.vals:
            self.collect_list(ob.vals)
    #
    def collect(self, values):
        self.crossref_dict = {}
        for v in values:
            self.collect_value(v)


