# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

class ObjectTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_empty_object(self):
        v = instance('aaa', [], {})
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(v.mapping, {})
        self.assertEqual(v.sequence, ())
    #
    def test_object_init(self):
        l = {'a':1, 'b':2}
        v = instance('aaa', [1,2,3], {'a':1, 'b':2})
        self.assertEqual(v.mapping, {'a':1, 'b':2})
        self.assertEqual(v.sequence, (1,2,3))
    #
    def test_object1(self):
        v = loads('aaa {4 5 6 a:1 b:2 c:3}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Instance)
        self.assertEqual(v.sequence, (4, 5, 6))
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, '''aaa{4 5 6 a:1 b:2 c:3}''')
    #
    def test_object2(self):
        v = loads('aaa{4 5 6 a:1 b : 2 c:3}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Instance)
        self.assertEqual(v.sequence, (4, 5, 6))
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  4
  5
  6
  a: 1
  b: 2
  c: 3''')
    #
    def test_instance_ident1(self):
        v = loads('''
aaa:
\t1
        2\t
\t3
\ta:1
        b: 2
        c : 3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Instance)
        self.assertEqual(v.sequence, (1,2,3))
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3 a:1 b:2 c:3}')
    #
    def test_instance_ident2(self):
        v = loads('''
aaa:
                1\t
\t        2
        \t3
\t\ta:1
        \tb: 2
        \tc : 3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Instance)
        self.assertEqual(v.sequence, (1,2,3))
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3 a:1 b:2 c:3}')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ObjectTestCase))
    return suite
