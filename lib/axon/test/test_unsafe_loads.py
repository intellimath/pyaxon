# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

class C(object):
    pass

class D(object):
    pass

class E(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def mapping_instance_maker(cls):
    def make_instance(attrs):
        inst = cls.__new__(cls)
        for name, value in attrs.items():
            setattr(inst, name, value)
        return inst
    return make_instance

def mapping_reducer_maker(cls):
    def type_reducer(o):
        attrs = {}
        for name in o.__dict__:
            if name.startswith('_'):
                continue
            attrs[as_name(name)] = getattr(o, name)

        return as_name(cls.__name__), attrs
    return type_reducer


factory('C', mapping_instance_maker(C))
factory('D', mapping_instance_maker(D))
factory('E', mapping_instance_maker(E))

reduce(C, mapping_reducer_maker(C))
reduce(D, mapping_reducer_maker(D))
reduce(E, mapping_reducer_maker(E))

class UnsafeLoadsTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_1(self):
        v = C()
        v.a = 1
        v.b = 2
        v.c = 3
        text = dumps([v])
        #display(text)
        v1 = loads(text, mode='strict')[0]
        self.assertEqual(v.a, v1.a)
        self.assertEqual(v.b, v1.b)
        self.assertEqual(v.c, v1.c)
    #
    def test_2(self):
        v = C()
        v.a = 1
        v.b = 2
        v.c = 3
        w = D()
        w.a = 'a'
        w.b = [1,2]
        w.c = 2
        text = dumps([v, w])
        #display(text)
        v1, w1 = loads(text, mode='strict')
        self.assertEqual(v.a, v1.a)
        self.assertEqual(v.b, v1.b)
        self.assertEqual(v.c, v1.c)
        self.assertEqual(w.a, w1.a)
        self.assertEqual(w.b, w1.b)
        self.assertEqual(w.c, w1.c)
    #
    def test_3(self):
        v = E(1, 2, 3)
        text = dumps([v])
        #display(text)
        v1 = loads(text, mode='strict')[0]
        self.assertEqual(v.a, v1.a)
        self.assertEqual(v.b, v1.b)
        self.assertEqual(v.c, v1.c)
    #
    def test_4(self):
        from random import randint
        v = C()
        v.x = 1
        v.y = lst = []
        for i in range(7):
            w = D()
            w.z = randint(1,1000)
            lst.append(w)
        text = dumps([v])
        #print()
        #display(text)
        v1 = loads(text, mode='strict')[0]
        self.assertEqual(v1.x, 1)
        self.assertEqual(len(v1.y), 7)
        self.assertEqual(all([type(z) is D for z in v1.y]), True)
        self.assertEqual(all([z.z==z1.z for z,z1 in zip(v1.y, lst)]), True)
    #
    def test_5(self):
        from random import randint
        vs = []
        v = C()
        v.x = 1
        v.y = lst = []
        for i in range(7):
            w = D()
            w.z = randint(1,1000)
            lst.append(w)
            vs.append(w)
        vs.append(v)
        text = dumps(vs, crossref=True, pretty=1)
        #print()
        #print(text)
        #vs1 = loads(text, builder='strict')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnsafeLoadsTestCase))
    return suite
