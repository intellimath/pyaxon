# coding: utf-8

# {{LICENCE}}

# cython: language_level=3


##################################################

import cython

from cpython.object cimport PyObject, PyObject_Unicode
#from cpython.dict cimport PyDict_GetItem, PyDict_SetItem
#from cpython.float cimport PyFloat_FromString
from cpython.unicode cimport PyUnicode_AsASCIIString
from cpython.bytes cimport PyBytes_AsString
from cpython.long cimport PyLong_FromString
#from cpython.dict cimport PyDict_SetItem, PyDict_GetItem

from cpython.datetime cimport import_datetime, tzinfo

cdef object _decimal2str

cdef extern from "utils.h":
    inline Py_UCS4 c_unicode_char(unicode text, int pos)
    inline unicode c_unicode_substr(unicode text, int start, int end)
    inline unicode c_object_to_unicode(object o)


#cdef inline object dict_get(object op, object key, object default):
#    cdef PyObject* val = <PyObject*>PyDict_GetItem(op, key)
#    if val == NULL:
#        return default
#    else:
#        return <object>val

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
    elif tp is c_str_type:
        return c_object_to_unicode(ob)
    elif ob is None:
        return c_object_to_unicode('')
    else:
        raise TypeError('This object %r is not unicode compatible' % ob)

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

cdef inline object py_as_name(object name):
    n = name_cache.get(name, None)
    if n is None:
        uname = c_as_unicode(name)
        name_cache[name] = uname
    elif name is None:
        uname = empty_name
    else:
        uname = n
    return uname

# ----------------------------------------
# Datatypes
# ----------------------------------------


ctypedef PyObject* PyObjectPtr

cdef public unicode empty_name
cdef public unicode c_undescore
cdef public object c_undefined

cdef public dict name_cache

cdef object c_str_type

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
@cython.final
cdef public class Empty[type EmptyType, object EmptyObject]:
    cdef public object name

#
# Sequence
#
@cython.final
cdef public class Sequence[object SequenceObject, type SequenceType]:
    cdef public object name
    cdef public list sequence
    #

#
# Collection
#
@cython.final
cdef public class Collection[object CollectionObject, type CollectionType]:
    cdef public object name
    cdef public list sequence
    #

#
# Object
#
@cython.final
cdef public class Mapping[object MappingObject, type MappingType]:
    cdef public object name
    cdef public dict mapping
    #
#
#
# Element
#
@cython.final
cdef public class Element[object ElementObject, type ElementType]:
    cdef public object name
    cdef public dict mapping
    cdef public list sequence
    #
#
# Construct
#
@cython.final
cdef public class Instance[object InstanceObject, type InstanceType]:
    cdef public object name
    cdef public tuple sequence
    cdef public dict mapping
    #

@cython.locals(s=Sequence)
cdef public object c_new_sequence(object name, list sequence)
#
@cython.locals(s=Collection)
cdef public object c_new_collection(object name, list sequence)
#
@cython.locals(o=Mapping)
cdef public object c_new_mapping(object name, dict mapping)
#
@cython.locals(e=Element)
cdef public object c_new_element(object name, dict mapping, list sequence)
#
@cython.locals(e=Instance)
cdef public object c_new_instance(object name, tuple args, dict mapping)

@cython.locals(e=Empty)
cdef public object c_new_empty(object name)

cdef public dict c_factory_dict

cdef class Builder:
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef class SafeBuilder(Builder):
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef class StrictBuilder(Builder):
    #cdef public SafeBuilder builder
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef class MixedBuilder(Builder):
    cdef public SafeBuilder builder
    cdef public object create_mapping(self, object, dict)
    cdef public object create_element(self, object, dict, list)
    cdef public object create_sequence(self, object, list)
    cdef public object create_instance(self, object, tuple, dict)
    cdef public object create_empty(self, object)

cdef public class GenericBuilder(Builder)[object GenericBuilderObject, type GenericBuilderType]:
    cdef object create_mapping(self, object, dict)
    cdef object create_element(self, object, dict, list)
    cdef object create_sequence(self, object, list)
    cdef object create_instance(self, object, tuple, dict)
    cdef object create_empty(self, object)

#cdef Builder safe_builder = SafeBuilder()
#cdef Builder strict_builder = StrictBuilder()
#cdef Builder mixed_builder = MixedBuilder()

cdef dict c_builder_dict

cdef inline Builder c_get_builder(object mode):
    return <Builder>c_builder_dict.get(mode, None)

cpdef Builder get_builder(object)


####################################################################

cdef unicode NAME_IS_EMPTY

cdef class StringReader:
    cdef unicode buffer
    cdef int pos
    cdef int n

    @cython.locals(ch=Py_UCS4, line=unicode, buffer=unicode,
                   pos=int, pos0=int, n=int)
    cpdef unicode readline(StringReader self)

    cpdef close(StringReader self)

cdef public class timezone(tzinfo)[object TimeZoneUTCObject, type TimeZoneUTCType]:
    """Fixed offset in minutes east from UTC."""

    cdef public object offset
    cdef public object name
