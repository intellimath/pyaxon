# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3

# {{LICENCE}}

import axon.types as types
#from axon.types import unicode_type, str_type, int_type, long_type
#from axon.types import bool_type, float_type, bytes_type

try:
    import cdecimal as _decimal

except:
    import decimal as _decimal

default_decimal_context = _decimal.getcontext()
_decimal2str = default_decimal_context.to_eng_string

import datetime

try:
    from base64 import encodebytes, decodebytes
except:
    from base64 import encodestring as encodebytes, decodestring as decodebytes

class PyInt:

    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

#
# Reducers
#

def mapping_reduce(o):
    return o.name, o.mapping
#
def element_reduce(o):
    return o.name, o.mapping, o.sequence
#
def sequence_reduce(o):
    return o.name, o.sequence
#
def collection_reduce(o):
    return o.name + '*', o.sequence
#
def instance_reduce(o):
    return o.name, o.sequence, o.mapping
#
def empty_reduce(o):
    return o.name,
#

_set_name = 'set'
_tuple_name = 'tuple'
_list_name = 'list'
_dict_name = 'dict'

def set_reduce(o):
    return _set_name, tuple(o)
#
def tuple_reduce(o):
    return _tuple_name, tuple(o)
#
def dict_reduce(o):
    return _dict_name, o
#
def list_reduce(o):
    return _list_name, o

_c_type_reducers = {
    Mapping: mapping_reduce,
    Element: element_reduce,
    Sequence: sequence_reduce,
    Instance: instance_reduce,
    Collection: collection_reduce,
    Empty: empty_reduce,
    set: set_reduce,
    tuple: tuple_reduce,
    list: list_reduce,
    dict: dict_reduce,
}

#
c_reduce_dict = _c_type_reducers.copy()

#

def reset_reduce():
    c_reduce_dict = _c_type_reducers.copy()

#class Namespace(dict):
#    def __init__(self, **kw):
#        self.__dict__.update(kw)

def reduce(type_, reduce_func = None):
    if reduce_func is None:
        def _factory(factory_func):
            c_reduce_dict[type_] = factory_func
            return factory_func
        return _factory
    else:
        c_reduce_dict[type_] = reduce_func

#
#
#############################################################################
#


#import datetime

class PyPointer:
    pass

def c_new_pyptr(p):
    pyptr = PyPointer.__new__(PyPointer)
    pyptr.ptr = p
    return pyptr

def _dump_unicode(ob):
    line = c_as_unicode(ob)
    pos0 = 0
    pos = 0
    text = '"'

    n = len(line)
    while pos < n:
        if line[pos] == '"':
            if pos != pos0:
                text += line[pos0: pos]
            text += '\\"'
            pos += 1
            pos0 = pos
        else:
            pos += 1

    if pos != pos0:
        text += line[pos0: pos]
    return text + '"'

def _dump_str(line):
    return _dump_unicode(c_as_unicode(line))

def _dump_bool(o):
    #return '⊤' if o else '⊥'
    return 'true' if o else 'false'

def _dump_date(o):
    d = "%d-%02d-%02d" % (o.year, o.month, o.day)
    return d

def _dump_tzinfo(o):
    return str(o)

def _dump_time(o):
    #cdef object t

    if o.second:
        if o.microsecond:
            t = "%02d:%02d:%02d.%06d" % (o.hour, o.minute, o.second, o.microsecond)
        else:
            t = "%02d:%02d:%02d" % (o.hour, o.minute, o.second)
    else:
            t = "%02d:%02d" % (o.hour, o.minute)

    tzinfo = o.tzinfo
    if tzinfo is not None:
        t += _dump_tzinfo(tzinfo)

    return t

def _dump_datetime(o):
    sign = 0

    if o.second:
        if o.microsecond:
            t = "%d-%02d-%02dT%02d:%02d:%02d.%06d" % (o.year, o.month, o.day, o.hour, o.minute, o.second, o.microsecond)
        else:
            t = "%d-%02d-%02dT%02d:%02d:%02d" % (o.year, o.month, o.day, o.hour, o.minute, o.second)
    else:
            t = "%d-%02d-%02dT%02d:%02d" % (o.year, o.month, o.day, o.hour, o.minute)

    tzinfo = o.tzinfo
    if tzinfo is not None:
        t += _dump_tzinfo(tzinfo)

    return c_as_unicode(t)

def _dump_none(o):
    return 'null'

def _dump_int(o):
    return unicode(o)

def _dump_bytes(o):
    #print('###', encodebytes(o), '###')
    text = unicode(encodebytes(o), 'ascii')
    return '|' + text

def _dump_long(o):
    return unicode(o)

def _dump_float(o):
    d = PyFloat_AS_DOUBLE(o)
    if isfinite(d):
        return unicode(o)

    if isnan(d):
        return '?'

    if isinf(d):
        if signbit(d):
            return '-∞'
        else:
            return '∞'

    if signbit(d):
        return '-0'

    return '0'

def _dump_decimal(d):
    #cdef unicode val
    if d.is_finite():
        val  = c_as_unicode(_decimal2str(d))

    elif d.is_nan():
        val = '?'

    elif d.is_infinite():
        if d.is_signed():
            val = '-∞'
        else:
            val = '∞'

    elif d.is_signed():
        val = '-0'
    else:
        val = '0'

    return val + '$'

def _dump_undef(o):
    return '??'

# cdef unicode _dump_Name(object o):
#     return unicode(o)

# cdef void _dump_attribute(Attribute attr, Dumper dumper):
#     dumper.write(_dump_name(attr.c_name))
#     dumper.write(':')
#     dumper._dump(attr.c_value)
#
# cdef void _pretty_dump_attribute(Attribute attr, Dumper dumper, unicode offset):
#     dumper.write(_dump_name(attr.c_name))
#     dumper.write(': ')
#     dumper._pertty_dump(attr.c_value, offset, 0)

def dump_default(v):
    return unicode(v)

c_simple_dumpers = {
    types.int_type: c_new_pyptr(_dump_int),
    types.long_type: c_new_pyptr(_dump_long),
    types.float_type: c_new_pyptr(_dump_float),

    types.str_type: c_new_pyptr(_dump_str),
    types.unicode_type: c_new_pyptr(_dump_unicode),

    types.bytes_type: c_new_pyptr(_dump_bytes),
    types.bool_type: c_new_pyptr(_dump_bool),

    _decimal.Decimal: c_new_pyptr(_dump_decimal),
    datetime.date: c_new_pyptr(_dump_date),
    datetime.time: c_new_pyptr(_dump_time),
    datetime.datetime: c_new_pyptr(_dump_datetime),

    Undefined: c_new_pyptr(_dump_undef),
    type(None): c_new_pyptr(_dump_none),
}

simple_types = set(c_simple_dumpers.keys())

class SimpleDumpers:
    #cdef dict c_mapping

    def __init__(self):
        self.mapping = c_simple_dumpers.copy()

    def add(self, tp, ptr):
        self.mapping[tp] = c_new_pyptr(ptr)

    def update(self, o):
        #cdef SimpleDumpers sd

        if type(o) is dict:
            self.mapping.update(o)
        elif type(o) is SimpleDumpers:
            sd = o
            self.mapping.update(sd.mapping)

def dump_as_str(tp=None):
    if tp is None:
        def _dump_as_str(func):
            c_simple_dumpers[tp] = func
            return func
        return _dump_as_str
    else:
        c_simple_dumpers[tp] = c_new_pyptr(dump_default)


#
# Dumping
#

def _dump_name(ob):
    name = ob
    pos0 = 0
    pos = 0
    text = None

    n = len(name)
    if n == 0:
        raise ValueError('Empty name')

    ch = name[pos]
    if ch.isalpha() or ch == '_':
        pos += 1
    else:
        raise ValueError('Invalid name')
    while pos < n:
        ch = name[pos]
        if ch.isalnum() or ch == '_' or ch == '-':
            pos += 1
        else:
            raise ValueError('Invalid name')

    if pos != pos0:
        if text is None:
            text = name[pos0: pos]
        else:
            text += name[pos0: pos]

    return text

def _dump_key(ob):
    name = ob
    pos0 = 0
    pos = 0
    text = None
    is_qname = 0

    n = len(name)
    while pos < n:
        ch = name[pos]
        if ch.isalnum() or ch == '_':
            pos += 1
        elif ch == '"':
            if pos != pos0:
                if text is None:
                    text = name[pos0, pos]
                else:
                    text += name[pos0: pos]
            text += '\\"'
            pos += 1
            pos0 = pos
            is_qname = 1
        else:
            pos += 1
            is_qname = 1

    if pos != pos0:
        if text is None:
            text = name[pos0: pos]
        else:
            text += name[pos0: pos]

    if is_qname:
        return '"' + text + '"'
    else:
        return text

_simple_types = {
    types.unicode_type, types.str_type, types.int_type, types.long_type,
    types.float_type, types.decimal_type, types.bool_type,
    types.date_type, types.time_type, types.datetime_type}

def is_simple_type(self, o):
    return type(o) in _simple_types or (self.crossref and id(o) in self.crossref_set2)


class Dumper:
    '''
    Dumper class
    '''
    #
    def __init__(self, fd, crossref=0, pretty=0, nsize=1, sorted=1):

        self.max_size = 65000
        self.size = 0

        self.crossref = 1 if crossref else 0
        self.crossref_set = None
        self.crossref_set2 = None
        self.crossref_dict = None

        self.pretty = pretty
        #self.offset = '  '
        self.nsize = nsize

        self.sorted = sorted

        self.c_simple_dumpers = c_simple_dumpers
        self.c_type_reducers = c_reduce_dict

        self.write = fd.write
    #
    def _pretty_dump_crossref(self, o):
        o_id = id(o)
        if o_id in self.crossref_set:
            self.write(' &')

            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
    #
    def _dump_crossref(self, o):
        o_id = id(o)
        if o_id in self.crossref_set:
            self.write('&')

            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
    #
    def _dump_label(self, o):
        o_id = id(o)
        if  o_id in self.crossref_set2:
            self.write('*')
#
            label = self.crossref_dict[o_id]
            self.write(label)
            return 1
        elif  o_id in self.crossref_set:
            self.write('&')
#
            label = self.crossref_dict[o_id]
            self.write(label)
            self.write(' ')
            self.crossref_set2.add(o_id)
            self.crossref_set.remove(o_id)
            return 2
        else:
            return -1
    #
    def _dump(self, o):

        if self.size > self.max_size:
            self.write('\n')
            self.size = 0

        otype = type(o)
        dumper = self.c_simple_dumpers.get(otype, None)
        if dumper is None:
            if self.crossref:
                if self._dump_label(o) == 1:
                    return 0

            if otype is list:
                self.dump_list(o)
            elif otype is dict:
                self.dump_dict(o)
            elif otype is tuple:
                self.dump_tuple(o)
            #elif otype is set:
            #    self.dump_set(o)
            else:
                reducer = self.c_type_reducers.get(otype, None)
                if reducer is None:
                    raise TypeError('There is no reducer for this type: ' + repr(otype))
                else:
                    self._dump_with_reducer(reducer, o)
        else:
            self._dump_value(o, dumper)
    #
    def _pretty_dump(self, o, offset, use_offset):
        this_offset = offset
        new_offset = offset + '  '

        if not use_offset:
            this_offset = ''

        self.write(this_offset)

        otype = type(o)
        dumper = self.c_simple_dumpers.get(otype, None)
        if dumper is None:
            if self.crossref:
                if self._dump_label(o) == 1:
                    return 0

            if otype is list:
                if self.nsize and len(o) <= self.nsize and all([is_simple_type(self, v) for v in o]):
                    self.dump_list(o)
                else:
                    self.pretty_dump_list(o, new_offset, not use_offset)
            elif otype is dict:
                if self.nsize and len(o) <= self.nsize and all([is_simple_type(self, v) for v in o]):
                    self.dump_dict(o)
                else:
                    self.pretty_dump_dict(o, new_offset, not use_offset)
            elif otype is tuple:
                if self.nsize and len(o) <= self.nsize and all([is_simple_type(self, v) for v in o]):
                    self.dump_tuple(o)
                else:
                    self.pretty_dump_tuple(o, new_offset, not use_offset)
            #elif otype is set:
            #    self.pretty_dump_set(o, new_offset, not use_offset)
            else:
                reducer = self.c_type_reducers.get(otype, None)
                if reducer is None:
                    raise TypeError('There is no reducer for this type: ' + repr(otype))
                else:
                    self._pretty_dump_with_reducer(reducer, o, offset)
        else:
            self._dump_value(o, dumper)
    #
    def _dump_value(self, o, dumper):
            if type(dumper) is PyPointer:
                ptr = dumper
                text = ptr.ptr(o)
            else:
                text = dumper(o)
            self.size += len(text)
            self.write(text)
    #
    def _dump_dict_sequence(self, d):
        i = 0

        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        for k,v in items:
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_key(text))
            self.size += len(text)

            self.write(':')
            self._dump(v)
            i += 1
    #
    def _dump_attr_sequence(self, d):
        i = 0

        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        for k,v in items:
            if i > 0:
                self.write(' ')

            text = c_as_unicode(k)
            self.write(_dump_name(text))
            self.size += len(text)

            self.write(':')
            self._dump(v)
            i += 1
    #
    def _dump_list_sequence(self, l):
        i = 0

        for v in l:
            if i > 0:
                self.write(' ')
            self._dump(v)
            i += 1
    #
    def _dump_set_sequence(self, l):
        i = 0

        for v in l:
            if i > 0:
                self.write(' ')
            self._dump(v)
            i += 1
    #
    def _dump_tuple_sequence(self, l):
        i = 0

        for v in l:
            if i > 0:
                self.write(' ')
            self._dump(v)
            i += 1
    #
    def dump_list(self, l):
        self.write('[')
        self._dump_list_sequence(l)
        self.write(']')
    #
#    def dump_set(self, l):
#        if not l:
#            self.write('∅')
#        else:
#            self.write('{')
#            self._dump_set_sequence(l)
#            self.write('}')
    #
    def dump_dict(self, d):
        self.write('{')
        self._dump_dict_sequence(d)
        self.write('}')
    #
    def dump_tuple(self, d):
        self.write('(')
        self._dump_tuple_sequence(d)
        self.write(')')
    #
    def _pretty_dump_dict_sequence(self, d, w, use_offset):
        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        for k,v in items:
            if use_offset:
                self.write('\n')
                self.write(w)
            else:
                use_offset = 0
                self.write(' ')
                use_offset = 1

            text = c_as_unicode(k)
            self.write(_dump_key(text))
            self.write(': ')
            self._pretty_dump(v, w, 0)
    #
    def _pretty_dump_attr_sequence(self, d, w, use_offset):
        if self.sorted:
            items = sorted(d.items())
        else:
            items = d.items()

        for k,v in items:
            if use_offset:
                self.write('\n')
                self.write(w)
            else:
                use_offset = 0
                self.write(' ')
                use_offset = 1

            text = c_as_unicode(k)
            self.write(_dump_name(text))
            self.write(': ')
            self._pretty_dump(v, w, 0)
    #
    def _pretty_dump_list_sequence(self, l, w, use_offset):
        for v in l:
            if use_offset:
                self.write('\n')
                self._pretty_dump(v, w, 1)
            else:
                self.write(' ')
                self._pretty_dump(v, w, 0)
                use_offset = 1
    #
    def _pretty_dump_tuple_sequence(self, l, w, use_offset):
        for v in l:
            if use_offset:
                self.write('\n')
                self._pretty_dump(v, w, 1)
            else:
                self.write(' ')
                self._pretty_dump(v, w, 0)
                use_offset = 1
    #
    def pretty_dump_list(self, l, w, use_offset):
        self.write('[')
        self._pretty_dump_list_sequence(l, w, use_offset)
        self.write(']')
    #
#    def pretty_dump_set(self, l, w, use_offset):
#        if not l:
#            self.write('∅')
#        else:
#            self.write('{')
#            self._pretty_dump_set_sequence(l, w, 0)
#            self.write('}')
    #
    def pretty_dump_dict(self, d, w, use_offset):
        self.write('{')
        self._pretty_dump_dict_sequence(d, w, use_offset)
        self.write('}')
    #
    def pretty_dump_tuple(self, l, w, use_offset):
        self.write('(')
        self._pretty_dump_tuple_sequence(l, w, 0)
        self.write(')')
    #
    def dump_content(self, items):
        for i, item in enumerate(items):

            if item is None:
                continue

            if i == 1:
                self.write(' ')

            tp = type(item)
            if tp is dict:
                self._dump_attr_sequence(item)
            elif tp is tuple:
                self._dump_tuple_sequence(item)
            elif tp is list:
                self._dump_list_sequence(item)
            elif tp is set:
                self._dump_set_sequence(item)
            else:
                for j, v in enumerate(item):
                    if j > 0:
                        self.write(' ')
                    self._dump(v)
    #
    def dump_collection(self, name, collection):
        N = len(collection)
        for i, o in enumerate(collection):
            if self.crossref:
                self.write(' ')
                v =  self._dump_label(o)
                if v == 1:
                    return 0

            self.write('{')

            otype = type(o)
            reducer = self.c_type_reducers.get(otype, None)
            if reducer is None:
                raise TypeError('There is no reducer for this type: ' + repr(otype))
            else:
                items = reducer(o)
                n = len(items)

                if name != items[0]:
                    raise ValueError("Invalid name for collection %s-th item" % i)

                if n < 1 or n > 3:
                    raise ValueError('Reducer returns invalid number of items: %s' % n)
                elif n > 1:
                    self.dump_content(items[1:])

                self.write('}')
    #
    def _dump_with_reducer(self, reducer, o):

        results = reducer(o)
        n = len(results)

        name = c_as_unicode(results[0])

        if name.endswith('*'):
            is_collection = 1
            name = c_unicode_substr(name, 0, c_unicode_length(name)-1)
        else:
            is_collection = 0

        self.write(_dump_name(name))
        self.size += len(name)

        if is_collection:
            self.write('*')

        if not is_collection and (n < 1 or n > 3):
            raise ValueError('Reducer returns invalid number of items: %s' % n)

        if n == 1:
            self.write('{}')
            return 0

        self.write('{')

        if is_collection:
            self.dump_collection(name, results[1])
        else:
            self.dump_content(results[1:])

        self.write('}')
    #
    def pretty_dump_content(self, items, offset):
        offset1 = offset + '  '
        use_offset = 1
        n = len(items)

        for item in items:

            if item is None:
                continue

            tp = type(item)
            if tp is dict:
                if self.nsize and len(item) <= self.nsize and all(is_simple_type(self, x) for x in item.values()):
                    self.write("\n")
                    self.write(offset1)
                    self._dump_attr_sequence(item)
                else:
                    self._pretty_dump_attr_sequence(item, offset1, use_offset)
            elif tp is list:
                if self.nsize and len(item) <= self.nsize and all(is_simple_type(self, x) for x in item):
                    self.write("\n")
                    self.write(offset1)
                    self._dump_list_sequence(item)
                else:
                    self._pretty_dump_list_sequence(item, offset1, use_offset)
            elif tp is tuple:
                if self.nsize and len(item) <= self.nsize and all(is_simple_type(self, x) for x in item):
                    self.write("\n")
                    self.write(offset1)
                    self._dump_tuple_sequence(item)
                else:
                    self._pretty_dump_tuple_sequence(item, offset1, use_offset)
            else:
                for v in item:
                    self.write('\n')
                    self._pretty_dump(v, offset1, use_offset)
    #
    def pretty_dump_collection(self, name, collection, offset):
        new_offset = offset + '  '
        N = len(collection)

        for i, o in enumerate(collection):
            self.write('\n')
            self.write(new_offset)
            if self.crossref:
                v = self._dump_label(o)
                if v == 1:
                    return 0

            if self.pretty == 1:
                self.write('{')
            elif self.pretty == 2:
                self.write(':')

            otype = type(o)
            reducer = self.c_type_reducers.get(otype, None)
            if reducer is None:
                raise TypeError('There is no reducer for this type: ' + repr(otype))
            else:
                items = reducer(o)
                n = len(items)

                if name != items[0]:
                    raise ValueError("Invalid name for collection %s-th item" % i)

                if n < 1 or n > 3:
                    raise ValueError('Reducer returns invalid number of items: %s' % n)
                elif n > 1:
                    self.pretty_dump_content(items[1:], new_offset)

            if self.pretty == 1:
                self.write('}')

    #
    def _pretty_dump_with_reducer(self, reducer, o, offset):

        results = reducer(o)
        n = len(results)

        name = c_as_unicode(results[0])

        if name.endswith('*'):
            is_collection = 1
            name = c_unicode_substr(name, 0, c_unicode_length(name)-1)
        else:
            is_collection = 0

        self.write(_dump_name(name))

        if is_collection:
            self.write('*')

        if not is_collection and (n < 1 or n > 3):
            raise ValueError('Reducer returns invalid number of items: %s' % n)

        if n == 1:
            if self.pretty == 2:
                self.write(':\n')
                self.write(offset)
                self.write('  ...')
            else:
                self.write('{}')
            return 0

        if self.pretty == 1:
            self.write(' {')
        elif self.pretty == 2:
            self.write(':')

        #if self.crossref:
        #    self._pretty_dump_crossref(o)

        if is_collection:
            self.pretty_dump_collection(name, results[1], offset)
        else:
            self.pretty_dump_content(results[1:], offset)

        if self.pretty == 1:
            self.write('}')
        #elif self.pretty == 2:
        #    self.write('\n')
        #    self.write(offset)
    #
    def dump(self, seq):
        '''
        Main dumping method.

        :param seq:

            Sequence of values to dump

        :param pretty:

            Flag indicates whether to use pretty dumping mode. Default is `False` (i.e. no pretty dumping)

        '''

        if self.crossref:
            self.crossref_dict = {}
            self.collect(seq)
            self.apply_crossref()

        iterseq = iter(seq)
        v = next(iterseq)

        if self.pretty:
            self._pretty_dump(v, '', 1)
        else:
            self._dump(v)

        if self.pretty:
            for v in iterseq:
                self.write('\n')
                self._pretty_dump(v, '', 1)
        else:
            for v in iterseq:
                self.write(' ')
                #self.size = 0
                self._dump(v)
    #
    def apply_crossref(self):
        crossref_set = set()
        crossref_set2 = set()
        for o_ref, count in self.crossref_dict.items():
            if count.val > 1:
                crossref_set.add(o_ref)

        crossref_dict = {}
        i = 0
        for o_ref in crossref_set:
            i += 1
            crossref_dict[o_ref] = unicode(i)

        self.crossref_set = crossref_set
        self.crossref_set2 = crossref_set2
        self.crossref_dict = crossref_dict
        crossref_dict = None
        crossref_set = None
        crossref_set2 = None
    #
    def _collect(self, o):

        if type(o) in simple_types:
            return 0

        ref_o = id(o)
        count = self.crossref_dict.get(ref_o, None)
        if count is None:
            count = PyInt(1)
            self.crossref_dict[ref_o] = count
        else:
            count.val += 1
            self.crossref_dict[ref_o] = count
            return 0

        otype = type(o)
        if otype is list:
            self._collect_list(o)
        elif otype is dict:
            self._collect_dict(o)
        elif otype is tuple:
            self._collect_tuple(o)
        elif otype is set:
            self._collect_set(o)
        else:
            reducer = self.c_type_reducers.get(otype, None)
            if reducer is None:
                raise TypeError('There is no reducer for this type: ' + repr(otype))
            else:
                self._collect_with_reducer(reducer, o)
    #
    def _collect_list(self, lst):
        for v in lst:
            self._collect(v)
    #
    def _collect_tuple(self, lst):
        for v in lst:
            self._collect(v)
    #
    def _collect_set(self, lst):
        for v in lst:
            self._collect(v)
    #
    def _collect_dict(self, d):
        for v in d.values():
            self._collect(v)
    #
    def _collect_with_reducer(self, reducer, o):

        results = reducer(o)
        n = len(results)

        if n == 1:
            return 0

        for i in range(1, n):
            results_i = results[i]
            tp = type(results_i)
            if tp is list:
                self._collect_list(results_i)
            elif tp is dict:
                self._collect_dict(results_i)
            elif tp is tuple:
                self._collect_tuple(results_i)
            elif tp is set:
                self._collect_set(results_i)
    #
    def collect(self, values):
        for v in values:
            self._collect(v)


# def dump_atomic(o):
#     otype = type(o)
#     dumper  = c_simple_dumpers.get(otype, None)
#     if dumper is None:
#         return str(o)
#     else:
#         return dumper(o)
