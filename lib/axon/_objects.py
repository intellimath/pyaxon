# coding: utf-8

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

#
# ----------------------------------------
# Datatypes
# ----------------------------------------

import cython

#from axon.errors import error
import axon.errors as errors

from axon.types import builtins

import datetime
import_datetime()

try:
    from datetime import timezone as timezone_cls
except:
    timezone_cls = timezone

try:
    from base64 import encodebytes, decodebytes
except:
    from base64 import encodestring as encodebytes, decodestring as decodebytes

try:
    import _decimal
except:
    import decimal as _decimal    

default_decimal_context = _decimal.getcontext()
_str2decimal = default_decimal_context.create_decimal
_decimal2str = default_decimal_context.to_eng_string

from _weakref import proxy as _proxy

# ATOMIC = 1
# DICT = 2
# LIST = 3
# TUPLE = 4
# COMPLEX = 5
# END = 6
# REFERENCE = 7
# LABEL = 8
# ATTRIBUTE = 9
# KEY = 10
# 
# class Token:
#     def __str__(self):
#         return '%s: %r' % (self.type, self.val)
#         
# 
# end_token = c_new_token0(END)
# dict_token = c_new_token0(DICT)
# list_token = c_new_token0(LIST)
# tuple_token = c_new_token0(TUPLE)

class Undefined:
    def __repr__(self):
        return '??'
    def __str__(self):
        return '??'

# def isundef(o):
#     return type(o) is Undefined

c_undefined = Undefined()
undef = c_undefined

# def _error_readonly(self):
#     return AttributeError(
#         'Readonly object type %r don\'t support assigning items or attributes' \
#         % type(self))
#
# def _error_empty_mapping(self):
#     return KeyError(
#         'Object %r contains an empty mapping' \
#         % type(self))
#
# def _error_empty_sequence(self):
#     return KeyError(
#         'Object %r contains an empty sequence' \
#         % type(self))
#
# def _error_invalid_name(name):
#     return KeyError('Invalid name: %r' % type(name))
#
def _error_unsupported_comparison(self):
    return TypeError('This type of comparison is not supported by %r' % type(self))

def _error_incomparable_types(self, other):
    return TypeError('Types %r and %r are not comparable' % (type(self), type(other)))
                 
#####################################################
# name cache
#####################################################

c_undescore = '_'
empty_name = ''

name_cache = {empty_name: empty_name, c_undescore: c_undescore}

def clear_all_names():
    name_cache = {}

def as_name(name):
    return c_as_name(c_as_unicode(name))

def as_unicode(o):
    return c_as_unicode(o)

def as_list(o):
    return c_as_list(o)

def as_dict(o):
    return c_as_dict(o)

def as_tuple(o):
    return c_as_tuple(o)
    
c_constants = {
    # c_as_name(c_as_unicode('true')): True,
    # c_as_name(c_as_unicode('false')): False,
    # c_as_name(c_as_unicode('null')): None,
    c_as_name(c_as_unicode('NaN')): float('nan'),
    c_as_name(c_as_unicode('NaND')): _decimal.Decimal(float('nan')),
    c_as_name(c_as_unicode('Inf')): float('inf'),
    c_as_name(c_as_unicode('NegInf')): float('-inf'),
}
 
reserved_name_dict = {'null':None, 'true':True, 'false':False}
empty_odict = OrderedDict([])
empty_list = []

#
# Readonly dict
#
# class rdict(dict):
#     #
#     def __setitem__(self, key, item):
#         raise _error_readonly(self)
#     #
#     def setdefault(self, key, default):
#         raise _error_readonly(self)
#     #
#     def __delitem__(self, key):
#         raise _error_readonly(self)
#     #
#     def __richcmp__(self, other, op):
#         if type(self) is rdict:
#             if op == 2:
#                 return dict.__eq__(self, other)
#             elif op == 3:
#                 return not dict.__eq__(self, other)
#             raise TypeError('This type of comparison is not supported')
#         else:
#             raise TypeError('The type of %r is not rdict' % type(self))
    #
#
# Readonly list
#
# class rlist(list):
#     #
#     def __setitem__(self, index, item):
#         raise _error_readonly(self)
#     #
#     def append(self, item):
#         raise _error_readonly(self)
#     #
#     def extend(self, items):
#         self._error_readonly(self)
#     #
#     def __delitem__(self, index):
#         raise _error_readonly(self)
#     #
#     def __richcmp__(self, other, op):
#         if type(self) is rlist:
#             if op == 2:
#                 return list.__eq__(self, other)
#             elif op == 3:
#                 return not list.__eq__(self, other)
#             raise TypeError('This type of comparison is not supported')
#         else:
#             raise TypeError('The type of %r is not rlist' % type(self))
#
# c_empty_dict = rdict({})
# c_empty_list = rlist([])

#
# Name
#
# @cython.final
# cdef public class Name[type AxonNameType, object AxonName]:
#     cdef unicode c_name
#     #
#     property name:
#         def __get__(self):
#             return self.c_name
#     #
#     def __init__(self, unicode name):
#         self.c_name = name
#     #
#     def __hash__(self):
#         return self.c_name.__hash__()
#     #
#     def __repr__(self):
#         return self.c_name
#
# cdef public object c_new_name(unicode name):
#     cdef Name n = <Name>(Name.__new__(Name))
#     n.c_name = name
#     return n
#
# def name(unicode uname):
#     cdef Name n = <Name>(Name.__new__(Name))
#     if type(uname) is unicode:
#         n.c_name = <unicode>uname
#     else:
#         n.c_name = unicode(uname)
#     return n

#
# Attribute
#
class Attribute(object):
    #
    def __init__(self, name, val):
        self.name = c_as_name(name)
        self.val = val
    #
    def __getitem__(self, index):
        if index == 0:
            return self.name
        elif index == 1:
            return self.val
        else:
            raise IndexError('Index out of range: ' + str(index))
    #
    def __iter__(self):
        yield self.name
        yield self.val
    #
    def __repr__(self):
        return self.name + ':' + repr(self.val)

def attribute(name, val):
    a = Attribute.__new__(Attribute)
    a.name = c_as_unicode(name)
    a.val = val
    return a

def c_new_attribute(name, val):
    a = Attribute.__new__(Attribute)
    a.name = name
    a.val = val
    return a

#
# KeyVal
#
class KeyVal(object):
    #
    def __init__(self, key, val):
        self.key = c_as_unicode(key)
        self.val = val
    #
    def __getitem__(self, index):
        if index == 0:
            return self.key
        elif index == 1:
            return self.val
        else:
            raise IndexError('Index out of range: ' + str(index))
    #
    def __iter__(self):
        yield self.key
        yield self.val
    #
    def __repr__(self):
        return repr(self.key) + ':' + repr(self.val)

def keyval(key, val):
    a = KeyVal.__new__(KeyVal)
    a.key = c_as_unicode(key)
    a.val = val
    return a

def c_new_keyval(key, val):
    a = KeyVal.__new__(KeyVal)
    a.key = key
    a.val = val
    return a

# class ObjectWithMetadata(object):
#     #
#     def __init__(self, ob, metadata):
#         self.metadata = metadata
#         self.ob = ob
#     #
#     def __getitem__(self, i):
#         return self.ob[i]
#     #
#     def __setitem__(self, i, v):
#         self.ob[i] = v
#     #
#     def __delitem__(self, i):
#         del self.ob[i]
#     #
#     def __contains__(self, v):
#         return v in self.ob
#     #
#     def __bool__(self):
#         return self.ob and self.metadata
#     #
#     def __iter__(self):
#         return iter(self.ob)
#     #
#     def __str__(self):
#         return str(self.ob) + ' / ' + str(self.metadata)
#     #
#     def __repr__(self):
#         return str(self.ob) + ' / ' + str(self.metadata)
#     #
#     def __getattr__(self, name):
#         if name == '__metadata__':
#             return self.metadata
#         else:
#             return self.ob.__getattribute__(name)
#
# def c_add_metadata(ob, metadata):
#     o = ObjectWithMetadata.__new__(ObjectWithMetadata)
#     o.ob = ob
#     o.metadata = metadata
#     return o
#
# def add_metadata(ob, metadata):
#     return c_add_metadata(ob, metadata)
#

#
# Node
#
class Node(object):
    
    @property
    def __tag__(self):
        return self.name

    @property
    def __attrs__(self):
        return self.attrs

    @property
    def __vals__(self):
        return self.vals

    def __init__(self, name, attrs=None, vals=None):
        self.name = c_as_name(name)
        
        if attrs is None:
            self.attrs = None
        else:
            self.attrs = OrderedDict(attrs)
            
        if vals is None:
            self.vals = None
        else:
            tp = type(vals)
            if tp is list:
                self.vals = vals
            else:
                self.vals = list(vals)
    #
    def __getattr__(self, name):
        if name.startswith('__'):
            return self.__getattribute__(name)
        else:
            if self.attrs is not None:
                val = self.attrs.get(name, c_undefined)
            else:
                val = c_undefined
                
            if val is c_undefined:
                raise AttributeError("Undefined name: " + self.name)

            return val
    #
    def __setattr__(self, name, val):
        if name.startswith('__'):
            object.__setattr__(self, name, val)
        else:
            self.attrs[name] = val
    #
    def __getitem__(self, index):
        if self.vals is None:
            raise errors.errors_no_children(Node)
        return self.vals[index]
    #
    def __setitem__(self, index, val):
        if self.vals is None:
            raise errors.errors_no_children(Node)
        self.vals[index] = val
    #
    def __delitem__(self, index):
        if self.vals is None:
            raise errors.errors_no_children(Node)
        del self.vals[index]
    #
    def __iadd__(self, vals):
        if self.vals is None:
            self.vals = []
        self.vals.extend(vals)
        return self
    #
    def __iter__(self):
        if self.vals is None:
            return iter([])
        else:
            return iter(self.vals)
    #
    def __nonzero__(self):
        return self.attrs or self.vals
    #
    def __richcmp__(self, other, op):
        if type(self) is Node:
            v = (self.name == other.name) and (self.attrs == other.attrs) and (self.vals == other.vals)
            if op == 2:
                return v
            elif op == 3:
                return not v
            else:
                raise _error_unsupported_comparison(self)
        else:
            raise _error_incomparable_types(self, other)
    #
    def __repr__(self):
        attrs = self.attrs
        vals = self.vals
        name = self.name
        print(self.name, attrs, vals)
        if attrs:
            attrs_text = ', '.join([str(name)+': '+repr(attrs[name]) for name in attrs])
        else:
            attrs_text = ''
        if vals:
            vals_text = ', '.join([repr(x) for x in vals])
        else:
            vals_text = ''
        sp = (' ' if attrs and vals else '')
        return name + '{' + attrs_text + sp + vals_text + '}'
    #
    def __reduce__(self):
        return node, (self.name, self.attrs, self.vals)

def c_new_node(name, attrs, vals):
    node = Node.__new__(Node)
    node.name = name
    node.attrs = attrs
    node.vals = vals
    return node
        
def node(name, attrs=None, vals=None):
    '''
    Factory function for creating node.

    :param name:

        name of the sequence.

    :param sequence:

        python sequence containing values.
    '''
    if attrs is not None:
        if len(attrs) == 0:
            _attrs = None
        else:
            _attrs = OrderedDict(attrs)
    else:
        _attrs = None
    
    if vals is not None and len(vals) == 0:
        _vals = None
    else:
        _vals = c_as_list(vals)
    
    return c_new_node(c_as_name(name), _attrs, _vals)
            
def dict_as_sequence_factory(items):
    return dict(items)

class FactoryRegister:

    def __init__(self):
        self.reset()
        self.reset_types()

    def reset(self):
        self.c_factory_dict = {}
        self.c_factory_dict['dict'] = dict_as_sequence_factory

    def reset_types(self):
        self.c_type_factory_dict = {}

    def factory(self, name, factory_func=None):
        name = c_as_unicode(name)
        if factory_func is None:
            def _factory(factory_func, name=name):
                self.c_factory_dict[name] = factory_func
                return factory_func
            return _factory
        else:
            self.c_factory_dict[name] = factory_func
    #
    def defname(self, name, val):
        name = c_as_unicode(name)
        self.c_constants[name] = val

    def type(self, tp, factory_func=None):
        if factory_func is None:
            def _factory(factory_func, tp=tp):
                self.c_type_factory_dict[tp] = factory_func
                return factory_func
            return _factory
        else:
            self.c_type_factory_dict[tp] = factory_func

    def convert(self, ob, to):
        caller = self.c_type_factory_dict.get(to, None)
        otype = type(ob)
        if caller is None:
            raise errors.error2("Object %s can't be converted to %s" % (otype, to))

        if otype is Node:
            return caller(ob.sequence)
        elif otype is dict:
            return caller(ob)
        elif otype is list:
            return caller(ob)
        elif otype is tuple:
            return caller(ob)
        else:
            raise errors.error2("Object %s do not support convertion" % otype)

default_factory_register = FactoryRegister()

factory = default_factory_register.factory
defname = default_factory_register.defname
type_factory = default_factory_register.type
convert = default_factory_register.convert
reset_factory = default_factory_register.reset
reset_type_factory = default_factory_register.reset_types

def dict_as_node(d):
    return c_new_node(c_as_name('dict'), None, [(k,v) for k,v in d.items()])

class Builder:
    def create_node(self, name, attrs, vals):
        return self.node(name, attrs, vals)
    #

class SafeBuilder(Builder):
    #
    def create_node(self, name, attrs, vals):
        return c_new_node(name, attrs, vals)
    #
    
class StrictBuilder(Builder):

    @cython.locals(register=FactoryRegister)
    def __init__(self, register=default_factory_register):
        self.register = register
        self.c_factory_dict = register.c_factory_dict
    #
    def create_node(self, name, attrs, vals):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            errors.error_no_handler(name)
        else:
            return handler(attrs, vals)
    #

class MixedBuilder(Builder):

    @cython.locals(register=FactoryRegister)
    def __init__(self, register=default_factory_register):
        self.register = register
        self.c_factory_dict = register.c_factory_dict
    #
    def create_node(self, name, attrs, vals):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            return c_new_node(name, attrs, vals)
        else:
            return handler(attrs, vals)
    #

_inf = float('inf')
_ninf = float('-inf')
_nan = float('nan')
_decimal_inf = _str2decimal('Infinity')
_decimal_ninf = _str2decimal('-Infinity')
_decimal_nan = _str2decimal('NaN')

tz_dict = {}


class SimpleBuilder:

    def create_int(self, text):
        n = c_unicode_length(text)
        num_buffer = PyBytes_FromStringAndSize(cython.NULL, n+1)

        buf = num_buffer

        for i in range(n):
            buf[i] = c_unicode_char(text, i)
        buf[n] = 0

        return c_int_fromstring(buf)

    def create_float(self, text):
        n = c_unicode_length(text)
        num_buffer = PyBytes_FromStringAndSize(cython.NULL, n)

        buf = num_buffer

        for i in range(n):
            buf[i] = c_unicode_char(text, i)

        return c_float_fromstring(num_buffer)

    def create_decimal(self, text):
        return _str2decimal(text)

    def create_time(self, h, m, s, ms, tz):
        return time_new(h, m, s, ms, tz)

    def create_timedelta(self, d, s, ms):
        return timedelta_new(d, s, ms)

    def create_date(self, y, m, d):
        return date_new(y, m, d)

    def create_datetime(self, y, M, d, h, m, s, ms, tz):
        return datetime_new(y, M, d, h, m, s, ms, tz)

    def create_tzinfo(self, minutes):
        o_minutes = minutes
        tzinfo = tz_dict.get(o_minutes, None)
        if tzinfo is None:
            tzinfo = timezone_cls(datetime.timedelta(minutes=o_minutes))
            tz_dict[o_minutes] = tzinfo
        return tzinfo

    def create_inf(self):
        return _inf

    def create_ninf(self):
        return _ninf

    def create_nan(self):
        return _nan

    def create_decimal_inf(self):
        return _decimal_inf

    def create_decimal_ninf(self):
        return _decimal_ninf

    def create_decimal_nan(self):
        return _decimal_nan

    def create_binary(self, text):
        return decodebytes(text.encode('ascii'))

class StringReader:

    def __init__(self, text):
        self.buffer = text
        self.pos = 0
        self.n = len(text)

    def readline(self):

        buffer = self.buffer
        pos = self.pos
        pos0 = self.pos
        n = self.n

        if pos >= n:
            return ''

        while 1:
            if pos >= n:
                line = c_unicode_substr(buffer, pos0, pos)
                break

            ch = c_unicode_char(buffer, pos)
            if ch == '\n':
                pos += 1
                if pos >= n:
                    line = c_unicode_substr(buffer, pos0, pos)
                    break

                ch = c_unicode_char(buffer, pos)
                if ch == '\r':
                    pos += 1

                line = c_unicode_substr(buffer, pos0, pos)
                break
            elif ch == '\r':
                pos += 1
                if pos >= n:
                    line = c_unicode_substr(buffer, pos0, pos)
                    break

                ch = c_unicode_char(buffer, pos)
                if ch == '\n':
                    pos += 1

                line = c_unicode_substr(buffer, pos0, pos)
                break
            else:
                pos += 1
                #ch = buffer[pos]

        self.pos = pos
        return line

    def close(self):
        self.pos = self.n


class StringWriter:

    def __init__(self):
        self.blocks = []
        self.items = []
        self.n = 0

    def write(self, item):
        if self.n > 256:
            self.blocks.append(''.join(self.items))
            self.items = []
            self.n = 0
        self.items.append(item)
        self.n += 1

    def getvalue(self):
        if self.items:
            self.blocks.append(''.join(self.items))
            self.items = []
            self.n = 0
        return ''.join(self.blocks)

    def close(self):
        self.items = []
        self.blocks = []



class timezone(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name=None):
        self.offset = offset
        self.name = name

    def utcoffset(self, dt):
        return self.offset

    def tzname(self, dt):
        seconds = self.offset.seconds + self.offset.days * 24 * 60 * 60

        if seconds < 0:
            seconds = -seconds
            sign = '-'
        else:
            sign = '+'

        minutes, seconds = builtins.divmod(seconds, 60)
        hours, minutes = builtins.divmod(minutes, 60)

        if minutes:
            return 'UTC%s%02d:%02d' % (sign, hours, minutes)
        else:
            return 'UTC%s%02d' % (sign, hours)

    def dst(self, dt):
        return None

    def __richcmp__(self, other, op):
        if not isinstance(other, tzinfo):
            raise TypeError('Invalid type: expected `tzinfo` instance')

        if op == 0:
            return self.offset < other.offset
        elif op == 1:
            return self.offset <= other.offset
        elif op == 2:
            return self.offset == other.offset
        elif op == 3:
            return self.offset != other.offset
        elif op == 4:
            return self.offset > other.offset
        else:
            return self.offset >= other.offset

    def __str__(self):
        return self.tzname(None)

    def __repr__(self):
        if self.name:
            return "timezone(%r, %s)" % (self.offset, self.name)
        else:
            return "timezone(%r)" % (self.offset,)

# class Context(object):
#     
#     def set(self, key, value):
#         self._dict[key] = value
#         return 0
# 
#     def get(self, key):
#         val = self._dict.get(key, undef)
#         if val is undef:
#             if self.parent is None:
#                 return undef
#             else:
#                 return self.parent.get(key)
#         else:
#             return val
# 
#     def update(self, kw):
#         self._dict.update(kw)
#         return 0
#     
# def new_context(parent):
#     o = Context.__new__(Context)
#     o.parent = parent
#     o._dict = {}
       

