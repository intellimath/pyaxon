# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3

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
from cpython.object cimport Py_EQ, Py_NE

from operator import eq as _eq
import sys as _sys
import collections

from axon._common cimport c_as_unicode, c_as_list, c_as_dict, c_as_tuple, dict_get
    
cdef dict _repr_running = {}


cdef class _MappingView:

    cdef OrderedDict _mapping

cdef class _KeysView(_MappingView):
    pass


cdef class _ItemsView(_MappingView):
    pass

cdef class _ValuesView(_MappingView):
    pass

################################################################################
### OrderedDict
################################################################################

@cython.freelist(64)
@cython.final
cdef public class Link[object LinkObject, type LinkType]:
    cdef cython.void *prev
    cdef cython.void *next
    cdef object key
    cdef object val
    
cdef Link link_marker

cdef public class OrderedDict[object OrderedDictObject, type OrderedDictType]:
    cdef Link root
    cdef dict map

cdef public class OrderedDictEx(OrderedDict)[object OrderedDictExObject, type OrderedDictExType]:
    cdef dict metadata

cdef c_init_odict(OrderedDict od, list args)
    
cdef OrderedDict c_new_odict(list args)
cdef OrderedDictEx c_new_odict_ex(list args, dict metadata)
