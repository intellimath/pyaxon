# coding: utf-8

cimport cython
from cpython.object cimport PyObject, Py_SIZE
#from cpython.list cimport PyList_Append, PyList_SET_ITEM
from cpython.dict cimport PyDict_SetItem, PyDict_GetItem

#from cpython.unicode cimport PyUnicode_AsASCIIString
#from cpython.bytes cimport PyBytes_AsString
from cpython.long cimport PyLong_FromString
#from cpython.bytes cimport PyBytes_FromStringAndSize, PyBytes_AS_STRING

from cpython.datetime cimport import_datetime, tzinfo
from cpython.datetime cimport time_new, timedelta_new, date_new, datetime_new

cimport cpython.array as array

cdef extern from "unicodeobject.h":
    unicode PyUnicode_FromOrdinal(int ordinal)

cdef extern from "bytesobject.h":
    inline bytes PyBytes_FromStringAndSize(char* p, int n)
    #inline char* PyBytes_AS_STRING(object b)
    #inline int PyBytes_GET_SIZE(object b)

cdef extern from "utils.h":
    inline object c_float_fromstring(object text)
    inline object c_int_fromstring(char *text)
    inline object c_int_fromlong(long val)
    inline object c_int_fromint(int val)

    inline Py_UCS4 c_unicode_char(unicode text, int pos)
    inline unicode c_unicode_substr(unicode text, int start, int end)
    inline int c_unicode_length(unicode text)

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
                               c_new_collection, c_new_element, c_new_empty

cdef object unicode_type, str_type, int_type, long_type
cdef object bool_type, float_type, bytes_type

cdef dict c_constants
cdef dict c_factory_dict

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

cdef object _str2decimal

@cython.locals(n=int, i=int, buf=cython.p_char, num_buffer=bytes)
cdef inline object str2float(unicode text)
cdef inline object str2decimal(unicode text)
@cython.locals(n=int, i=int, buf=cython.p_char, num_buffer=bytes)
cdef inline object str2int(unicode text)

cdef object time_fromargs(int, int, int, int, object tzinfo)
cdef object timedelta_fromargs(int, int, int)
cdef object date_fromargs(int, int, int)
cdef object datetime_fromargs(int, int, int, int, int, int, int, object tzinfo)

cdef object _inf
cdef object _ninf
cdef object _nan

cdef object float_inf()
cdef object float_ninf()
cdef object float_nan()


cdef object c_new_mapping_mixed(object name, dict mapping)
cdef object c_new_sequence_mixed(object name, list sequence)
cdef object c_new_element_mixed(object name, dict mapping, list sequence)
cdef object c_new_instance_mixed(object name, tuple sequence, dict mapping)
cdef object c_new_empty_mixed(object name)

cdef object c_new_mapping_strict(object name, dict mapping)
cdef object c_new_sequence_strict(object name, list sequence)
cdef object c_new_element_strict(object name, dict mapping, list sequence)
cdef object c_new_instance_strict(object name, tuple sequence, dict mapping)
cdef object c_new_empty_strict(object name)

cdef public class Builder[type BuilderType, object Builder]:
    cdef object (*create_mapping)(object, dict)
    cdef object (*create_element)(object, dict, list)
    cdef object (*create_sequence)(object, list)
    cdef object (*create_instance)(object, tuple, dict)
    cdef object (*create_empty)(object)

cdef public class SimpleBuilder[type SimpleBuilderType, object SimpleBuilder]:
    cdef object (*create_int)(unicode)
    cdef object (*create_float)(unicode)
    cdef object (*create_decimal)(unicode)
    cdef object (*create_time)(int, int, int, int, object)
    cdef object (*create_date)(int, int, int)
    cdef object (*create_datetime)(int, int, int, int, int, int, int, object)
    cdef object (*create_tzinfo)(int)
    cdef object (*create_inf)()
    cdef object (*create_ninf)()
    cdef object (*create_nan)()

@cython.locals(builder=Builder)
cdef Builder safe_builder()

@cython.locals(builder=Builder)
cdef Builder strict_builder()

@cython.locals(builder=Builder)
cdef Builder mixed_builder()

cdef dict tz_dict = {}

cdef public class FixedOffsetTZ(tzinfo)[object FixedOffsetTZObject, type FixedOffsetTZType]:
    """Fixed offset in minutes east from UTC."""

    cdef public object minutes

    cdef void _init(FixedOffsetTZ self, object minutes)

cdef object tzinfo_fromargs(int minutes)

@cython.final
cdef class Loader:

    cdef object fd
    cdef object readline
    cdef object encoding

    cdef public unicode line
    cdef bint eof
    cdef public int pos
    cdef public int lnum
    cdef public object errto

    cdef int bc
    cdef int bs
    cdef int bq

    cdef bint json

    cdef Builder builder
    cdef SimpleBuilder sbuilder

    cdef dict c_constants
    cdef dict labeled_objects

    cdef list ta
    cdef list da
    cdef list to

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

    @cython.locals(ch=Py_UCS4, n=int)
    cdef bint get_dots(Loader self)

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

    @cython.locals(ch=Py_UCS4, pos0=int, text=unicode, numtype=bint)
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

    cdef object get_constant_or_string(Loader self, unicode name)

    @cython.locals(ch=Py_UCS4)
    cdef object get_negative_constant(Loader self)

    @cython.locals(ch=Py_UCS4, val=object, is_multi=bint, pos0=int)
    cdef object get_value(Loader self, int idn)

    @cython.locals(ch=Py_UCS4, val=object,
                   sequence=list, mapping=dict, v=bint, values=list) #, pos0=int)
    cdef object get_collection(Loader self, object name, int idn)

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

    #@cython.locals(ch=Py_UCS4)
    #cdef bint get_sequence_part_only(Loader self, list sequence, int idn) except -1

    #@cython.locals(ch=Py_UCS4)
    #cdef bint get_mapping_part_only(Loader self, dict mapping, int idn) except -1