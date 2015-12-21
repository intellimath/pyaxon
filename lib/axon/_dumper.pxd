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

cdef bint IS_NAME=1
cdef bint IS_KEY=0

cdef extern from "pymath.h" nogil:
    bint Py_IS_FINITE(double x)
    bint Py_IS_INFINITY(double x)
    bint Py_IS_NAN(double x)
    bint copysign(double x, double x)

# cdef extern from "math.h" nogil:
#     bint isnan(double x)
#     bint isinf(double x)
#     bint signbit(double x)
#     bint isfinite(double x)

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


from cpython.object cimport PyObject
from cpython.dict cimport PyDict_SetItem, PyDict_GetItem
from cpython.unicode cimport PyUnicode_FromEncodedObject

from axon._objects cimport Node, Attribute, attribute, KeyVal, DictEx, ListEx, TupleEx
from axon._objects cimport c_undefined, reserved_name_dict
#from axon._objects cimport name_cache, c_as_name
from axon._objects cimport StringWriter

from axon._common cimport c_as_unicode, c_as_list, c_as_dict, c_as_tuple, dict_get

#from axon._objects cimport Token
#from axon._objects cimport c_new_token, end_token, dict_token, tuple_token, list_token
#from axon._objects cimport ATOMIC, END, COMPLEX, ATTRIBUTE, KEY, REFERENCE, LABEL, LIST, DICT, TUPLE

from axon.odict cimport OrderedDict as axon_odict

cdef inline Node as_node(object ob):
    return <Node>ob

cdef class PyInt:
    cdef long val

#####################################################################################

cdef object unicode_type
cdef object str_type
cdef object int_type
cdef object long_type
cdef object decimal_type
cdef object bool_type
cdef object float_type
cdef object bytes_type
cdef object bytearray_type
cdef object none_type
cdef object date_type
cdef object time_type
cdef object datetime_type
cdef set simple_types


#####################################################################################

cdef public dict c_reduce_dict
cdef public dict c_all_names

cpdef node_reduce(Node o)
cpdef attribute_reduce(Attribute o)

cdef dict _c_type_reducers

cdef public dict c_factory_dict
cdef public dict c_reduce_dict

cdef class PyPointer:
    cdef unicode (*ptr)(object)

@cython.locals(pyptr=PyPointer)
cdef PyPointer c_new_pyptr(unicode (*p)(object))

@cython.final
cdef class SimpleDumper:

    cdef inline unicode dump_int(SimpleDumper, object)

    @cython.locals(d=double)
    cdef inline unicode dump_float(SimpleDumper, object)

    cdef inline unicode dump_decimal(SimpleDumper, object)

    cdef inline unicode dump_str(SimpleDumper, object)
        
    @cython.locals(text=unicode)
    cdef inline unicode dump_bytes(SimpleDumper, object)

    @cython.locals(n=int, pos=int, pos0=int, text=unicode, ch=Py_UCS4, 
                   flag=bint, is_id=bint)
    cdef inline unicode dump_unicode(SimpleDumper, object)

    cdef inline unicode dump_bool(SimpleDumper, object)

    @cython.locals(d=unicode)
    cdef inline unicode dump_date(self, o)

    cdef inline unicode _dump_tzinfo(SimpleDumper, object)

    cdef inline unicode dump_time(SimpleDumper, object)

    cdef inline unicode dump_datetime(SimpleDumper, object)

    cdef inline unicode dump_none(SimpleDumper, object)


cdef SimpleDumper _simple_dumper

cdef public class SimpleDumpers[type SimpleDumpersType, object SimpleDumpers]:
    cdef public dict mapping

    cdef void add(self, type tp, unicode (*ptr)(object))

    @cython.locals(sd=SimpleDumpers)
    cdef void update(self, object o)

cdef unicode dump_default(object v)

cdef public dict c_simple_dumpers
cdef set simple_types

#
# Dumping
#

@cython.locals(name=unicode, pos0=cython.int, pos=cython.int, text=unicode,
               ch=Py_UCS4, is_qname=cython.bint)
cdef unicode _dump_name(object ob)

@cython.locals(pos0=cython.int, pos=cython.int, text=unicode,
               ch=Py_UCS4, is_qname=cython.bint)
cdef unicode _dump_key(object ob)

#ctypedef unicode *SimpleDumperFunction(object)

@cython.final
cdef public class Dumper[object Dumper, type DumperType]:
    '''
    Dumper class
    '''
    #
    cdef dict c_simple_dumpers
    cdef dict c_type_reducers
    cdef int hsize
    cdef object fd
    cdef StringWriter sfd
    
    cdef SimpleDumper sdumper

    cdef int pretty
    cdef int sorted

    cdef bint crossref
    cdef public dict crossref_dict
    cdef public set crossref_set
    cdef public set crossref_set2
    cdef bint collected
    #
    cdef inline bint is_simple_type(Dumper self, o)
    #
    @cython.locals(i=int)
    cdef inline bint is_all_simple_list(Dumper self, list l, int n)
    #
    @cython.locals(i=int)
    cdef inline bint is_all_simple_tuple(Dumper self, tuple l, int n)
    #
    cdef inline void write(Dumper self, o)
    #
    cdef void pretty_dump_crossref(Dumper self, o)
    #
    cdef void dump_crossref(Dumper self, o)
    #
    cdef bint dump_label(Dumper self, o)
    #
    @cython.locals(flag=bint)
    cdef dump_value(Dumper self, o)
    #
    @cython.locals(flag=bint, this_offset=unicode, new_offset=unicode)
    cdef pretty_dump_value(Dumper self, o, unicode offset, bint use_offset)
    #
    @cython.locals(text=unicode, ptr=PyPointer)
    cdef bint dump_simple_value(Dumper self, o) except -1
    #
    cdef dump_attribute(Dumper self, Attribute attr)
    #
    cdef dump_keyval(Dumper self, KeyVal attr)
    #
    @cython.locals(i=int)
    cdef dump_metadata_values(Dumper self, dict d)
    #
    @cython.locals(i=int)
    cdef dump_dict_values(Dumper self, dict d)
    #
    @cython.locals(i=int)
    cdef dump_odict_values(Dumper self, object d)
    #
    @cython.locals(i=int)
    cdef dump_attrs_sequence(Dumper self, axon_odict d)
    #
    @cython.locals(i=int)
    cdef dump_list_sequence(Dumper self, list l)
    #
    cdef dump_tuple_ex(Dumper self, TupleEx l)
    #
    @cython.locals(i=int)
    cdef dump_tuple_sequence(Dumper self, tuple l)
    #
    cdef dump_list_ex(Dumper self, ListEx l)
    #
    cdef dump_list(Dumper self, list l)
    #
    #cdef dump_set(Dumper self, set l)
    #
    cdef dump_dict_ex(Dumper self, DictEx d)
    #
    cdef dump_dict(Dumper self, dict d)
    #
    cdef dump_odict(Dumper self, object d)
    #
    cdef dump_tuple(Dumper self, tuple d)
    #
    cdef dump_node(Dumper self, Node ob)
    #
    @cython.locals(i=int, j=int, flag=int)
    cdef pretty_dump_node_sequence(Dumper self, list l, unicode w, bint use_offset)
    #
    @cython.locals(i=int, j=int, flag=int, name=unicode)
    cdef pretty_dump_node_attrs(Dumper self, axon_odict l, unicode w, bint use_offset)
    #
    @cython.locals(i=int, n=int)
    cdef pretty_dump_metadata(Dumper self, object d, unicode w, bint use_offset)
    #
    @cython.locals(i=int, n=int)
    cdef pretty_dump_dict_values(Dumper self, object d, unicode w, bint use_offset)
    #
    @cython.locals(i=int, n=int)
    cdef pretty_dump_attribute(Dumper self, Attribute attr, unicode w, bint use_offset)
    #
    @cython.locals(i=int, n=int)
    cdef pretty_dump_keyval(Dumper self, KeyVal attr, unicode w, bint use_offset)
    #
    @cython.locals(i=int, j=int, flag=int)
    cdef pretty_dump_list_sequence(Dumper self, list l, unicode w, bint use_offset)
    #
    @cython.locals(n=int)
    cdef pretty_dump_list_ex(Dumper self, ListEx l, unicode w, bint use_offset)
    #
    @cython.locals(n=int)
    cdef pretty_dump_list(Dumper self, list l, unicode w, bint use_offset)
    #
    #cdef pretty_dump_set(Dumper self, set l, unicode w, bint use_offset)
    #
    cdef pretty_dump_dict_ex(Dumper self, DictEx d, unicode w, bint use_offset)
    #
    cdef pretty_dump_dict(Dumper self, dict d, unicode w, bint use_offset)
    #
    cdef pretty_dump_odict(Dumper self, object d, unicode w, bint use_offset)
    #
    @cython.locals(n=int)
    cdef pretty_dump_tuple_ex(Dumper self, TupleEx l, unicode w, bint use_offset)
    #
    @cython.locals(n=int)
    cdef pretty_dump_tuple(Dumper self, tuple l, unicode w, bint use_offset)
    #
    @cython.locals(w1=unicode, m=int, n=int)
    cdef pretty_dump_node(Dumper self, Node ob, unicode w, bint use_offset)
    #
    @cython.locals(count=PyInt, crossref_set=set, crossref_dict=dict, i=int)
    cdef void apply_crossref(Dumper self)
    #
    @cython.locals(count=PyInt)
    cdef collect_value(Dumper self, o)
    #
    cdef void collect_list(Dumper self, list lst)
    #
    cdef void collect_list_ex(Dumper self, ListEx lst)
    #
    cdef void collect_tuple(Dumper self, tuple lst)
    #
    cdef void collect_set(Dumper self, set lst)
    #
    cdef void collect_dict(Dumper self, dict d)
    #
    cdef void collect_dict_ex(Dumper self, DictEx d)
    #
    cdef void collect_odict(Dumper self, axon_odict d)
    #
    cdef void collect_node(Dumper self, Node d)
    #
    cdef void collect_attribute(Dumper self, Attribute d)
    #
    cdef void collect_keyval(Dumper self, KeyVal d)
    #
    cdef void collect(Dumper self, values)


cdef set _simple_types


# cpdef object dump_tok(Token tok)
