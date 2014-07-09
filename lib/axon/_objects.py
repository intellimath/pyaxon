# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3

# The MIT License (MIT)
# 
# Copyright (c) <2011-2013> <Shibzukhov Zaur, szport at gmail dot com>
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

from axon.errors import error
import axon.errors as errors

from axon.types import builtins

from axon.types import str_type
c_str_type = str_type

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
    import cdecimal as _decimal
except:
    import decimal as _decimal

default_decimal_context = _decimal.getcontext()
_str2decimal = default_decimal_context.create_decimal
_decimal2str = default_decimal_context.to_eng_string

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
        return '?'
    def __str__(self):
        return '??'

def isundef(o):
    return type(o) is Undefined

c_undefined = Undefined()
undef = c_undefined

def _error_readonly(self):
    return AttributeError(
        'Readonly object type %r don\'t support assigning items or attributes' \
        % type(self))

def _error_empty_mapping(self):
    return KeyError(
        'Object %r contains an empty mapping' \
        % type(self))

def _error_empty_sequence(self):
    return KeyError(
        'Object %r contains an empty sequence' \
        % type(self))

def _error_invalid_name(name):
    return KeyError('Invalid name: %r' % type(name))

#####################################################
# name cache
#####################################################

c_undescore = '_'
empty_name = ''

name_cache = {None: empty_name, c_undescore: c_undescore}

def clear_all_names():
    name_cache = {}

def as_unicode(o):
    return c_as_unicode(o)

def as_list(o):
    return c_as_list(o)

def as_dict(o):
    return c_as_dict(o)

def as_tuple(o):
    return c_as_tuple(o)

#
# Readonly dict
#
class rdict(dict):
    #
    def __setitem__(self, key, item):
        raise _error_readonly(self)
    #
    def setdefault(self, key, default):
        raise _error_readonly(self)
    #
    def __delitem__(self, key):
        raise _error_readonly(self)
    #
    def __richcmp__(self, other, op):
        if type(self) is rdict:
            if op == 2:
                return dict.__eq__(self, other)
            elif op == 3:
                return not dict.__eq__(self, other)
            raise TypeError('This type of comparison is not supported')
        else:
            raise TypeError('The type of %r is not rdict' % type(self))
    #
#
# Readonly list
#
class rlist(list):
    #
    def __setitem__(self, index, item):
        raise _error_readonly(self)
    #
    def append(self, item):
        raise _error_readonly(self)
    #
    def extend(self, items):
        self._error_readonly(self)
    #
    def __delitem__(self, index):
        raise _error_readonly(self)
    #
    def __richcmp__(self, other, op):
        if type(self) is rlist:
            if op == 2:
                return list.__eq__(self, other)
            elif op == 3:
                return not list.__eq__(self, other)
            raise TypeError('This type of comparison is not supported')
        else:
            raise TypeError('The type of %r is not rlist' % type(self))

c_empty_dict = rdict({})
c_empty_list = rlist([])

#
# Name
#
# @cython.final
# cdef public class Name[type SimpleonNameType, object SimpleonName]:
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
#
#

class NamedValue:
    #
    def __init__(self, name, value):
        self.__name__ = value
        self.__value__ = value
    #
    def __getitem__(self, index):
        return self.__value__[index]
    #
    def __setitem__(self, index, value):
        self.__value__[index] = value
    #
    def __getattr__(self, name):
        return getattr(self.__value__, name)
    #
    def __isinstancecheck__(cls, inst):
        return isinstance(inst.__value__, cls)
    #

def named(name, value):
    return NamedValue(name, value)

#
# Attribute
#
class Attribute:
    #
    def __init__(self, name, value):
        self.name = c_as_name(name)
        self.value = value
    #
    def __getitem__(self, index):
        if index == 0:
            return self.name
        elif index == 1:
            return self.value
        else:
            raise IndexError('Index out of range')
    #
    def __repr__(self):
        return self.name + ':' + repr(self.value)
    #


def new_attribute(name, value):
    a = Attribute.__new__(Attribute)
    a.name = c_as_unicode(name)
    a.value = value
    return a

def c_new_attribute(name, value):
    a = Attribute.__new__(Attribute)
    a.name = name
    a.value = value
    return a

#
#
#

class Attrs(object):
    #
    def __getattr__(self, name):
        return self.mapping[name]
    #
    def __getitem__(self, name):
        return self.mapping[name]
    #
    #def __setattr__(self, name, value):
    #    self.mapping[name] = value
    #
    def __repr__(self):
        return repr(self.mapping)

def new_attrs(mapping):
    attrs = Attrs.__new__(Attrs)
    attrs.mapping = mapping
    return attrs

#
# Empty
#
class Empty(object):
    '''
    Empty named complex value.

    .. py:attribute:: _name

    Name of complex value

    .. py:attribute:: _mapping

    Dictionary of attributes.

    .. py:attribute:: _sequence

    List of values.

    '''
    @property
    def mapping(self):
        return None
    #
    @property
    def sequence(self):
        return None
    #
    @property
    def a(self):
        return new_attrs(c_empty_dict)
    #
    def __init__(self, name, sequences=None):
        self.name = c_as_name(name)
    #
#     def __richcmp__(self, other, op):
#         v = self.name == other.name and  \
#             len(other.mapping) == 0 and \
#             len(other.sequence) == 0
#         if op == 2:
#             return v
#         elif op == 3:
#             return not v
#         else:
#             raise TypeError('This type of comparison is not supported')
#     #
    def __repr__(self):
        return 'empty(' + repr(self.name) + ')'
    #
    def as_mapping(self, mapping=None):
        return c_new_mapping(self.name, c_as_dict(mapping))
    #
    def as_sequence(self, sequence=None):
        return c_new_sequence(self.name, c_as_list(sequence))
    #
    def as_element(self, mapping=None, sequence=None):
        return c_new_element(self.name, c_as_dict(mapping), c_as_list(sequence))
            #
    def as_instance(self, sequence=None, mapping=None):
        return c_new_instance(self.name, c_as_tuple(sequence), c_as_dict(mapping))



#
# Sequence
#
class Sequence(object):
    '''
    Named sequence of values.

    .. py:attribute:: _name

    Name of sequence.

    .. py:attribute:: _mapping

    Empty dictionary of attributes.

    .. py:attribute:: _sequence

    List of values.

    '''
    #
    @property
    def mapping(self):
        return None
    #
    @property
    def a(self):
        return new_attrs(c_empty_dict)
    #
    def __init__(self, name, sequence=None):
        self.name = c_as_name(name)
        self.sequence = c_as_list(sequence)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, val):
        self.sequence[index] = val
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Sequence:
#             v = (self.name == other.name) and (self.sequence == other.sequence)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def __repr__(self):
        return 'sequence(' + \
                ', '.join([repr(x) for x in (self.name, self.sequence) if x]) + ')'
    #
    def as_mapping(self):
        raise error("Sequence->Mapping convertion isn't available")
    #
    def as_sequence(self):
        return self
    #
    def as_element(self, mapping=None):
        return c_new_element(self.name, c_as_dict(mapping), self.sequence)
    #
    def as_instance(self, mapping=None):
        return c_new_instance(self.name, tuple(self.sequence), c_as_dict(mapping))

#
# Mapping
#
class Mapping(object):
    '''
    Named mapping containing pairs of `name`/`value`.

    .. py:attribute:: _name

    Name of mapping

    .. py:attribute:: _mapping

    Mapping containing pairs of name: value.

    .. py:attribute:: _sequence

    Empty list of values.

    '''
    #
    @property
    def sequence(self):
        return None
    #
    @property
    def a(self):
        return new_attrs(self.mapping)
    #
    def __init__(self, name, mapping=None):
        self.name = c_as_name(name)
        self.mapping = c_as_dict(mapping)
    #
    def get(self, name, default=None):
        return self.mapping.get(name, default)
    #
    def set(self, name, val):
        self.mapping[name] = val
    #
    def update(self, map):
        self.mapping.update(map)
    #
    def __contains__(self, name):
        return name in self.mapping
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Mapping:
#             v = (self.name == other.name) and (self.mapping == other.mapping)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
#     #
    def __repr__(self):
        return  'mapping(' + \
                ', '.join([repr(x) for x in (self.name, self.mapping) if x]) + ')'
    #
    def as_mapping(self):
        return self
    #
    def as_sequence(self):
        raise error("Mapping->Sequence convertion isn't available")
    #
    def as_element(self, sequence=None):
        return c_new_element(self.name, self.mapping, c_as_list(sequence))
    #
    def as_instance(self, sequence=None):
        return c_new_instance(self.name, c_as_tuple(sequence), self.mapping)

#
#
# Element
#
class Element(object):
    '''
    Named mapping containing list of values.

    .. py:attribute:: _name

    Name of element

    .. py:attribute:: _mapping

    Mapping containing pairs of `name`/`value`.

    .. py:attribute:: _sequence

    Child list of values.

    '''
    #
    @property
    def a(self):
        return new_attrs(self.mapping)
    #
    def __init__(self, name, mapping, sequence=None):
        self.name = c_as_name(name)
        self.mapping = c_as_dict(mapping)
        self.sequence = c_as_list(sequence)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, val):
        self.sequence[index] = val
    #
    def __contains__(self, name):
        return name in self.mapping
    #
    def get(self, name, default=None):
        return self.mapping.get(name, default)
    #
    def set(self, name, val):
        self.mapping[name] = val
    #
    def update(self, map):
        self.mapping.update(map)
    #
    def append(self, sub):
        self.sequence.append(sub)
    #
    def extend(self, subs):
        self.sequence.extend(subs)
    #
    def __repr__(self):
        return  'element(' + \
                ', '.join([repr(x) for x in (self.name, self.mapping, self.sequence) if x]) + ')'
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Element:
#             v = (self.name == other.name) and \
#                 (self.sequence == other.sequence) and \
#                 (self.mapping == other.mapping)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def as_mapping(self):
        raise error("Element->Mapping convertion isn't available")
    #
    def as_sequence(self):
        raise error("Element->Sequence convertion isn't available")
    #
    def as_element(self):
        return self
    #
    def as_instance(self):
        return c_new_instance(self.name, tuple(self.sequence), self.mapping)

#
# Instance
#
class Instance(object):
    '''
    Named sequence containing pairs of name: value.

    .. py:attribute:: _name

    Name of object.

    .. py:attribute:: _mapping

    Mapping containing optional values in form of `name`: `value` pairs.

    .. py:attribute:: _sequence

    List of requiered values.

    '''
    #
    @property
    def a(self):
        return new_attrs(self.mapping)
    #
    def __init__(self, name, sequence=None, mapping=None):
        self.name = c_as_name(name)
        self.sequence = c_as_tuple(sequence)
        self.mapping = c_as_dict(mapping)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, val):
        self.sequence[index] = val
    #
    def get(self, name, default=None):
        return self.mapping.get(name, default)
    #
    def set(self, name, val):
        self.mapping[name] = val
    #
    def update(self, map):
        self.mapping.update(map)
    #
    def append(self, sub):
        self.sequence.append(sub)
    #
    def extend(self, subs):
        self.sequence.extend(subs)
    #
    def __repr__(self):
        return  'instance(' + \
                ', '.join([repr(x) for x in (self.name, self.sequence, self.mapping) if x]) + ')'
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Instance:
#             s0 = self
#             s = other
#             v = (self.name == other.name) and \
#                 (self.sequence == other.sequence) and \
#                 (self.mapping == other.mapping)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def as_mapping(self):
        raise error("Instance->Mapping convertion isn't available")
    #
    def as_sequence(self):
        raise error("Instance->Sequence convertion isn't available")
    #
    def as_element(self):
        return c_new_element(self.name, self.mapping, list(self.sequence))
    #
    def as_instance(self):
        return self

####################################################################

def c_new_sequence(name, sequence):
    s = Sequence.__new__(Sequence)
    s.name = name
    s.sequence = sequence
    return s

def c_new_mapping(name, mapping):
    o = Mapping.__new__(Mapping)
    o.name = name
    o.mapping = mapping
    return o
#
def c_new_element(name, mapping, sequence):
    e = Element.__new__(Element)
    e.name = name
    e.mapping = mapping
    e.sequence = sequence
    return e
#
def c_new_instance(name, args, mapping):
    e = Instance.__new__(Instance)
    e.name = name
    e.sequence = args
    e.mapping = mapping
    return e

def c_new_empty(name):
    e = Empty.__new__(Empty)
    e.name = name
    return e

#####################################################################################

#NAME_IS_EMPTY = 'Name is empty'

def sequence(name, sequence=None):
    '''
    Factory function for creating named sequence.

    :param name:

        name of sequence.

    :param sequence:

        python sequence containing values.
    '''
    return c_new_sequence(c_as_name(name), c_as_list(sequence))
#
def mapping(name, mapping=None):
    '''
    Factory function for creating named mapping.

    :param name:

        name of sequence.

    :param mapping:

        python dictionary containing pairs of `name`/`value`.
    '''
    return c_new_mapping(c_as_name(name), c_as_dict(mapping))
#
def element(name, mapping, sequence=None):
    '''
    Factory function for creating named element.

    :param name:

        name of element.

    :param mapping:

        python dictionary containing pairs of `name: value`.

    :param sequence:

        python sequence containing child values.
    '''
    return c_new_element(c_as_name(name), c_as_dict(mapping), c_as_list(sequence))
#
def instance(name, sequence, mapping):
    '''
    Factory function for creating named instance.

    :param name:

        name of object.

    :param sequence:

        python sequence containing required values.

    :param mapping:

        python dictionary containing optional values in form of of `name`: `value` pairs.

    '''
    return c_new_instance(c_as_name(name), c_as_tuple(sequence), c_as_dict(mapping))
#
def empty(name):
    '''
    Factory function for creating empty complex value.

    :param name:

        name of empty complex value.
    '''
    return c_new_empty(c_as_name(name))
#

c_factory_dict = {}

def reset_factory():
    c_factory_dict = {}

def factory(name, factory_func=None):
    name = c_as_unicode(name)
    if factory_func is None:
        def _factory(factory_func, name=name):
            c_factory_dict[name] = factory_func
            return factory_func
        return _factory
    else:
        c_factory_dict[name] = factory_func

class Builder:
    def create_sequence(self, name, sequence):
        return None
    #
    def create_mapping(self, name, mapping):
        return None
    #
    def create_element(self, name, mapping, sequence):
        return None
    #
    def create_instance(self, name, args, mapping):
        return None

    def create_empty(self, name):
        return None

class SafeBuilder(Builder):
    #
    def create_mapping(self, name, mapping):
        o = Mapping.__new__(Mapping)
        o.name = name
        o.mapping = mapping
        return o
    #
    def create_sequence(self, name, sequence):
        s = Sequence.__new__(Sequence)
        s.name = name
        s.sequence = sequence
        return s
    #
    def create_element(self, name, mapping, sequence):
        e = Element.__new__(Element)
        e.name = name
        e.mapping = mapping
        e.sequence = sequence
        return e
    #
    def create_instance(self, name, args, mapping):
        e = Instance.__new__(Instance)
        e.name = name
        e.sequence = args
        e.mapping = mapping
        return e

    def create_empty(self, name):
        e = Empty.__new__(Empty)
        e.name = name
        return e

class StrictBuilder(Builder):

    def __init__(self):
        self.c_factory_dict = c_factory_dict

    def create_mapping(self, name, mapping):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            errors.error_no_handler(name)
        else:
            return handler(mapping)
    #
    def create_sequence(self, name, sequence):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            errors.error_no_handler(name)
        else:
            return handler(sequence)
    #
    def create_element(self, name, mapping, sequence):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            errors.error_no_handler(name)
        else:
            return handler(mapping, sequence)
    #
    def create_instance(self, name, sequence, mapping):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            errors.error_no_handler(name)
        else:
            return handler(sequence, mapping)
    #
    def create_empty(self, name):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            errors.error_no_handler(name)
        else:
            return handler()

class MixedBuilder(Builder):

    def __init__(self):
        self.c_factory_dict = c_factory_dict

    def create_mapping(self, name, mapping):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            return c_new_mapping(name, mapping)
        else:
            return handler(mapping)
    #
    def create_sequence(self, name, sequence):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            return c_new_sequence(name, sequence)
        else:
            return handler(sequence)
    #
    def create_element(self, name, mapping, sequence):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            return c_new_element(name, mapping, sequence)
        else:
            return handler(mapping, sequence)
    #
    def create_instance(self, name, sequence, mapping):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            return c_new_instance(name, sequence, mapping)
        else:
            return handler(sequence, mapping)
    #
    def create_empty(self, name):
        handler = self.c_factory_dict.get(name)
        if handler is None:
            return c_new_empty(name)
        else:
            return handler()

class GenericBuilder(Builder):

    def create_mapping(self, name, mapping):
        return self.mapping(name, c_as_dict(mapping))
    #
    def create_sequence(self, name, sequence):
        return self.sequence(name, c_as_list(sequence))
    #
    def create_element(self, name, mapping, sequence):
        return self.element(name, c_as_dict(mapping), c_as_list(sequence))
    #
    def create_instance(self, name, sequence, mapping):
        return self.instance(name, c_as_list(sequence), c_as_dict(mapping))
    #
    def create_empty(self, name):
        return self.empty(name)

c_builder_dict = {
    'safe': SafeBuilder(),
    'strict': StrictBuilder(),
    'mixed': MixedBuilder()
}

def register_builder(mode, builder):
    c_builder_dict[mode] = builder

def get_builder(mode):
    return c_get_builder(mode)

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
