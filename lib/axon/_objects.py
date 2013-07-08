# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3

# {{LICENCE}}

#
# ----------------------------------------
# Datatypes
# ----------------------------------------

from axon.errors import error
import axon.errors as errors

from axon.types import str_type

c_str_type = str_type

class Undefined:
    def __repr__(self):
        return '?'
    def __str__(self):
        return '??'

def isundef(o):
    return type(o) is Undefined

c_undefined = Undefined()
undef = c_undefined

def _error_readonly(self):
    return AttributeError(
        'Readonly object type %r don\'t support assigning items or attributes' \
        % type(self))

def _error_empty_mapping(self):
    return KeyError(
        'Object %r contains an empty mapping' \
        % type(self))

def _error_empty_sequence(self):
    return KeyError(
        'Object %r contains an empty sequence' \
        % type(self))

def _error_invalid_name(name):
    return KeyError('Invalid name: %r' % type(name))

#####################################################
# name cache
#####################################################

c_undescore = '_'
empty_name = ''

name_cache = {None: empty_name, c_undescore: c_undescore}

def clear_all_names():
    name_cache = {}

def as_unicode(o):
    return c_as_unicode(o)

def as_list(o):
    return c_as_list(o)

def as_dict(o):
    return c_as_dict(o)

def as_tuple(o):
    return c_as_tuple(o)

#
# Readonly dict
#
class rdict(dict):
    #
    def __setitem__(self, key, item):
        raise _error_readonly(self)
    #
    def setdefault(self, key, default):
        raise _error_readonly(self)
    #
    def __delitem__(self, key):
        raise _error_readonly(self)
    #
    def __richcmp__(self, other, op):
        if type(self) is rdict:
            if op == 2:
                return dict.__eq__(self, other)
            elif op == 3:
                return not dict.__eq__(self, other)
            raise TypeError('This type of comparison is not supported')
        else:
            raise TypeError('The type of %r is not rdict' % type(self))
    #
#
# Readonly list
#
class rlist(list):
    #
    def __setitem__(self, index, item):
        raise _error_readonly(self)
    #
    def append(self, item):
        raise _error_readonly(self)
    #
    def extend(self, items):
        self._error_readonly(self)
    #
    def __delitem__(self, index):
        raise _error_readonly(self)
    #
    def __richcmp__(self, other, op):
        if type(self) is rlist:
            if op == 2:
                return list.__eq__(self, other)
            elif op == 3:
                return not list.__eq__(self, other)
            raise TypeError('This type of comparison is not supported')
        else:
            raise TypeError('The type of %r is not rlist' % type(self))

c_empty_dict = rdict({})
c_empty_list = rlist([])

#
# Name
#
# @cython.final
# cdef public class Name[type SimpleonNameType, object SimpleonName]:
#     cdef unicode c_name
#     #
#     property name:
#         def __get__(self):
#             return self.c_name
#     #
#     def __init__(self, unicode name):
#         self.c_name = name
#     #
#     def __hash__(self):
#         return self.c_name.__hash__()
#     #
#     def __repr__(self):
#         return self.c_name
#
# cdef public object c_new_name(unicode name):
#     cdef Name n = <Name>(Name.__new__(Name))
#     n.c_name = name
#     return n
#
# def name(unicode uname):
#     cdef Name n = <Name>(Name.__new__(Name))
#     if type(uname) is unicode:
#         n.c_name = <unicode>uname
#     else:
#         n.c_name = unicode(uname)
#     return n

#
#
#

class NamedValue:
    #
    def __init__(self, name, value):
        self.__name__ = value
        self.__value__ = value
    #
    def __getitem__(self, index):
        return self.__value__[index]
    #
    def __setitem__(self, index, value):
        self.__value__[index] = value
    #
    def __getattr__(self, name):
        return getattr(self.__value__, name)
    #
    def __isinstancecheck__(cls, inst):
        return isinstance(inst.__value__, cls)
    #

def named(name, value):
    return NamedValue(name, value)

#
# Attribute
#
class Attribute:
    #
    def __init__(self, name, value):
        self.name = c_as_name(name)
        self.value = value
    #
    def __getitem__(self, index):
        if index == 0:
            return self.name
        elif index == 1:
            return self.value
        else:
            raise IndexError('Index out of range')
    #
    def __repr__(self):
        return self.name + ':' + repr(self.value)
    #


def new_attribute(name, value):
    a = Attribute.__new__(Attribute)
    a.name = c_as_unicode(name)
    a.value = value
    return a

def c_new_attribute(name, value):
    a = Attribute.__new__(Attribute)
    a.name = name
    a.value = value
    return a

#
#
#

class Attrs(object):
    #
    def __getattr__(self, name):
        return self.mapping[name]
    #
    def __setattr__(self, name, value):
        self.mapping[name] = value
    #
    def __repr__(self):
        return repr(self.mapping)

def new_attrs(mapping):
    attrs = Attrs.__new__(Attrs)
    attrs.mapping = mapping
    return attrs

#
# Empty
#
class Empty:
    '''
    Empty named complex value.

    .. py:attribute:: _name

    Name of complex value

    .. py:attribute:: _mapping

    Dictionary of attributes.

    .. py:attribute:: _sequence

    List of values.

    '''
    @property
    def mapping(self):
        return c_empty_dict
    #
    @property
    def sequence(self):
        return c_empty_list
    #
    @property
    def a(self):
        return new_attrs(c_empty_dict)
    #
    def __init__(self, name, sequences=None):
        self.name = c_as_name(name)
    #
#     def __richcmp__(self, other, op):
#         v = self.name == other.name and  \
#             len(other.mapping) == 0 and \
#             len(other.sequence) == 0
#         if op == 2:
#             return v
#         elif op == 3:
#             return not v
#         else:
#             raise TypeError('This type of comparison is not supported')
#     #
    def __repr__(self):
        return 'empty(' + repr(self.name) + ')'
    #
    def as_mapping(self, mapping=None):
        return c_new_mapping(self.name, c_as_dict(mapping))
    #
    def as_sequence(self, sequence=None):
        return c_new_sequence(self.name, c_as_list(sequence))
    #
    def as_element(self, mapping=None, sequence=None):
        return c_new_element(self.name, c_as_dict(mapping), c_as_list(sequence))
            #
    def as_instance(self, sequence=None, mapping=None):
        return c_new_instance(self.name, c_as_tuple(sequence), c_as_dict(mapping))



#
# Sequence
#
class Sequence(object):
    '''
    Named sequence of values.

    .. py:attribute:: _name

    Name of sequence.

    .. py:attribute:: _mapping

    Empty dictionary of attributes.

    .. py:attribute:: _sequence

    List of values.

    '''
    #
    @property
    def mapping(self):
        return None
    #
    @property
    def a(self):
        return new_attrs(c_empty_dict)
    #
    def __init__(self, name, sequence=None):
        self.name = c_as_name(name)
        self.sequence = c_as_list(sequence)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, val):
        self.sequence[index] = val
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Sequence:
#             v = (self.name == other.name) and (self.sequence == other.sequence)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def __repr__(self):
        return 'sequence(' + \
                ', '.join([repr(x) for x in (self.name, self.sequence) if x]) + ')'
    #
    def as_mapping(self):
        raise error("Sequence->Mapping convertion isn't available")
    #
    def as_sequence(self):
        return self
    #
    def as_element(self, mapping=None):
        return c_new_element(self.name, c_as_dict(mapping), self.sequence)
    #
    def as_instance(self, mapping=None):
        return c_new_instance(self.name, tuple(self.sequence), c_as_dict(mapping))

#
# Mapping
#
class Mapping:
    '''
    Named mapping containing pairs of `name`/`value`.

    .. py:attribute:: _name

    Name of mapping

    .. py:attribute:: _mapping

    Mapping containing pairs of name: value.

    .. py:attribute:: _sequence

    Empty list of values.

    '''
    #
    @property
    def sequence(self):
        return None
    #
    @property
    def a(self):
        return new_attrs(self.mapping)
    #
    def __init__(self, name, mapping=None):
        self.name = c_as_name(name)
        self.mapping = c_as_dict(mapping)
    #
    def get(self, name, default=undef):
        return self.mapping.get(name, default)
    #
    def set(self, name, val):
        self.mapping[name] = val
    #
    def update(self, map):
        self.mapping.update(map)
    #
    def __contains__(self, name):
        return name in self.mapping
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Mapping:
#             v = (self.name == other.name) and (self.mapping == other.mapping)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
#     #
    def __repr__(self):
        return  'mapping(' + \
                ', '.join([repr(x) for x in (self.name, self.mapping) if x]) + ')'
    #
    def as_mapping(self):
        return self
    #
    def as_sequence(self):
        raise error("Mapping->Sequence convertion isn't available")
    #
    def as_element(self, sequence=None):
        return c_new_element(self.name, self.mapping, c_as_list(sequence))
    #
    def as_instance(self, sequence=None):
        return c_new_instance(self.name, c_as_tuple(sequence), self.mapping)

#
#
# Element
#
class Element:
    '''
    Named mapping containing list of values.

    .. py:attribute:: _name

    Name of element

    .. py:attribute:: _mapping

    Mapping containing pairs of `name`/`value`.

    .. py:attribute:: _sequence

    Child list of values.

    '''
    #
    @property
    def a(self):
        return new_attrs(self.mapping)
    #
    def __init__(self, name, mapping, sequence=None):
        self.name = c_as_name(name)
        self.mapping = c_as_dict(mapping)
        self.sequence = c_as_list(sequence)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, val):
        self.sequence[index] = val
    #
    def __contains__(self, name):
        return name in self.mapping
    #
    def get(self, name, default=undef):
        return self.mapping.get(name, default)
    #
    def set(self, name, val):
        self.mapping[name] = val
    #
    def update(self, map):
        self.mapping.update(map)
    #
    def append(self, sub):
        self.sequence.append(sub)
    #
    def extend(self, subs):
        self.sequence.extend(subs)
    #
    def __repr__(self):
        return  'element(' + \
                ', '.join([repr(x) for x in (self.name, self.mapping, self.sequence) if x]) + ')'
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Element:
#             v = (self.name == other.name) and \
#                 (self.sequence == other.sequence) and \
#                 (self.mapping == other.mapping)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def as_mapping(self):
        raise error("Element->Mapping convertion isn't available")
    #
    def as_sequence(self):
        raise error("Element->Sequence convertion isn't available")
    #
    def as_element(self):
        return self
    #
    def as_instance(self):
        return c_new_instance(self.name, tuple(self.sequence), self.mapping)

#
# Instance
#
class Instance:
    '''
    Named sequence containing pairs of name: value.

    .. py:attribute:: _name

    Name of object.

    .. py:attribute:: _mapping

    Mapping containing optional values in form of `name`: `value` pairs.

    .. py:attribute:: _sequence

    List of requiered values.

    '''
    #
    @property
    def a(self):
        return new_attrs(self.mapping)
    #
    def __init__(self, name, sequence=None, mapping=None):
        self.name = c_as_name(name)
        self.sequence = c_as_tuple(sequence)
        self.mapping = c_as_dict(mapping)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, val):
        self.sequence[index] = val
    #
    def get(self, name, default=undef):
        return self.mapping.get(name, default)
    #
    def set(self, name, val):
        self.mapping[name] = val
    #
    def update(self, map):
        self.mapping.update(map)
    #
    def append(self, sub):
        self.sequence.append(sub)
    #
    def extend(self, subs):
        self.sequence.extend(subs)
    #
    def __repr__(self):
        return  'instance(' + \
                ', '.join([repr(x) for x in (self.name, self.sequence, self.mapping) if x]) + ')'
    #
#     def __richcmp__(self, other, op):
#         if type(self) is Instance:
#             s0 = self
#             s = other
#             v = (self.name == other.name) and \
#                 (self.sequence == other.sequence) and \
#                 (self.mapping == other.mapping)
#             if op == 2:
#                 return v
#             elif op == 3:
#                 return not v
#             else:
#                 raise TypeError(
#                     'This type of comparison is not supported')
#         else:
#             raise TypeError(
#                 'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def as_mapping(self):
        raise error("Instance->Mapping convertion isn't available")
    #
    def as_sequence(self):
        raise error("Instance->Sequence convertion isn't available")
    #
    def as_element(self):
        return c_new_element(self.name, self.mapping, list(self.sequence))
    #
    def as_instance(self):
        return self


#
# Collection
#
class Collection(object):
    '''
    Sequence of named complex values with the same name

    .. py:attribute:: name

    Name of sequence.

    '''
    #
    def __init__(self, name, sequence=None):
        self.name = c_as_name(name)
        self.sequence = []
        for o in sequence:
            if o.name != name:
                errors.error_expected_same_name(self, name)
            self.sequence.append(o)
    #
    def __getitem__(self, index):
        return self.sequence[index]
    #
    def __setitem__(self, index, o):
        if o.name != self.name:
            errors.error_expected_same_name(self, self.name)
        self.sequence[index] = o
    #
    def append(self, o):
        if o.name != self.name:
            errors.error_expected_same_name(self, self.name)
        self.sequence.append(o)
    #
    def __richcmp__(self, other, op):
        if type(self) is Collection:
            v = (self.name == other.name) and (self.sequence == other.sequence)
            if op == 2:
                return v
            elif op == 3:
                return not v
            else:
                raise TypeError(
                    'This type of comparison is not supported')
        else:
            raise TypeError(
                'Types %r and %r are not comparable at all' % (type(self), type(other)))
    #
    def __iter__(self):
        return iter(self.sequence)
    #
    def __len__(self):
        return len(self.sequence)
    #
    def __repr__(self):
        return 'collection(' + repr(self.name) + ', ' + \
            ', '.join([repr(v) for v in self.sequence]) + ')'
    #
    def as_mapping(self):
        raise error("Collection->Mapping convertion isn't available")
    #
    def as_sequence(self):
        raise error("Collection->Sequence convertion isn't available")
    #
    def as_element(self, mapping=None):
        raise error("Collection->Element convertion isn't available")
    #
    def as_instance(self, mapping=None):
        raise error("Collection->Instance convertion isn't available")

####################################################################

def c_new_sequence(name, sequence):
    s = Sequence.__new__(Sequence)
    s.name = name
    s.sequence = sequence
    return s

def c_new_collection(name, sequence):
    s = Collection.__new__(Collection)
    s.name = name
    s.sequence = sequence
    return s

def c_new_mapping(name, mapping):
    o = Mapping.__new__(Mapping)
    o.name = name
    o.mapping = mapping
    return o
#
def c_new_element(name, mapping, sequence):
    e = Element.__new__(Element)
    e.name = name
    e.mapping = mapping
    e.sequence = sequence
    return e
#
def c_new_instance(name, args, mapping):
    e = Instance.__new__(Instance)
    e.name = name
    e.sequence = args
    e.mapping = mapping
    return e

def c_new_empty(name):
    e = Empty.__new__(Empty)
    e.name = name
    return e

#####################################################################################

NAME_IS_EMPTY = 'Name is empty'

def sequence(name, sequence=None):
    '''
    Factory function for creating named sequence.

    :param name:

        name of sequence.

    :param sequence:

        python sequence containing values.
    '''
    return c_new_sequence(c_as_name(name), c_as_list(sequence))
#
def collection(name, sequence=None):
    '''
    Factory function for creating named sequence.

    :param name:

        name of sequence.

    :param sequence:

        python sequence containing values.
    '''
    lst = c_as_list(sequence)
    for o in lst:
        if o.name != name:
            error("Element must have same name '%s'" % name)
    return c_new_collection(c_as_name(name), lst)
#
def mapping(name, mapping=None):
    '''
    Factory function for creating named mapping.

    :param name:

        name of sequence.

    :param mapping:

        python dictionary containing pairs of `name`/`value`.
    '''
    return c_new_mapping(c_as_name(name), c_as_dict(mapping))
#
def element(name, mapping, sequence=None):
    '''
    Factory function for creating named element.

    :param name:

        name of element.

    :param mapping:

        python dictionary containing pairs of `name: value`.

    :param sequence:

        python sequence containing child values.
    '''
    return c_new_element(c_as_name(name), c_as_dict(mapping), c_as_list(sequence))
#
def instance(name, sequence, mapping):
    '''
    Factory function for creating named instance.

    :param name:

        name of object.

    :param sequence:

        python sequence containing required values.

    :param mapping:

        python dictionary containing optional values in form of of `name`: `value` pairs.

    '''
    return c_new_instance(c_as_name(name), c_as_tuple(sequence), c_as_dict(mapping))
#
def empty(name):
    '''
    Factory function for creating empty complex value.

    :param name:

        name of empty complex value.
    '''
    return c_new_empty(c_as_name(name))
#



class StringReader:

    def __init__(self, text):
        self.buffer = text
        self.pos = 0
        self.n = len(text)

    def readline(self):

        buffer = self.buffer
        pos = self.pos
        pos0 = self.pos
        n = self.n

        if pos >= n:
            return ''

        while 1:
            if pos >= n:
                line = c_unicode_substr(buffer, pos0, pos)
                break

            ch = c_unicode_char(buffer, pos)
            if ch == '\n':
                pos += 1
                if pos >= n:
                    line = c_unicode_substr(buffer, pos0, pos)
                    break

                ch = c_unicode_char(buffer, pos)
                if ch == '\r':
                    pos += 1

                line = c_unicode_substr(buffer, pos0, pos)
                break
            elif ch == '\r':
                pos += 1
                if pos >= n:
                    line = c_unicode_substr(buffer, pos0, pos)
                    break

                ch = c_unicode_char(buffer, pos)
                if ch == '\n':
                    pos += 1

                line = c_unicode_substr(buffer, pos0, pos)
                break
            else:
                pos += 1
                #ch = buffer[pos]

        self.pos = pos
        return line

    def close(self):
        self.pos = self.n

