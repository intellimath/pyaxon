# coding: utf-8

# {{LICENCE}}

import sys

cimport cython

cdef extern from "math.h":
    bint isnan(double x)
    bint isinf(double x)
    bint signbit(double x)
    bint isfinite(double x)

cdef extern from "floatobject.h":
    double PyFloat_AS_DOUBLE(object)

cdef extern from "utils.h":
    inline int c_unicode_length(unicode text)
    inline unicode c_unicode_substr(unicode text, int start, int end)


from axon._objects cimport Empty, Mapping, Element, Sequence, Instance, Collection, Undefined
#from axon._objects cimport c_new_element, c_new_empty, c_new_mapping, c_new_construct, c_new_sequence
#from axon._objects cimport c_reduce_dict, c_simple_dumpers, simple_types
#from axon._objects cimport SimpleDumpers, PyPointer
from axon._objects cimport c_undefined
from axon._objects cimport name_cache, empty_name, c_as_unicode, c_as_name

# cdef inline unicode c_as_unicode(object ob):
#     if type(ob) is unicode:
#         return ob
#
#     if type(ob) == type(''):
#         return unicode(ob)
#
#     if ob is None:
#         return unicode('')
#
#     raise TypeError('This object %r is not unicode compatible' % ob)

# cdef inline c_as_name(object name):
#     n = name_cache.get(name, None)
#     if n is None:
#         uname = c_as_unicode(name)
#         name_cache[name] = uname
#     elif name is None:
#         uname = empty_name
#     else:
#         uname = n
#     return uname


cdef class PyInt:
    cdef long val

#####################################################################################

cdef public dict c_reduce_dict
cdef public dict c_all_names

cpdef mapping_reduce(Mapping o)
#
cpdef element_reduce(Element o)
#
cpdef sequence_reduce(Sequence o)
#
cpdef collection_reduce(Collection o)
#
cpdef instance_reduce(Instance o)
#
cpdef empty_reduce(Empty o)
#

cdef unicode _set_name
cdef unicode _tuple_name
cdef unicode _list_name
cdef unicode _dict_name

cpdef set_reduce(o)
#
cpdef tuple_reduce(o)
#
cpdef dict_reduce(o)
#
cpdef list_reduce(o)

cdef dict _c_type_reducers

cdef public dict c_factory_dict
cdef public dict c_reduce_dict

cdef dict c_simple_dumpers
cdef set simple_types

cdef class PyPointer:
    cdef unicode (*ptr)(object)

@cython.locals(pyptr=PyPointer)
cdef PyPointer c_new_pyptr(unicode (*p)(object))

cdef public class SimpleDumpers[type SimpleDumpersType, object SimpleDumpers]:
    cdef public dict mapping

    cdef void add(self, type tp, unicode (*ptr)(object))

    @cython.locals(sd=SimpleDumpers)
    cdef void update(self, object o)

@cython.locals(line=unicode, pos0=int, pos=cython.uint, text=unicode)
cdef unicode _dump_unicode(object ob)

cdef unicode _dump_str(object line)

cdef unicode _dump_bool(object o)

cdef unicode _dump_date(object o)

@cython.locals(sign=cython.bint)
cdef object _dump_tzinfo(object o)

@cython.locals(t=object)
cdef unicode _dump_time(object o)

@cython.locals(dt=object, sign=cython.bint)
cdef unicode _dump_datetime(object o)

cdef unicode _dump_none(object o)

cdef unicode _dump_int(object o)

@cython.locals(text=unicode)
cdef unicode _dump_bytes(object o)

cdef unicode _dump_long(object o)

@cython.locals(d=double)
cdef unicode _dump_float(object o)

@cython.locals(val=unicode)
cdef unicode _dump_decimal(object d)

cdef unicode _dump_undef(object d)

cdef unicode dump_default(object v)

cdef dict c_simple_dumpers
cdef set simple_types

#
# Dumping
#

@cython.locals(name=unicode, pos0=cython.int, pos=cython.int, text=unicode,
               ch=Py_UCS4, is_qname=cython.bint)
cdef unicode _dump_name(object ob, bint quote)

#ctypedef unicode *SimpleDumperFunction(object)

@cython.final
cdef public class Dumper[object Dumper, type DumperType]:
    '''
    Dumper class
    '''
    #
    cdef dict c_simple_dumpers
    cdef dict c_type_reducers
    cdef object write
    cdef long size, max_size
    cdef int nsize

    cdef int pretty
    cdef int sorted

    cdef bint crossref
    cdef dict crossref_dict
    cdef set crossref_set
    cdef set crossref_set2

    cdef bint quote
    #
    cdef void _pretty_dump_crossref(Dumper self, o)
    #
    cdef void _dump_crossref(Dumper self, o)
    #
    cdef bint _dump_label(Dumper self, o)
    #
    cdef int _dump(Dumper self, o) except -1
    #
    @cython.locals(text=unicode, ptr=PyPointer)
    cdef void _dump_value(Dumper self, o, dumper)
    #
    @cython.locals(i=int, text=unicode)
    cdef int _dump_dict_sequence(Dumper self, dict d) except -1
    #
    @cython.locals(i=int, text=unicode)
    cdef int _dump_attr_sequence(Dumper self, dict d) except -1
    #
    @cython.locals(i=int)
    cdef int _dump_list_sequence(Dumper self, list l) except -1
    #
    @cython.locals(i=int)
    cdef int _dump_set_sequence(Dumper self, set l) except -1
    #
    @cython.locals(i=int)
    cdef int _dump_tuple_sequence(Dumper self, tuple l) except -1
    #
    cdef int dump_list(Dumper self, list l) except -1
    #
    #cdef int dump_set(Dumper self, set l) except -1
    #
    cdef int dump_dict(Dumper self, dict d) except -1
    #
    #cdef int dump_tuple(Dumper self, tuple d) except -1
    #
    @cython.locals(text=unicode)
    cdef int _pretty_dump_dict_sequence(Dumper self, dict d, unicode w, bint use_offset) except -1
    #
    @cython.locals(text=unicode)
    cdef int _pretty_dump_attr_sequence(Dumper self, dict d, unicode w, bint use_offset) except -1
    #
    cdef int _pretty_dump_list_sequence(Dumper self, list l, unicode w, bint use_offset) except -1
    #
    cdef int _pretty_dump_tuple_sequence(Dumper self, tuple l, unicode w, bint use_offset) except -1
    #
    cdef int pretty_dump_list(Dumper self, list l, unicode w, bint use_offset) except -1
    #
    #cdef int pretty_dump_set(Dumper self, set l, unicode w, bint use_offset) except -1
    #
    cdef int pretty_dump_dict(Dumper self, dict d, unicode w, bint use_offset) except -1
    #
    #cdef int pretty_dump_tuple(Dumper self, tuple l, unicode w, bint use_offset) except -1
    #
    cdef int dump_collection(Dumper self, unicode name, list collection) except -1
    #
    cdef int dump_content(Dumper self, tuple items) except -1
    #
    @cython.locals(name=unicode, i=cython.uint, j=cython.uint,
                   n=cython.uint, flag=cython.uint)
    cdef int _dump_with_reducer(Dumper self, reducer, o) except -1
    #
    @cython.locals(this_offset=unicode, new_offset=unicode)
    cdef int _pretty_dump(Dumper self, o, unicode offset, bint use_offset) except -1
    #
    @cython.locals(i=int, n=int, atext=list, vtext=list, name=unicode,
                   offset1=unicode, use_offset=bint)
    cdef int _pretty_dump_with_reducer(Dumper self, reducer, o, unicode offset) except -1
    #
    @cython.locals(count=PyInt, crossref_set=set, crossref_dict=dict, i=int)
    cdef void apply_crossref(Dumper self)
    #
    @cython.locals(count=PyInt)
    cdef int _collect(Dumper self, o) except -1
    #
    cdef int _collect_list(Dumper self, list lst) except -1
    #
    cdef int _collect_tuple(Dumper self, tuple lst) except -1
    #
    cdef int _collect_set(Dumper self, set lst) except -1
    #
    cdef int _collect_dict(Dumper self, dict d) except -1
    #
    @cython.locals(n=int)
    cdef int _collect_with_reducer(Dumper self, reducer, o) except -1
    #
    cdef int collect(Dumper self, values) except -1


cdef set _simple_types
cdef bint is_simple_type(Dumper self, object tp)
