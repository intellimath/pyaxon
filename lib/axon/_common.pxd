
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
