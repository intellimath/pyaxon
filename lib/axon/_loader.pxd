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

cimport cython
from cpython.object cimport PyObject, Py_SIZE
#from cpython.list cimport PyList_Append, PyList_SET_ITEM, PyList_GET_ITEM
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

    inline unicode get_chunk(Loader self, int pos0)
    inline int pylist_append(object lst, object x)

from axon._objects cimport c_undefined, empty_name
from axon._objects cimport c_get_cached_name, c_as_name, c_constants
from axon._objects cimport c_new_node, c_new_attribute, c_new_keyval
from axon._objects cimport Attribute, KeyVal, Node, reserved_name_dict
#from axon._objects cimport c_add_metadata

from axon._objects cimport Builder, SafeBuilder, StrictBuilder, MixedBuilder
from axon._objects cimport SimpleBuilder
from axon._common cimport c_as_unicode, c_as_list, c_as_dict, c_as_tuple, dict_get

#from axon._objects cimport c_new_token, c_new_token0, c_new_token1
#from axon._objects cimport end_token, dict_token, tuple_token, list_token
#from axon._objects cimport ATOMIC, END, COMPLEX, ATTRIBUTE, KEY, REFERENCE, LABEL, LIST, DICT, TUPLE

from axon.odict cimport OrderedDict, c_new_odict

cdef object unicode_type, str_type, int_type, long_type
cdef object bool_type, float_type, bytes_type

@cython.final
cdef class Loader:

    cdef object fd
    cdef object readline
    cdef object encoding

    cdef public object line
    cdef bint eof
    cdef public int pos, col
    cdef public int lnum
    cdef public object errto
    
    cdef public bint before08
    
    #cdef dict global_context

    cdef int bc
    cdef int bs
    cdef int bq
    cdef int ba
    
    cdef public Builder builder
    cdef public SimpleBuilder sbuilder

    cdef dict c_constants
    cdef dict labeled_objects

    cdef int[:] ta
    cdef int[:] da
    cdef int[:] to

    cdef bint is_nl
    cdef public int idn
    
    cdef KeyVal keyval
    
    cpdef _check_pairs(Loader self)

    #@cython.locals(is_odict=bint)
    #cpdef iload(Loader self)

    @cython.locals(sequence=list, mapping=OrderedDict, keyval=KeyVal, is_odict=bint)
    cpdef load(Loader self)

    #cdef inline void skip_char(Loader self)
    #cdef inline Py_UCS4 next_char(Loader self)
    #cdef inline Py_UCS4 current_char(Loader self)

    # @cython.locals(ch=Py_UCS4)
    # cdef inline Py_UCS4 moveto_next_token(Loader self) except -1

    @cython.locals(ch=Py_UCS4)
    cdef inline Py_UCS4 skip_spaces(Loader self)

    @cython.locals(ch=Py_UCS4, prev_ch=Py_UCS4)
    cdef inline void skip_whitespace(Loader self)

    @cython.locals(line=unicode, ch=Py_UCS4, n=int)
    cdef next_line(Loader self)

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

    @cython.locals(ch=Py_UCS4, pos0=int, text=unicode, v=bint)
    cdef object get_date_time(Loader self)

    @cython.locals(ch=Py_UCS4, pos0=int)
    cdef inline object _get_name(Loader self)

    @cython.locals(ch=Py_UCS4, pos0=int)
    cdef inline object get_name(Loader self)

    @cython.locals(ch=Py_UCS4, pos0=int)
    cdef inline object get_key(Loader self)

    @cython.locals(pos0=int, ch=Py_UCS4)
    cdef object get_label(Loader self)

    @cython.locals(ch=Py_UCS4, flag=bint, i=int, val=int,
                   dig=int, ch0=int)
    cdef unicode get_unicode_hex(Loader self)

    @cython.locals(ch=Py_UCS4, text=unicode, pos0=int, triple=bint)
    cdef object get_string(Loader self, Py_UCS4 endch)

    @cython.locals(ch=Py_UCS4, text=unicode, pos0=int)
    cdef object get_base64(Loader self)

    @cython.locals(ch=Py_UCS4)
    cdef skip_comment(self)

    @cython.locals(ch=Py_UCS4)
    cdef skip_comments(self)

    # @cython.locals(ch=Py_UCS4)
    # cdef object get_constant_or_string(Loader self, unicode name)

    @cython.locals(ch=Py_UCS4)
    cdef object get_negative_constant(Loader self)

    @cython.locals(ch=Py_UCS4, val=object, name=object, text=object)
    cdef object get_value(Loader self, int idn, int idn0)

    @cython.locals(ch=Py_UCS4, key=object, val=object)
    cdef object get_keyval_dict(self, dict mapping)

    @cython.locals(ch=Py_UCS4, key=object, val=object)
    cdef object get_keyval_odict(self, OrderedDict mapping)

    @cython.locals(ch=Py_UCS4, key=object, val=object, pos0=int, is_key=bint)
    cdef object get_keyval_or_value(self)

    @cython.locals(ch=Py_UCS4, val=object)
    cdef object get_named(self, object name, int idn, int idn0)

    @cython.locals(ch=Py_UCS4, val=object, vals=list, attrs=OrderedDict, 
                   attr=Attribute, flag=int, metadata=dict)
    cdef object get_complex_value(Loader self, object name, int idn, int idn0)

    @cython.locals(ch=Py_UCS4, val=object, attr=Attribute, keyval=KeyVal, metadata=dict)
    cdef object get_attributes(Loader self, OrderedDict attrs, int idn, int idn0)

    @cython.locals(ch=Py_UCS4, val=object, metadata=dict)
    cdef object get_values(Loader self, list vals, int idn, int idn0)

    @cython.locals(sequence=list, mapping=OrderedDict, ch=Py_UCS4, 
                   key=object, val=object, is_odict=bint, keyval=KeyVal, metadata=dict)
    cdef object get_list_value(Loader self)

    @cython.locals(sequence=list, v=bint, metadata=dict)
    cdef object get_tuple_value(Loader self)

    #@cython.locals(ch=Py_UCS4, metadata=dict)
    #cdef object get_metadata(Loader self)

    @cython.locals(mapping=dict, sequence=set, ch=Py_UCS4, 
                   key=object, val=object, is_dict=bint, keyval=KeyVal, metadata=dict)
    cdef object get_dict_value(Loader self)

    # @cython.locals(ch=Py_UCS4, sequence=list)
    # cdef object get_odict_value(Loader self)

