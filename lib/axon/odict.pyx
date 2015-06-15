# coding: utf-8

#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: language_level=3

# The MIT License (MIT)
# 
# Copyright (c) <2011-2015> <Shibzukhov Zaur, szport at gmail dot com>
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

cimport cython
from cpython.object cimport Py_EQ, Py_NE

from operator import eq as _eq
import sys as _sys
import collections
    
cdef dict _repr_running = {}

cdef public class OrderedDict[object OrderedDictObject, type OrderedDictType]

cdef class _MappingView:

    #cdef OrderedDict _mapping

    def __init__(self, OrderedDict mapping):
        self._mapping = mapping

    def __len__(self):
        return len(self._mapping)
        
    def _eq__(self, other):
        for v1, v2 in zip(self, other):
            if v1 != v2:
                return False
        return True

    def __richcmp__(self, other, int op):
        if op == Py_EQ:
            return self._eq__(other)
        elif op == Py_NE:
            return not self._eq__(other)
        return NotImplemented

    def __repr__(self):
        args = [(key, val) for key, val in self._mapping.items()]
        return '{0.__class__.__name__}({1})'.format(self._mapping, args)

collections.MappingView.register(_MappingView)

cdef class _KeysView(_MappingView):

    def __contains__(self, key):
        return key in self._mapping

    def __iter__(self):
        return iter(self._mapping)
        
    def __reversed__(self):
        yield from self._mapping.__reversed__()

collections.KeysView.register(_KeysView)        

cdef class _ItemsView(_MappingView):

    def __contains__(self, item):
        cdef Link link
    
        key, value = item
        link = <Link>self._mapping.get(key, None)
        if link is None:
            return False
        else:
            return link.value == value

    def __iter__(self):
        for key in self._mapping:
            yield (key, self._mapping[key])

    def __reversed__(self):
        for key in self._mapping.__reversed__():
            yield (key, self._mapping[key])
            
collections.ItemsView.register(_ItemsView)        

cdef class _ValuesView(_MappingView):

    def __contains__(self, value):
        for key in self._mapping:
            if value == self._mapping[key]:
                return True
        return False

    def __iter__(self):
        for key in self._mapping:
            yield self._mapping[key]
            
    def __reversed__(self):
        for key in self._mapping.__reversed__():
            yield self._mapping[key]
            
collections.ValuesView.register(_ValuesView)        


################################################################################
### OrderedDict
################################################################################

cdef public class Link[object LinkObject, type LinkType]:    
    def __iter__(self):
        yield self.key
        yield self.value

cdef Link link_marker = Link()

cdef Link link_new(Link prev, Link next):
   cdef Link link = Link.__new__(Link)
   link.prev = <cython.void*>prev
   link.next = <cython.void*>next
   return link

cdef public class OrderedDict[object OrderedDictObject, type OrderedDictType]:
    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  The signature is the same as
        regular dictionaries, but keyword arguments are not recommended because
        their insertion order is arbitrary.
        '''
        cdef Link root

        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))

        if self.root is None:
            self.map = {}
            root = <Link>Link.__new__(Link)
            root.prev = root.next = <cython.void*>root
            self.root = root
        
        self.__update(args, kwds)

    def __setitem__(self, key, value):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link at the end of the linked list,
        # and the inherited dictionary is updated with the new key/value pair.
        
        cdef Link root, last, link
        
        if dict.__contains__(self.map, key):
            link = <Link>dict.__getitem__(self.map, key)
            link.value = value
        else:
            root = self.root
            last = <Link>root.prev

            link = <Link>Link.__new__(Link)

            link.prev, link.next = <cython.void*>last, <cython.void*>root
            link.key, link.value = key, value
            last.next =  root.prev = <cython.void*>link
            
            dict.__setitem__(self.map, key, link)

    def __getitem__(self, key):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link at the end of the linked list,
        # and the inherited dictionary is updated with the new key/value pair.
        cdef Link link
        
        link = <Link>dict.__getitem__(self.map, key)
        return link.value

    def __delitem__(self, key):
        'od.__delitem__(y) <==> del od[y]'
        # Deleting an existing item uses self.__map to find the link which gets
        # removed by updating the links in the predecessor and successor nodes.
        cdef Link link, link_prev, link_next
        
        link = <Link>dict.pop(self.map, key)
        link_prev = <Link>link.prev
        link_next = <Link>link.next
        link_prev.next = <cython.void*>link_next
        link_next.prev = <cython.void*>link_prev        

    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        # Traverse the linked list in order.
        cdef Link root, curr
        
        root = self.root
        curr = <Link>root.next
        while curr is not root:
            yield curr.key
            curr = <Link>curr.next
    
    def __nonzero__(self):
        return bool(self.map)

    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        # Traverse the linked list in reverse order.
        cdef Link root, curr

        root = self.root
        curr = <Link>root.prev
        while curr is not root:
            yield curr.key
            curr = <Link>curr.prev
            
    def __len__(self):
        return len(self.map)
            
    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        cdef Link root

        root = self.root
        root.prev = root.next = <cython.void*>root
        dict.clear(self.map)

    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        '''
        
        cdef Link root, link, link_prev, link_next
        
        if not self.map:
            raise KeyError('dictionary is empty')
        root = self.root
        if last:
            link = <Link>root.prev
            link_prev = <Link>link.prev
            link_prev.next = <cython.void*>root
            root.prev = <cython.void*>link_prev
        else:
            link = <Link>root.next
            link_next = <Link>link.next
            root.next = <cython.void*>link_next
            link_next.prev = <cython.void*>root
        key = link.key
        value = link.value
        dict.__delitem__(self.map, key)
        return key, value
        
    def move_to_end(self, key, last=True):
        '''Move an existing element to the end (or beginning if last==False).

        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).

        '''
        cdef Link root, link, link_prev, link_next, link_last, link_first
        
        link = <Link>dict.__getitem__(self.map, key)
        link_prev = <Link>link.prev
        link_next = <Link>link.next
        link_prev.next = <cython.void*>link_next
        link_next.prev = <cython.void*>link_prev
        root = self.root
        if last:
            link_last = <Link>root.prev
            link.prev = <cython.void*>link_last
            link.next = <cython.void*>root
            link_last.next = root.prev = <cython.void*>link
        else:
            link_first = <Link>root.next
            link.prev = <cython.void*>root
            link.next = <cython.void*>link_first
            root.next = link_first.prev = <cython.void*>link

    def __sizeof__(self):
        _sizeof = _sys.getsizeof
        n = len(self) + 1                       # number of links including root
        size = _sizeof(self.map)            # internal dictionary
        size += _sizeof(self.root) * n         # link objects
        return size
    
    def __update(self, args, kwds):
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' %
                            len(args))
        if args:
            other = args[0]
            tp = type(other) 
            if tp is list:
                for key, value in <list>other:
                    self[key] = value
            elif tp is dict:
                for key, value in (<dict>other).items():
                    self[key] = value
            elif tp is tuple:
                for key, value in <list>other:
                    self[key] = value
            elif isinstance(other, collections.Mapping):
                for key in other:
                    self[key] = other[key]
            elif hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        if kwds:
            for key, value in kwds.items():
                self[key] = value

    def update(self, *args, **kw):
        ''' D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.
            If E present and has a .keys() method, does:     for k in E: D[k] = E[k]
            If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v
            In either case, this is followed by: for k, v in F.items(): D[k] = v
        '''
        self.__update(args, kw)
    
    def get(self, key, default=None):
        'D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'
        cdef Link link
        
        link = <Link>dict.get(self.map, key, None)
        if link is None:
            return default
        else:
            return link.value

    def __contains__(self, key):
        return key in self.map

    def keys(self):
        "D.keys() -> a set-like object providing a view on D's keys"
        return _KeysView(self)

    def items(self):
        "D.items() -> a set-like object providing a view on D's items"
        return _ItemsView(self)

    def values(self):
        "D.values() -> an object providing a view on D's values"
        return _ValuesView(self)
    
    def pop(self, key, default=link_marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding
        value.  If key is not found, d is returned if given, otherwise KeyError
        is raised.

        '''
        cdef Link link
        link = <Link>dict.pop(self.map, key, link_marker)
        if link is link_marker:
            if default is link_marker:
                raise KeyError("There is no such key %r" % key)
            else:
                return default
        else:
            return link.value

    def setdefault(self, key, default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        
        cdef Link link
        link = <Link>dict.get(self.map, key, None)
        if link is None:
            self[key] = default
            return default
        else:
            return link.value

    def __repr__(self):
        'od.__repr__() <==> repr(od)'
        #call_key = id(self), _get_ident()
        call_key = id(self)
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self.map:
                return '%s()' % (self.__class__.__name__,)
            args = [(key, val) for key, val in self.items()]
            return '%s(%r)' % (self.__class__.__name__, args)
        finally:
            del _repr_running[call_key]

    def __reduce__(self):
        'Return state information for pickling'
        # items = [(k, self[k]) for k in self]
        # return odict, (items,)
        try:
            inst_dict = vars(self).copy()
            #for k in vars(OrderedDict()):
            #    inst_dict.pop(k, None)
        except:
            inst_dict = None
        return self.__class__, (), inst_dict, None, iter(self.items())
        
    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S.
        If not specified, the value defaults to None.

        '''
        self = cls()
        for key in iterable:
            self[key] = value
        return self

    def __eq(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.
        '''
        if len(self) != len(other):
            return 0
        if isinstance(other, OrderedDict):
            for item_self, item_other in zip(self.items(), other.items()):
                if item_self == item_other:
                    continue
                else:
                    return 0
        else:
            for key in self.map:
                if key in other:
                    if self[key] == other[key]:
                        continue
                    else:
                        return 0
                else:
                    return 0    
        return 1

    def __richcmp__(self, other, int op):
        if op == Py_EQ:
            return self.__eq(other)
        elif op == Py_NE:
            return not self.__eq(other)
        return NotImplemented


collections.MutableMapping.register(OrderedDict)

cdef OrderedDict c_new_odict(list args):
    cdef OrderedDict od
    cdef Link root, last, link
    
    od = OrderedDict.__new__(OrderedDict)
    od.map = {}
    root = <Link>Link.__new__(Link)
    root.prev = root.next = <cython.void*>root
    od.root = root

    if args is not None:  
        for key, value in args:
            root = od.root
            last = <Link>root.prev

            link = <Link>Link.__new__(Link)

            link.prev, link.next = <cython.void*>last, <cython.void*>root
            link.key, link.value = key, value
            last.next =  root.prev = <cython.void*>link
            
            dict.__setitem__(od.map, key, link)
    return od

def odict(args):
    return c_new_odict(c_as_list(args))            

