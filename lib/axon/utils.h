#include "Python.h"

#define CH_BETWEEN(x, a, b) (x >= a) && (x <= b)

#if PY_MAJOR_VERSION == 3

    /*PyObject* PyFloat_FromString(PyObject*);*/
    #define c_float_fromstring(text) (PyFloat_FromString((PyObject*)text))

#else

    /*PyObject* PyFloat_FromString(PyObject*, char **);*/
    #define c_float_fromstring(text) (PyFloat_FromString((PyObject*)text, NULL))

#endif

#if PY_MAJOR_VERSION == 3

    #define c_int_fromstring(text) PyLong_FromString(text, NULL, 10)
   
    #define c_int_tostring(ob) _PyLong_Format(ob, 10)

    #define c_int_fromlong(val) PyLong_FromLong(val)
    #define c_int_fromint(val) PyLong_FromLong((long)val)

    #define c_object_to_unicode(o) PyObject_Str(o)

#else

    #define c_int_fromstring(text) PyInt_FromString(text, NULL, 10)

    #define c_int_fromlong(val) PyInt_FromLong(val)
    #define c_int_fromint(val) PyInt_FromLong((long)val)

    #define c_int_tostring(ob)  PyLong_Check(ob)? _PyLong_Format(ob, 10, 0, 1) : _PyInt_Format((PyIntObject*)ob, 10, 1)

    #define c_object_to_unicode(o) PyObject_Unicode(o)

#endif


#if PY_VERSION_HEX >= 0x03030000

    #define c_unicode_substr(text, start, end) \
        PyUnicode_FromKindAndData(PyUnicode_KIND(text), PyUnicode_1BYTE_DATA(text) + start*PyUnicode_KIND(text), end-start)

    #define c_unicode_length(text) PyUnicode_GET_LENGTH(text)
    #define c_bytes_length(text) PyBytes_GET_LENGTH(text)

#else

    #define c_unicode_substr(text, start, end) \
        PyUnicode_FromUnicode(PyUnicode_AS_UNICODE(text)+start, end-start)

    #define c_unicode_length(text) PyUnicode_GET_SIZE(text)
    #define c_bytes_length(text) PyBytes_GET_SIZE(text)

#endif

#define c_dict_size(d) ((PyDictObject*)d)->ma_used

#if PY_VERSION_HEX >= 0x03030000
  #define c_unicode_char(u, i) PyUnicode_READ(PyUnicode_KIND(u), PyUnicode_DATA(u), (i))
  #define c_unicode_write_char(u, i, c) PyUnicode_WRITE(PyUnicode_KIND(u), PyUnicode_DATA(u), (i), (c))
#else
  #define c_unicode_char(u, i) ((Py_UCS4)(PyUnicode_AS_UNICODE(u)[(i)]))
  #define c_unicode_write_char(u, i, c) (PyUnicode_AS_UNICODE(u)[(i)] = (Py_UCS4)c)
#endif

#define current_char(self) c_unicode_char(self->line, self->pos)
#define skip_char(self) (self->pos)++
#define next_char(self) c_unicode_char(self->line, ++(self->pos))

#define get_chunk(self, pos0) c_unicode_substr(self->line, pos0, self->pos)

#define Py_SET_SIZE(o, n) Py_SIZE(o) = n

/*
static CYTHON_INLINE int pylist_append(PyObject* list, PyObject* x) {
    PyListObject* L = (PyListObject*) list;
    Py_ssize_t len = Py_SIZE(list);
    if (L->allocated > len) {
        Py_INCREF(x);
        PyList_SET_ITEM(list, len, x);
        Py_SIZE(list) = len+1;
        return 0;
    }
    return PyList_Append(list, x);
}
*/