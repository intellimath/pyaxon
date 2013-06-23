#ifndef __PYX_HAVE__axon___loader
#define __PYX_HAVE__axon___loader

struct Builder;
struct SimpleBuilder;
struct FixedOffsetTZObject;

/* "axon/_loader.pxd":141
 * cdef object c_new_empty_strict(object name)
 * 
 * cdef public class Builder[type BuilderType, object Builder]:             # <<<<<<<<<<<<<<
 *     cdef object (*create_mapping)(object, dict)
 *     cdef object (*create_element)(object, dict, list)
 */
struct Builder {
  PyObject_HEAD
  PyObject *(*create_mapping)(PyObject *, PyObject *);
  PyObject *(*create_element)(PyObject *, PyObject *, PyObject *);
  PyObject *(*create_sequence)(PyObject *, PyObject *);
  PyObject *(*create_instance)(PyObject *, PyObject *, PyObject *);
  PyObject *(*create_empty)(PyObject *);
};

/* "axon/_loader.pxd":148
 *     cdef object (*create_empty)(object)
 * 
 * cdef public class SimpleBuilder[type SimpleBuilderType, object SimpleBuilder]:             # <<<<<<<<<<<<<<
 *     cdef object (*create_int)(unicode)
 *     cdef object (*create_float)(unicode)
 */
struct SimpleBuilder {
  PyObject_HEAD
  PyObject *(*create_int)(PyObject *);
  PyObject *(*create_float)(PyObject *);
  PyObject *(*create_decimal)(PyObject *);
  PyObject *(*create_time)(int, int, int, int, PyObject *);
  PyObject *(*create_date)(int, int, int);
  PyObject *(*create_datetime)(int, int, int, int, int, int, int, PyObject *);
  PyObject *(*create_tzinfo)(int);
  PyObject *(*create_inf)(void);
  PyObject *(*create_ninf)(void);
  PyObject *(*create_nan)(void);
};

/* "axon/_loader.pxd":171
 * cdef dict tz_dict = {}
 * 
 * cdef public class FixedOffsetTZ(tzinfo)[object FixedOffsetTZObject, type FixedOffsetTZType]:             # <<<<<<<<<<<<<<
 *     """Fixed offset in minutes east from UTC."""
 * 
 */
struct FixedOffsetTZObject {
  PyDateTime_TZInfo __pyx_base;
  struct __pyx_vtabstruct_4axon_7_loader_FixedOffsetTZ *__pyx_vtab;
  PyObject *minutes;
};

#ifndef __PYX_HAVE_API__axon___loader

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

__PYX_EXTERN_C DL_IMPORT(PyTypeObject) BuilderType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) FixedOffsetTZType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) SimpleBuilderType;

#endif /* !__PYX_HAVE_API__axon___loader */

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC init_loader(void);
#else
PyMODINIT_FUNC PyInit__loader(void);
#endif

#endif /* !__PYX_HAVE__axon___loader */
