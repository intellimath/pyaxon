#ifndef __PYX_HAVE__axon___dumper
#define __PYX_HAVE__axon___dumper

struct SimpleDumpers;
struct Dumper;

/* "axon/_dumper.pxd":102
 * cdef PyPointer c_new_pyptr(unicode (*p)(object))
 * 
 * cdef public class SimpleDumpers[type SimpleDumpersType, object SimpleDumpers]:             # <<<<<<<<<<<<<<
 *     cdef public dict mapping
 * 
 */
struct SimpleDumpers {
  PyObject_HEAD
  struct __pyx_vtabstruct_4axon_7_dumper_SimpleDumpers *__pyx_vtab;
  PyObject *mapping;
};

/* "axon/_dumper.pxd":161
 * 
 * @cython.final
 * cdef public class Dumper[object Dumper, type DumperType]:             # <<<<<<<<<<<<<<
 *     '''
 *     Dumper class
 */
struct Dumper {
  PyObject_HEAD
  struct __pyx_vtabstruct_4axon_7_dumper_Dumper *__pyx_vtab;
  PyObject *c_simple_dumpers;
  PyObject *c_type_reducers;
  PyObject *write;
  long size;
  long max_size;
  int nsize;
  int pretty;
  int sorted;
  int crossref;
  PyObject *crossref_dict;
  PyObject *crossref_set;
  PyObject *crossref_set2;
  int quote;
};

#ifndef __PYX_HAVE_API__axon___dumper

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

__PYX_EXTERN_C DL_IMPORT(PyTypeObject) SimpleDumpersType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) DumperType;

__PYX_EXTERN_C DL_IMPORT(PyObject) *c_reduce_dict;
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_v_4axon_7_dumper_c_all_names;
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_v_4axon_7_dumper_c_factory_dict;

#endif /* !__PYX_HAVE_API__axon___dumper */

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC init_dumper(void);
#else
PyMODINIT_FUNC PyInit__dumper(void);
#endif

#endif /* !__PYX_HAVE__axon___dumper */
