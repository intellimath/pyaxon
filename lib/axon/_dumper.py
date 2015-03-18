# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3

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

import axon.types as types
from axon.types import builtins
import axon.errors as errors

from collections import OrderedDict as odict

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

def mapping_reduce(o):
    return o
#
def element_reduce(o):
    return o
#
def sequence_reduce(o):
    return o
#
def instance_reduce(o):
    return o
#
def empty_reduce(o):
    return o

_c_type_reducers = {
    Mapping: mapping_reduce,
    Element: element_reduce,
    Sequence: sequence_reduce,
    Instance: instance_reduce,
    Empty: empty_reduce,

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

# cdef void _dump_attribute(Attribute attr, Dumper dumper):
#     dumper.write(_dump_name(attr.c_name))
#     dumper.write(':')
#     dumper._dump(attr.c_value)
#
# cdef void _pretty_dump_attribute(Attribute attr, Dumper dumper, unicode offset):
#     dumper.write(_dump_name(attr.c_name))
#     dumper.write(': ')
#     dumper._pertty_dump(attr.c_value, offset, 0)

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
        if isfinite(d):
            return c_object_to_unicode(o)

        if isnan(d):
            return '?'

        if isinf(d):
            if signbit(d):
                return '-∞'
            else:
                return '∞'

        if signbit(d):
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
#         is_id = 1

        n = c_unicode_length(line)

        if n == 0:
            return '""'

#         ch = c_unicode_char(line, pos)
#         pos += 1
#         if not ch.isalpha() and not ch == '_':
#             is_id = 0
            
        while pos < n:
            ch = c_unicode_char(line, pos)
#             if ch.isalnum() or ch == '_':
#                 pos += 1
#                 continue
                
            if ch == '"':
                if pos != pos0:
                    text += c_unicode_substr(line, pos0, pos)
                text += '\\"'
                pos += 1
                pos0 = pos
                flag = 1
            else:
                pos += 1
            
#             is_id = 0

        if pos != pos0:
            if flag:
                text += c_unicode_substr(line, pos0, pos)
            else:
                text = c_unicode_substr(line, pos0, pos)
        
#         if is_id:
#             return text
#         else:
#             return '"' + text + '"'
        return '"' + text + '"'

    def dump_bool(self, o):
        #return '⊤' if o else '⊥'
        return 'true' if o else 'false'

    def dump_date(self, o):
        d = "%d-%02d-%02d" % (o.year, o.month, o.day)
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
                t = "%02d:%02d:%02d.%06d" % (o.hour, o.minute, o.second, o.microsecond)
            else:
                t = "%02d:%02d:%02d" % (o.hour, o.minute, o.second)
        else:
                t = "%02d:%02d" % (o.hour, o.minute)

        tzinfo = o.tzinfo
        if tzinfo is not None:
            t += self._dump_tzinfo(tzinfo)

        return t

    def dump_datetime(self, o):
        if o.second:
            if o.microsecond:
                t = "%d-%02d-%02dT%02d:%02d:%02d.%06d" % (o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond)
            else:
                t = "%d-%02d-%02dT%02d:%02d:%02d" % (o.year, o.month, o.day, o.hour, o.minute, o.second)
        else:
                t = "%d-%02d-%02dT%02d:%02d" % (o.year, o.month, o.day, o.hour, o.minute)

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
        raise ValueError('Empty name')

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
        elif ch == "'":
            pos += 1
            pos0 = pos
            text += r"\'"
        else:
            pos += 1
            is_qname = 1

    if pos != pos0:
        if text is None:
            text = name[pos0: pos]
        else:
            text += name[pos0: pos]
        if is_qname:
            text = "'" + text + "'"

    return text

def _dump_key(ob):
    pos0 = 0
    pos = 0
    text = None
    is_qname = 0

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
    Dumper class
    '''
    #
    def __init__(self, fd, pretty=0, braces=0, sorted=1, hsize=0, crossref=0):

        #self.max_size = 65000

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
    def write(self, sval):
        if self.sfd is None:
            self.fd.write(sval)
        else:
            self.sfd.write(sval)
    #
    def _pretty_dump_crossref(self, o):
        o_id = id(o)
        if o_id in self.crossref_set:
            self.write(' &')
            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
    #
    def _dump_crossref(self, o):
        o_id = id(o)
        if o_id in self.crossref_set:
            self.write('&')
            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
    #
    def _dump_label(self, o):
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
    def _dump(self, o):

        flag = self._dump_value(o)
        if not flag:
            otype = type(o)
            if otype is list:
                self.dump_list(o)
            elif otype is dict:
                self.dump_dict(o)
            elif otype is tuple:
                self.dump_tuple(o)
            elif otype is axon_odict or otype is odict:
                self.dump_odict(o)
            #elif otype is set:
            #    self.dump_set(o)
            elif otype is Mapping:
                self.dump_mapping(o)
            elif otype is Sequence:
                self.dump_sequence(o)
            elif otype is Element:
                self.dump_element(o)
            elif otype is Instance:
                self.dump_instance(o)
            elif otype is Empty:
                self.dump_empty(o)
            else:
                reducer = self.c_type_reducers.get(otype, None)
                if reducer is None:
                    errors.error_no_reducer(otype)
                else:
                    ob = reducer(o)
                    obtype = type(ob)
                    if obtype is Mapping:
                        self.dump_mapping(ob)
                    elif obtype is Sequence:
                        self.dump_sequence(ob)
                    elif obtype is Element:
                        self.dump_element(ob)
                    elif obtype is Instance:
                        self.dump_instance(ob)
                    elif obtype is Empty:
                        self.dump_empty(ob)
                    elif obtype is dict:
                        self.dump_dict(ob)
                    elif obtype is list:
                        self.dump_list(ob)
                    elif obtype is tuple:
                        self.dump_tuple(ob)
                    elif otype is axon_odict or obtype is odict:
                        self.dump_odict(ob)
                    else:
                        errors.error_reducer_wrong_type(obtype)
    #
    def _pretty_dump(self, o, offset, use_offset):
        new_offset = offset + '  '
        
        flag = self._dump_value(o)
        if not flag:

            otype = type(o)
            if otype is list:
                self.pretty_dump_list(o, new_offset, use_offset)
            elif otype is dict:
                self.pretty_dump_dict(o, new_offset, use_offset)
            elif otype is tuple:
                self.pretty_dump_tuple(o, new_offset, use_offset)
            elif otype is axon_odict or otype is odict:
                self.pretty_dump_odict(o, new_offset, use_offset)
            #elif otype is set:
            #    self.pretty_dump_set(o, new_offset, not use_offset)
            elif otype is Mapping:
                self.pretty_dump_mapping(o, new_offset, use_offset)
            elif otype is Sequence:
                self.pretty_dump_sequence(o, new_offset, use_offset)
            elif otype is Element:
                self.pretty_dump_element(o, new_offset, use_offset)
            elif otype is Instance:
                self.pretty_dump_instance(o, new_offset, use_offset)
            elif otype is Empty:
                self.pretty_dump_empty(o, new_offset, use_offset)
            else:
                reducer = self.c_type_reducers.get(otype, None)

                if reducer is None:
                    errors.error_no_reducer(otype)
                else:
                    ob = reducer(o)
                    obtype = type(ob)

                    if obtype is Mapping:
                        self.pretty_dump_mapping(ob, new_offset, use_offset)
                    elif obtype is Sequence:
                        self.pretty_dump_sequence(ob, new_offset, use_offset)
                    elif obtype is Element:
                        self.pretty_dump_element(ob, new_offset, use_offset)
                    elif obtype is Instance:
                        self.pretty_dump_instance(ob, new_offset, use_offset)
                    elif obtype is Empty:
                        self.pretty_dump_empty(ob, new_offset, use_offset)
                    elif obtype is dict:
                        self.pretty_dump_dict(ob, new_offset, use_offset)
                    elif obtype is list:
                        self.pretty_dump_list(ob, new_offset, use_offset)
                    elif obtype is tuple:
                        self.pretty_dump_tuple(ob, new_offset, use_offset)
                    elif otype is axon_odict or otype is odict:
                        self.pretty_dump_odict(o, new_offset, use_offset)
                    else:
                        errors.error_reducer_wrong_type(obtype)
    #
    def _dump_value(self, o):
    
        if self.crossref:
            if self._dump_label(o) == 1:
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
    def _dump_attributes(self, d):
        i = 0

        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        for k,v in items:
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_name(text))

            self.write(':')

            self._dump(v)
            i += 1
    #
    def _dump_dict_values(self, d):
        i = 0

        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        for k,v in items:
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))

            self.write(':')

            self._dump(v)
            i += 1
    #
    def _dump_odict_values(self, d):
        i = 0

        for k,v in d.items():
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))

            self.write(':')

            self._dump(v)
            i += 1
    #
    def _dump_list_sequence(self, l):
        i = 0
        for v in l:
            if i > 0:
                self.write(' ')
            self._dump(v)
            i += 1
    #
    def _dump_set_sequence(self, l):
        i = 0
        for v in l:
            if i > 0:
                self.write(' ')
            self._dump(v)
            i += 1
    #
    def _dump_tuple_sequence(self, l):
        i = 0
        for v in l:
            if i > 0:
                self.write(' ')
            self._dump(v)
            i += 1
    #
    def dump_mapping(self, o):
        self.write(_dump_name(o.name))
        self.write('{')
        self._dump_attributes(o.mapping)
        self.write('}')
    #
    def dump_element(self, o):
        self.write(_dump_name(o.name))
        self.write('{')
        self._dump_attributes(o.mapping)
        if o.sequence:
            self.write(' ')
            self._dump_list_sequence(o.sequence)
        self.write('}')
    #
    def dump_sequence(self, o):
        self.write(_dump_name(o.name))
        self.write('{')
        self._dump_list_sequence(o.sequence)
        self.write('}')
    #
    def dump_instance(self, o):
        self.write(_dump_name(o.name))
        self.write('{')
        self._dump_tuple_sequence(o.sequence)
        if o.mapping:
            self.write(' ')
            self._dump_attributes(o.mapping)
        self.write('}')
    #
    def dump_empty(self, o):
        self.write(_dump_name(o.name))
        self.write('{}')
    #
    def dump_list(self, l):
        self.write('[')
        self._dump_list_sequence(l)
        self.write(']')
    #
    def dump_dict(self, d):
        self.write('{')
        self._dump_dict_values(d)
        self.write('}')
    #
    def dump_odict(self, d):
        self.write('<')
        self._dump_odict_values(d)
        self.write('>')
    #
    def dump_tuple(self, d):
        self.write('(')
        self._dump_tuple_sequence(d)
        self.write(')')
    #
    def _pretty_dump_attributes(self, d, w):
        if len(d) == 0: 
            return 0

        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        i = 0
        j = 0
        for k,v in items:
        
            if i > 0:
                if self.hsize: 
                    if j >= self.hsize:
                        use_offset = 1
                        j = 0
                    else:
                        use_offset = 1
                else:
                    use_offset = 1

                if use_offset:
                    self.write('\n')
                    self.write(w)
                else:
                    self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_name(text))
            
            self.write(': ')
            
            self._pretty_dump(v, w, 0)

            i += 1
            j += 1
    #
    def _pretty_dump_dict_values(self, d, w):
        if len(d) == 0: 
            return 0

        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()            

        i = 0
        j = 0
        for k,v in items:
        
            if i > 0:
                if self.hsize: 
                    if j >= self.hsize:
                        use_offset = 1
                        j = 0
                    else:
                        use_offset = 1
                else:
                    use_offset = 1

                if use_offset:
                    self.write('\n')
                    self.write(w)
                else:
                    self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))
            
            self.write(': ')
            
            self._pretty_dump(v, w, 0)

            i += 1
            j += 1
    #
    def _pretty_dump_odict_values(self, d, w):
        if len(d) == 0: 
            return 0

        i = 0
        j = 0
        for k,v in d.items():
        
            if i > 0:
                if self.hsize: 
                    if j >= self.hsize:
                        use_offset = 1
                        j = 0
                    else:
                        use_offset = 1
                else:
                    use_offset = 1

                if use_offset:
                    self.write('\n')
                    self.write(w)
                else:
                    self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))
            
            self.write(': ')
            
            self._pretty_dump(v, w, 0)

            i += 1
            j += 1
    #
    def _pretty_dump_list_sequence(self, l, w):
        n = len(l)
        if n == 0:
            return 0
        elif n == 1:
            v = l[0]
            if self.is_simple_type(v):
                self._dump_value(v)
            else:
                self._pretty_dump(v, w, 1)
            return 0
        elif n <= self.hsize and self.is_all_simple_list(l, n):
            for i in range(n):
                v = l[i]
                if i > 0:
                    self.write(' ')
                self._dump_value(v)
            return 0

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

                if use_offset:
                    self.write('\n')
                    self.write(w)
                else:
                    if j > 0:
                        self.write(' ')
            else:
                flag = self.is_simple_type(v)
                                
            self._pretty_dump(v, w, 1)

            j += 1
    #
    def _pretty_dump_tuple_sequence(self, l, w):
        n = len(l)
        if n == 0:
            return 0
        elif n == 1:
            v = l[0]
            flag = self.is_simple_type(v)
            if flag:
                self._dump_value(v)
            else:
                self._pretty_dump(v, w, 1)
            return 0
        elif n <= self.hsize:
            if self.is_all_simple_tuple(l, n):
                for i in range(n):
                    v = l[i]
                    if i > 0:
                        self.write(' ')
                    self._dump_value(v)
                return 0
            
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

                if use_offset:
                    self.write('\n')
                    self.write(w)
                else:
                    if j > 0:
                        self.write(' ')
            else:
                flag = self.is_simple_type(v)
                
            self._pretty_dump(v, w, 1)

            j += 1
    #
    def pretty_dump_mapping(self, o, w, use_offset):
        self.write(_dump_name(o.name))

        if self.pretty == 1:
            self.write(':\n')
            self.write(w)
        elif self.pretty == 2:
            self.write(' {')
            self.write('\n')
            self.write(w)


        self._pretty_dump_attributes(o.mapping, w)

        if self.pretty == 2:
            self.write('}')
    #
    def pretty_dump_element(self, o, w, use_offset):
        self.write(_dump_name(o.name))

        if self.pretty == 1:
            self.write(':\n')
            self.write(w)
        elif self.pretty == 2:
            self.write(' {\n')
            self.write(w)

        self._pretty_dump_attributes(o.mapping, w)
        if o.sequence:
            self.write('\n')
            self.write(w)
            self._pretty_dump_list_sequence(o.sequence, w)

        if self.pretty == 2:
            self.write('}')
    #
    def pretty_dump_sequence(self, o, w, use_offset):
        self.write(_dump_name(o.name))

        if self.pretty == 1:
            self.write(':\n')
            self.write(w)
        elif self.pretty == 2:
            self.write(' {')
            n = len(o.sequence)
            if n <= self.hsize and self.is_all_simple_list(o.sequence, n):
                use_offset = 0
            elif n == 1 and self.is_simple_type(o.sequence[0]):
                use_offset = 0
            if use_offset:
                self.write('\n')
                self.write(w)

        self._pretty_dump_list_sequence(o.sequence, w)

        if self.pretty == 2:
            self.write('}')
    #
    def pretty_dump_instance(self, o, w, use_offset):
        self.write(_dump_name(o.name))

        if self.pretty == 1:
            self.write(':\n')
            self.write(w)
        elif self.pretty == 2:
            self.write(' {')
            if use_offset:
                self.write('\n')
                self.write(w)

        self._pretty_dump_tuple_sequence(o.sequence, w)
        self.write('\n')
        self.write(w)
        if o.mapping:
            self._pretty_dump_attributes(o.mapping, w)

        if self.pretty == 2:
            self.write('}')
    #
    def pretty_dump_empty(self, o, w, use_offset):
        self.write(_dump_name(o.name))

        if self.pretty == 1:
            self.write(':')
            #self.write(w)
        elif self.pretty == 2:
            self.write(' {}')

    #
    def pretty_dump_list(self, l, w, use_offset):
        self.write('[')
        
        use_offset = 1 - use_offset
        
        n = len(l)
        if n == 1:
            if not self.is_simple_type(l[0]):
                self.write(' ')
        elif self.hsize and n <= self.hsize and self.is_all_simple_list(l, n):
            pass            
        elif use_offset:
            self.write('\n')
            self.write(w)
        elif n > 0:
            self.write(' ')
            
        self._pretty_dump_list_sequence(l, w)
        self.write(']')
    #
    def pretty_dump_dict(self, d, w, use_offset):
        self.write('{')
        n = len(d)
        if n > 1:
            if use_offset:
                self.write(' ')
            else:
                self.write('\n')
                self.write(w)
        self._pretty_dump_dict_values(d, w)
        self.write('}')
    #
    def pretty_dump_odict(self, d, w, use_offset):
        self.write('<')
        n = len(d)
        if n > 1:
            if use_offset:
                self.write(' ')
            else:
                self.write('\n')
                self.write(w)
        self._pretty_dump_odict_values(d, w)
        self.write('>')
    #
    def pretty_dump_tuple(self, l, w, use_offset):
        self.write('(')
        
        use_offset = 1 - use_offset
        
        n = len(l)
        if n == 1:
            if not self.is_simple_type(l[0]):
                self.write(' ')
        elif self.hsize and n <= self.hsize and self.is_all_simple_tuple(l, n):
            pass
        elif use_offset:
            self.write('\n')
            self.write(w)
        elif n > 1:
            self.write(' ')

        self._pretty_dump_tuple_sequence(l, w)
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

        iterseq = iter(seq)
        v = next(iterseq)

        if self.pretty:
            self._pretty_dump(v, '', 1)
        else:
            self._dump(v)

        if self.pretty:
            for v in iterseq:
                self.write('\n')
                self._pretty_dump(v, '', 1)
        else:
            for v in iterseq:
                self.write('\n')
                self._dump(v)
    #
    def apply_crossref(self):
        crossref_set = set()
        crossref_set2 = set()
        for o_ref, count in self.crossref_dict.items():
            if count.val > 1:
                crossref_set.add(o_ref)

        crossref_dict = {}
        i = 0
        for o_ref in crossref_set:
            i += 1
            crossref_dict[o_ref] = unicode(i)

        self.crossref_set = crossref_set
        self.crossref_set2 = crossref_set2
        self.crossref_dict = crossref_dict
        crossref_dict = None
        crossref_set = None
        crossref_set2 = None
    #
    def _collect(self, o):

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
            return 0

        if otype is list:
            self._collect_list(o)
        elif otype is dict:
            self._collect_dict(o)
        elif otype is tuple:
            self._collect_tuple(o)
        elif otype is set:
            self._collect_set(o)
        elif otype is Element:
            self._collect_element(o)
        elif otype is Mapping:
            self._collect_mapping(o)
        elif otype is Sequence:
            self._collect_sequence(o)
        elif otype is Instance:
            self._collect_instance(o)
        elif otype is Empty:
            pass
        else:
            reducer = self.c_type_reducers.get(otype, None)
            if reducer is None:
                errors.error_no_reducer(otype)
            else:
                ro = reducer(o)
                rotype = type(ro)
                if rotype is Element:
                    self._collect_element(ro)
                elif rotype is Mapping:
                    self._collect_mapping(ro)
                elif rotype is Sequence:
                    self._collect_sequence(ro)
                elif rotype is Instance:
                    self._collect_instance(ro)
                elif rotype is Empty:
                    pass
                else:
                    errors.error_reducer_wrong_type(rotype)
    #
    def _collect_list(self, lst):
        for v in lst:
            self._collect(v)
    #
    def _collect_tuple(self, lst):
        for v in lst:
            self._collect(v)
    #
    def _collect_set(self, lst):
        for v in lst:
            self._collect(v)
    #
    def _collect_dict(self, d):
        for v in d.values():
            self._collect(v)
    #
    def _collect_element(self, ob):
        self._collect_dict(ob.mapping)
        self._collect_list(ob.sequence)
    #
    def _collect_instance(self, ob):
        self._collect_tuple(ob.sequence)
        self._collect_dict(ob.mapping)
    #
    def _collect_mapping(self, ob):
        self._collect_dict(ob.mapping)
    #
    def _collect_sequence(self, ob):
        self._collect_list(ob.sequence)
    #
    def _collect_empty(self, ob):
        pass
    #
    def collect(self, values):
        self.crossref_dict = {}
        for v in values:
            self._collect(v)


# def dump_atomic(o):
#     otype = type(o)
#     dumper  = c_simple_dumpers.get(otype, None)
#     if dumper is None:
#         return str(o)
#     else:
#         return dumper(o)

# def dump_tok(tok):
#     if tok.type == END:
#         return '}'
#     elif tok.type == LIST:
#         return 'list{'
#     elif tok.type == DICT:
#         return 'dict{'
#     elif tok.type == TUPLE:
#         return 'tuple{'
#     elif tok.type == COMPLEX:
#         return '%s{' % tok.val
#     elif tok.type == ATTRIBUTE:
#         return '%s:' % tok.val
#     elif tok.type == KEY:
#         return '%s:' % tok.val
#     elif tok.type == REFERENCE:
#         return '*%s' % tok.val
#     elif tok.type == LABEL:
#         return '&%s' % tok.val
#     else:
#         return _simple_dumper(tok.val)
#
# def itokens2str(tokens):
#     iter_tokens = iter(tokens)
#     prev_tok = next(iter_tokens)
#     while 1:
#         tok = next(iter_tokens)
#         yield dump_tok(prev_tok)
#         if tok is not end_token or prev_tok.type in (2,3,4,5,9,10):
#             yield ' '
#         prev_tok = tok
#     yield prev_tok
#
#
# def tokens2str(tokens):
#     return ''.join(itokens2str(tokens))
