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


##################################################

import cython

from cpython.object cimport PyObject, PyObject_Unicode
#from cpython.dict cimport PyDict_GetItem, PyDict_SetItem
#from cpython.float cimport PyFloat_FromString
from cpython.unicode cimport PyUnicode_AsASCIIString
from cpython.unicode cimport PyUnicode_FromEncodedObject
from cpython.bytes cimport PyBytes_AsString
from cpython.long cimport PyLong_FromString
#from cpython.dict cimport PyDict_SetItem, PyDict_GetItem
from cpython.tuple import PyTuple_New, PyTuple_SETITEM
from cpython.ref import Py_INCREF

from cpython.datetime cimport import_datetime, tzinfo
from cpython.datetime cimport time_new, timedelta_new, date_new, datetime_new

cdef object _decimal2str

cdef extern from "math.h" nogil:
    bint isnan(double x)
    bint isinf(double x)
    bint signbit(double x)
    bint isfinite(double x)

cdef extern from "floatobject.h":
    double PyFloat_AS_DOUBLE(object)

cdef extern from "utils.h":
    inline Py_UCS4 c_unicode_char(object text, int pos)
    inline unicode c_unicode_substr(object text, int start, int end)
    inline int c_unicode_length(object text)
    inline unicode c_object_to_unicode(object o)

    inline unicode c_int_tostring(object o)

    inline object c_float_fromstring(object text)
    inline object c_int_fromstring(char *text)
    inline object c_int_fromlong(long val)
    inline object c_int_fromint(int val)


cdef extern from "bytesobject.h":
    inline bytes PyBytes_FromStringAndSize(char* p, int n)
    #inline char* PyBytes_AS_STRING(object b)
    #inline int PyBytes_GET_SIZE(object b)


# ----------------------------------------
# Datatypes
# ----------------------------------------


ctypedef PyObject* PyObjectPtr

cdef public unicode empty_name
cdef public unicode c_undescore
cdef public object c_undefined

from axon._common cimport c_as_unicode, c_as_list, c_as_dict, c_as_tuple, dict_get

cdef public dict name_cache

cdef inline unicode c_as_name(object name):
    n = name_cache.get(name, None)
    if n is None:
        uname = c_as_unicode(name)
        name_cache[name] = uname
    elif name is None:
        uname = empty_name
    else:
        uname = n
    return uname


# cdef int ATOMIC = 1
# cdef int DICT = 2
# cdef int LIST = 3
# cdef int TUPLE = 4
# cdef int COMPLEX = 5
# cdef int END = 6
# cdef int REFERENCE = 7
# cdef int LABEL = 8
# cdef int ATTRIBUTE = 9
# cdef int KEY = 10
# 
# @cython.freelist(64)
# cdef class Token:
#     cdef public int type
#     cdef public object val
#     #cdef int idn
# 
# cdef inline Token c_new_token(int type, object val):
#     cdef Token tok = Token.__new__(Token)
#     tok.type = type
#     tok.val = val
#     return tok
# 
# cdef inline Token c_new_token0(int type):
#     cdef Token tok = Token.__new__(Token)
#     tok.type = type
#     return tok
# 
# #cdef inline Token c_new_token1(int type, object val, int idn):
# #    cdef Token tok = Token.__new__(Token)
# #    tok.type = type
# #    tok.val = val
# #    tok.idn = idn
# #    return tok
# 
# cdef Token end_token = c_new_token0(END)
# cdef Token dict_token = c_new_token0(DICT)
# cdef Token list_token = c_new_token0(LIST)
# cdef Token tuple_token = c_new_token0(TUPLE)

@cython.final
cdef public class Undefined[object UndefinedObject, type UndefinedType]:
    pass

#
# Readonly dict
#
@cython.final
cdef public class rdict(dict)[object ReadonlyDict, type ReadonlyDictType]:
    pass

#
# Readonly list
#
@cython.final
cdef public class rlist(list)[object ReadonlyList, type ReadonlyListType]:
    pass

cdef public rdict c_empty_dict
cdef public rlist c_empty_list

cdef class NamedValue:
    cdef public object __name__
    cdef public object __value__

cpdef named(name, value)

#
# Attribute
#
@cython.final
cdef public class Attribute[type AttributeType, object Attribute]:
    cdef public unicode name
    cdef public object value

@cython.locals(a=Attribute)
cpdef new_attribute(name, value)

cdef public Attribute c_new_attribute(unicode name, object value)

cdef class Attrs(object):
    #
    cdef public dict mapping

@cython.locals(attrs=Attrs)
cdef object new_attrs(dict o)

#
# Empty
#
@cython.freelist(64)
@cython.final
cdef public class Empty[type EmptyType, object EmptyObject]:
    cdef public object name

#
# Sequence
#
@cython.freelist(64)
@cython.final
cdef public class Sequence[object SequenceObject, type SequenceType]:
    cdef public object name
    cdef public list sequence
    #

#
# Object
#
@cython.freelist(64)
@cython.final
cdef public class Mapping[object MappingObject, type MappingType]:
    cdef public object name
    cdef public dict mapping
    #
#
#
# Element
#
@cython.freelist(64)
@cython.final
cdef public class Element[object ElementObject, type ElementType]:
    cdef public object name
    cdef public dict mapping
    cdef public list sequence
    #
#
# Construct
#
@cython.freelist(64)
@cython.final
cdef public class Instance[object InstanceObject, type InstanceType]:
    cdef public object name
    cdef public tuple sequence
    cdef public dict mapping

#
#
# Node
#
# @cython.freelist(64)
# @cython.final
# cdef public class Node[object NodeObject, type NodeType]:
#     cdef public object name
#     cdef public dict mapping
#     cdef public list sequence

@cython.locals(s=Sequence)
cdef public object c_new_sequence(object name, list sequence)
#
#@cython.locals(s=Collection)
#cdef public object c_new_collection(object name, list sequence)
#
@cython.locals(o=Mapping)
cdef public object c_new_mapping(object name, dict mapping)
#
@cython.locals(e=Element)
cdef public object c_new_element(object name, dict mapping, list sequence)
#
@cython.locals(e=Instance)
cdef public object c_new_instance(object name, tuple args, dict mapping)
#
@cython.locals(e=Empty)
cdef public object c_new_empty(object name)
#
# @cython.locals(e=Node)
# cdef public object c_new_node(object name, dict mapping, list sequence)


cdef public dict c_mapping_factory_dict
cdef public dict c_element_factory_dict
cdef public dict c_sequence_factory_dict
cdef public dict c_instance_factory_dict
cdef public dict c_empty_factory_dict
cdef public dict c_type_factory_dict

cdef public dict c_node_factory_dict
cdef public dict c_row_factory_dict

cdef class Builder:
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef class SafeBuilder(Builder):
    @cython.locals(o=Mapping)
    cdef public object create_mapping(self, object, dict)
    @cython.locals(e=Element)
    cdef public object create_element(self, object, dict, list)
    @cython.locals(s=Sequence)
    cdef public object create_sequence(self, object, list)
    @cython.locals(s=Instance)
    cdef public object create_instance(self, object, tuple, dict)
    @cython.locals(e=Empty)
    cdef public object create_empty(self, object)

cdef class StrictBuilder(Builder):
    cdef public dict c_mapping_factory_dict
    cdef public dict c_element_factory_dict
    cdef public dict c_sequence_factory_dict
    cdef public dict c_instance_factory_dict
    cdef public dict c_empty_factory_dict
    cdef public dict c_type_factory_dict

    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef class MixedBuilder(Builder):
    cdef public dict c_mapping_factory_dict
    cdef public dict c_element_factory_dict
    cdef public dict c_sequence_factory_dict
    cdef public dict c_instance_factory_dict
    cdef public dict c_empty_factory_dict
    cdef public dict c_type_factory_dict
    
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef public class GenericBuilder(Builder)[object GenericBuilderObject, type GenericBuilderType]:
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef object _str2decimal

cdef object _inf
cdef object _ninf
cdef object _nan
cdef object _decimal_inf
cdef object _decimal_ninf
cdef object _decimal_nan

cdef dict tz_dict = {}

cdef public class SimpleBuilder[type SimpleBuilderType, object SimpleBuilder]:

    @cython.locals(n=int, i=int, buf=cython.p_char, num_buffer=bytes)
    cdef inline object create_int(self, object text)
    @cython.locals(n=int, i=int, buf=cython.p_char, num_buffer=bytes)
    cdef inline object create_float(self, object text)
    cdef inline object create_decimal(self, object text)
    cdef inline object create_time(self, int h, int m, int s, int ms, object tz)
    cdef inline object create_timedelta(self, int d, int s, int ms)
    cdef inline object create_date(self, int y, int m, int d)
    cdef inline object create_datetime(self, int y, int M, int d, 
                                       int h, int m, int s, int ms, object tz)
    cdef inline object create_tzinfo(self, int minutes)
    cdef inline object create_inf(self)
    cdef inline object create_ninf(self)
    cdef inline object create_nan(self)
    cdef inline object create_decimal_inf(self)
    cdef inline object create_decimal_ninf(self)
    cdef inline object create_decimal_nan(self)
    cdef inline object create_binary(self, unicode text)

####################################################################

#cdef unicode NAME_EMPTY

@cython.final
cdef class StringReader:
    cdef unicode buffer
    cdef int pos
    cdef int n

    @cython.locals(ch=Py_UCS4, line=unicode, buffer=object,
                   pos=int, pos0=int, n=int)
    cpdef unicode readline(StringReader self)

    cpdef close(StringReader self)

@cython.final
cdef class StringWriter:

    cdef list blocks
    cdef list items
    cdef int n

    cpdef write(StringWriter self, item)

    cpdef object getvalue(StringWriter self)

    cpdef close(StringWriter self)

cdef object timezone_cls

cdef public class timezone(tzinfo)[object TimeZoneUTCObject, type TimeZoneUTCType]:
    """Fixed offset in minutes east from UTC."""

    cdef public object offset
    cdef public object name
    
    
# cdef class Context:
# 
#     cdef public Context parent
#     cdef dict _dict
#     
#     cdef int set(self, object key, object value) except -1
# 
#     cdef int update(self, dict kw) except -1
# 
#     cdef object get(self, object key)
# 
# @cython.locals(o=Context)
# cdef inline Context new_context(Context parent)

cdef dict c_constants

#
# Python tuple utility functions
#

cdef inline tuple new_tuple(Py_ssize_t size):
    return <tuple>PyTuple_New(size)
	
cdef inline int tuple_set(tuple t, Py_ssize_t i, object o):
    cdef int r
    r = PyTuple_SETITEM(t, i, o)
    if r == 0:
        Py_INCREF(o)
    return r
