# coding: utf-8

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

from cpython.object cimport PyObject, PyObject_Unicode
from cpython.dict cimport PyDict_GetItem, PyDict_SetItem

cdef extern from "utils.h":
    inline unicode c_object_to_unicode(object o)


cdef inline object dict_get(object op, object key, object default):
    cdef PyObject* val = <PyObject*>PyDict_GetItem(op, key)
    if val == NULL:
        return default
    else:
        return <object>val

cdef inline dict c_as_dict(object ob):
    if type(ob) is dict:
        return <dict>ob
    elif ob is None:
        return {}
    else:
        return dict(ob)

cdef inline list c_as_list(object ob):
    if type(ob) is list:
        return <list>ob
    elif ob is None:
        return []
    else:
        return list(ob)

cdef inline tuple c_as_tuple(object ob):
    if type(ob) is tuple:
        return <tuple>ob
    elif ob is None:
        return ()
    else:
        return tuple(ob)

cdef inline unicode c_as_unicode(object ob):
    tp = type(ob)
    if tp is unicode:
        return <unicode>ob
    elif tp is str:
        return c_object_to_unicode(ob)
    elif ob is None:
        return c_object_to_unicode('')
    else:
        raise TypeError('This object %r is not unicode compatible' % ob)