# coding: utf-8

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

cimport cython
from cpython.object cimport PyObject, Py_SIZE
#from cpython.list cimport PyList_Append, PyList_SET_ITEM
from cpython.dict cimport PyDict_SetItem, PyDict_GetItem

#from cpython.unicode cimport PyUnicode_AsASCIIString
#from cpython.bytes cimport PyBytes_AsString
from cpython.long cimport PyLong_FromString
#from cpython.bytes cimport PyBytes_FromStringAndSize, PyBytes_AS_STRING

cimport cpython.array as array

cdef extern from "unicodeobject.h":
    unicode PyUnicode_FromOrdinal(int ordinal)

cdef extern from "utils.h":
    inline object c_float_fromstring(object text)
    inline object c_int_fromstring(char *text)
    inline object c_int_fromlong(long val)
    inline object c_int_fromint(int val)

    inline Py_UCS4 c_unicode_char(unicode object, int pos)
    inline unicode c_unicode_substr(unicode object, int start, int end)
    inline int c_unicode_length(unicode object)

    #inline bint CH_BETWEEN(Py_UCS4, Py_UCS4, Py_UCS4)

    inline void Py_SET_SIZE(object o, int n)

    inline Py_UCS4 current_char(Loader self)
    inline void skip_char(Loader self)
    inline Py_UCS4 next_char(Loader self)

    inline unicode get_token(Loader self, int pos0)


from axon._objects cimport c_undefined, empty_name
from axon._objects cimport name_cache, c_as_unicode, c_as_name, py_as_name
from axon._objects cimport c_as_tuple
from axon._objects cimport c_new_instance, c_new_mapping, c_new_sequence, \
                           c_new_element, c_new_empty

from axon._objects cimport Builder, SafeBuilder, StrictBuilder, MixedBuilder
from axon._objects cimport get_builder
from axon._objects cimport SimpleBuilder

from axon._objects cimport c_new_token, end_token, dict_token, tuple_token, list_token
from axon._objects cimport ATOMIC, END, COMPLEX, ATTRIBUTE, KEY, REFERENCE, LABEL, LIST, DICT, TUPLE

cdef object unicode_type, str_type, int_type, long_type
cdef object bool_type, float_type, bytes_type

cdef dict c_constants

cdef inline object dict_get(object op, object key, object default):
    cdef PyObject* val = <PyObject*>PyDict_GetItem(op, key)
    if val == NULL:
        return default
    else:
        return <object>val

# cdef inline unicode _as_name(object name):
#     val = name_cache.get(name, None)
#     if val is None:
#         if name is None:
#             return empty_name
#         name_cache[name] = name
#         return <unicode>name
#     else:
#         return <unicode>val
#
# cdef inline object c_as_name(object name):
#     n = dict_get(name_cache, name, None)
#     if n is None:
#         uname = c_as_unicode(name)
#         name_cache[name] = uname
#     elif name is None:
#         uname = empty_name
#     else:
#         uname = n
#     return uname
#
# cdef inline tuple c_as_tuple(object ob):
#     if type(ob) is tuple:
#         return <tuple>ob
#     elif ob is None:
#         return ()
#     else:
#         return tuple(ob)


# cdef inline unicode c_as_unicode(object ob):
#     tp = type(ob)
#     if tp is unicode:
#         return <unicode>ob
#     elif tp == type(''):
#         return unicode(ob)
#     elif ob is None:
#         return unicode('')
#     else:
#         raise TypeError('This object %r is not unicode compatible' % ob)

@cython.final
cdef class Loader:

    cdef object fd
    cdef object readline
    cdef object encoding

    cdef public object line
    cdef bint eof
    cdef public int pos
    cdef public int lnum
    cdef public object errto

    cdef int bc
    cdef int bs
    cdef int bq

    cdef bint json

    cdef public Builder builder
    cdef public SimpleBuilder sbuilder

    cdef dict c_constants
    cdef dict labeled_objects

    cdef int[:] ta
    cdef int[:] da
    cdef int[:] to

    cdef bint is_nl
    cdef list idn_stack
    cdef public int idn

    cpdef _check_pairs(Loader self)

    @cython.locals(sequence=list)
    cpdef load(Loader self)

    #cdef inline void skip_char(Loader self)
    #cdef inline Py_UCS4 next_char(Loader self)
    #cdef inline Py_UCS4 current_char(Loader self)

    @cython.locals(ch=Py_UCS4)
    cdef inline Py_UCS4 moveto_next_token(Loader self) except -1

    @cython.locals(ch=Py_UCS4)
    cdef inline Py_UCS4 skip_spaces(Loader self)

    @cython.locals(ch=Py_UCS4)
    cdef inline void skip_whitespace(Loader self)

    @cython.locals(line=unicode, ch=Py_UCS4, n=int)
    cdef void next_line(Loader self)

#     @cython.locals(ch=Py_UCS4, n=int)
#     cdef bint get_dots(Loader self)

    #@cython.locals(ch=Py_UCS4)
    #cdef inline bint valid_end_item(Loader self)

    @cython.locals(ch=Py_UCS4, val=int, i=int, ch0=int)
    cdef int try_get_int(Loader self, int maxsize)

    @cython.locals(ch=Py_UCS4, val=int)
    cdef int get_date(Loader self)

    @cython.locals(ch=Py_UCS4, val=int)
    cdef int get_time(Loader self)

    @cython.locals(ch=Py_UCS4, val=int)
    cdef int get_time_offset(Loader self)

    @cython.locals(ch=Py_UCS4, h=int, m=int,
                   sign=int, v=int, minutes=int)
    cdef object get_tzinfo(Loader self)

    @cython.locals(ch=Py_UCS4, pos0=int, text=unicode, numtype=bint, v=bint)
    cdef object get_number(Loader self)

    @cython.locals(ch=Py_UCS4, pos0=int)
    cdef object get_name(Loader self)

    @cython.locals(ch=Py_UCS4, pos0=int)
    cdef object get_key(Loader self)

    @cython.locals(ch=Py_UCS4)
    cdef inline object try_get_name(Loader self)

    @cython.locals(ch=Py_UCS4)
    cdef inline object try_get_key(Loader self)

    @cython.locals(pos0=int, ch=Py_UCS4)
    cdef object try_get_label(Loader self)

    @cython.locals(ch=Py_UCS4, flag=bint, i=int, val=int,
                   dig=int, ch0=int)
    cdef unicode get_unicode_hex(Loader self)

    @cython.locals(ch=Py_UCS4, text=unicode, pos0=int)
    cdef object get_string(Loader self, Py_UCS4 endch)

    @cython.locals(ch=Py_UCS4, text=unicode, pos0=int)
    cdef object get_base64(Loader self)

    @cython.locals(ch=Py_UCS4)
    cdef void skip_comment(self)

    @cython.locals(ch=Py_UCS4)
    cdef void skip_comments(self)

    @cython.locals(ch=Py_UCS4)
    cdef object get_constant_or_string(Loader self, unicode name)

    @cython.locals(ch=Py_UCS4)
    cdef object get_negative_constant(Loader self)

    @cython.locals(ch=Py_UCS4, val=object, is_multi=bint)
    cdef object get_value(Loader self, int idn)

    @cython.locals(ch=Py_UCS4, val=object,
                   sequence=list, mapping=dict, v=bint, is_multi=bint)
    cdef object get_complex_value(Loader self, object name, int idn)

    @cython.locals(ch=Py_UCS4, val=object,
                   mapping=dict, v=bint)
    cdef object get_sequence_mapping(Loader self, object name, list sequence, int idn)

    @cython.locals(ch=Py_UCS4, val=object,
                   sequence=list, v=bint)
    cdef object get_mapping_sequence(Loader self, object name, dict mapping, int idn)

    @cython.locals(sequence=list, ch=Py_UCS4, val=object)
    cdef object get_list_value(Loader self)

    @cython.locals(sequence=list, v=bint)
    cdef object get_tuple_value(Loader self)

    @cython.locals(ch=Py_UCS4, mapping=dict)
    cdef object get_dict_value(Loader self)

    @cython.locals(ch=Py_UCS4, is_multi=bint)
    cdef bint get_mapping_part(Loader self, dict mapping, list sequence, int idn) except -1

    @cython.locals(ch=Py_UCS4, is_multi=bint)
    cdef bint get_sequence_part(Loader self, list sequence, dict mapping, int idn) except -1

    #cpdef itokens(self)

    #@cython.locals(ch=Py_UCS4)
    #cpdef _itokens(Loader self, int idn)
    
    #@cython.locals(ch=Py_UCS4)
    #cpdef _inamed(Loader self, object name, int idn)    
    