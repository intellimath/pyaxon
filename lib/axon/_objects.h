#ifndef __PYX_HAVE__axon___objects
#define __PYX_HAVE__axon___objects

struct UndefinedObject;
struct ReadonlyDict;
struct ReadonlyList;
struct Attribute;
struct EmptyObject;
struct SequenceObject;
struct CollectionObject;
struct MappingObject;
struct ElementObject;
struct InstanceObject;

/* "axon/_objects.pxd":107
 * 
 * @cython.final
 * cdef public class Undefined[object UndefinedObject, type UndefinedType]:             # <<<<<<<<<<<<<<
 *     pass
 * 
 */
struct UndefinedObject {
  PyObject_HEAD
};

/* "axon/_objects.pxd":114
 * #
 * @cython.final
 * cdef public class rdict(dict)[object ReadonlyDict, type ReadonlyDictType]:             # <<<<<<<<<<<<<<
 *     pass
 * 
 */
struct ReadonlyDict {
  PyDictObject __pyx_base;
};

/* "axon/_objects.pxd":121
 * #
 * @cython.final
 * cdef public class rlist(list)[object ReadonlyList, type ReadonlyListType]:             # <<<<<<<<<<<<<<
 *     pass
 * 
 */
struct ReadonlyList {
  PyListObject __pyx_base;
};

/* "axon/_objects.pxd":137
 * #
 * @cython.final
 * cdef public class Attribute[type AttributeType, object Attribute]:             # <<<<<<<<<<<<<<
 *     cdef public unicode name
 *     cdef public object value
 */
struct Attribute {
  PyObject_HEAD
  PyObject *name;
  PyObject *value;
};

/* "axon/_objects.pxd":157
 * #
 * @cython.final
 * cdef public class Empty[type EmptyType, object EmptyObject]:             # <<<<<<<<<<<<<<
 *     cdef public object name
 * 
 */
struct EmptyObject {
  PyObject_HEAD
  PyObject *name;
};

/* "axon/_objects.pxd":164
 * #
 * @cython.final
 * cdef public class Sequence[object SequenceObject, type SequenceType]:             # <<<<<<<<<<<<<<
 *     cdef public object name
 *     cdef public list sequence
 */
struct SequenceObject {
  PyObject_HEAD
  PyObject *name;
  PyObject *sequence;
};

/* "axon/_objects.pxd":173
 * #
 * @cython.final
 * cdef public class Collection[object CollectionObject, type CollectionType]:             # <<<<<<<<<<<<<<
 *     cdef public object name
 *     cdef public list sequence
 */
struct CollectionObject {
  PyObject_HEAD
  PyObject *name;
  PyObject *sequence;
};

/* "axon/_objects.pxd":182
 * #
 * @cython.final
 * cdef public class Mapping[object MappingObject, type MappingType]:             # <<<<<<<<<<<<<<
 *     cdef public object name
 *     cdef public dict mapping
 */
struct MappingObject {
  PyObject_HEAD
  PyObject *name;
  PyObject *mapping;
};

/* "axon/_objects.pxd":191
 * #
 * @cython.final
 * cdef public class Element[object ElementObject, type ElementType]:             # <<<<<<<<<<<<<<
 *     cdef public object name
 *     cdef public dict mapping
 */
struct ElementObject {
  PyObject_HEAD
  PyObject *name;
  PyObject *mapping;
  PyObject *sequence;
};

/* "axon/_objects.pxd":200
 * #
 * @cython.final
 * cdef public class Instance[object InstanceObject, type InstanceType]:             # <<<<<<<<<<<<<<
 *     cdef public object name
 *     cdef public tuple sequence
 */
struct InstanceObject {
  PyObject_HEAD
  PyObject *name;
  PyObject *sequence;
  PyObject *mapping;
};

#ifndef __PYX_HAVE_API__axon___objects

#ifndef __PYX_EXTERN_C
  #ifdef __cplusplus
    #define __PYX_EXTERN_C extern "C"
  #else
    #define __PYX_EXTERN_C extern
  #endif
#endif

__PYX_EXTERN_C DL_IMPORT(PyTypeObject) EmptyType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) ReadonlyListType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) SequenceType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) AttributeType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) ReadonlyDictType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) MappingType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) UndefinedType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) CollectionType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) ElementType;
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) InstanceType;

__PYX_EXTERN_C DL_IMPORT(struct Attribute) *__pyx_f_4axon_8_objects_c_new_attribute(PyObject *, PyObject *);
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_f_4axon_8_objects_c_new_sequence(PyObject *, PyObject *);
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_f_4axon_8_objects_c_new_collection(PyObject *, PyObject *);
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_f_4axon_8_objects_c_new_mapping(PyObject *, PyObject *);
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_f_4axon_8_objects_c_new_element(PyObject *, PyObject *, PyObject *);
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_f_4axon_8_objects_c_new_instance(PyObject *, PyObject *, PyObject *);
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_f_4axon_8_objects_c_new_empty(PyObject *);

__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_v_4axon_8_objects_empty_name;
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_v_4axon_8_objects_c_undescore;
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_v_4axon_8_objects_c_undefined;
__PYX_EXTERN_C DL_IMPORT(PyObject) *__pyx_v_4axon_8_objects_name_cache;
__PYX_EXTERN_C DL_IMPORT(struct ReadonlyDict) *__pyx_v_4axon_8_objects_c_empty_dict;
__PYX_EXTERN_C DL_IMPORT(struct ReadonlyList) *__pyx_v_4axon_8_objects_c_empty_list;

#endif /* !__PYX_HAVE_API__axon___objects */

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC init_objects(void);
#else
PyMODINIT_FUNC PyInit__objects(void);
#endif

#endif /* !__PYX_HAVE__axon___objects */
