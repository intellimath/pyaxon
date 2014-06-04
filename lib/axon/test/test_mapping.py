# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

class MappingTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_empty_mapping(self):
        v = mapping('aaa', {})
        self.assertEqual(v.name, 'aaa')
        self.assertFalse(v.mapping)
        self.assertEqual(v.mapping, {})
        self.assertFalse(v.sequence)
        self.assertEqual(v.sequence, None)
    #
    def test_mapping_init(self):
        l = {'a':1, 'b':2}
        v = mapping('aaa', l)
        self.assertEqual(v.mapping, {'a':1, 'b':2})
    #
    def test_mapping1(self):
        v = loads('aaa{a:1 b: 2 c : 3}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Mapping)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, '''aaa{a:1 b:2 c:3}''')
    #
    def test_mapping1_1(self):
        v = loads('''
aaa:
   a:1
   b: 2
   c : 3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Mapping)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, '''aaa{a:1 b:2 c:3}''')
    #
    def test_mapping2(self):
        v = loads('aaa {a: 1 b:2 c:3}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Mapping)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  a: 1
  b: 2
  c: 3''')
    #
    def test_mapping3(self):
        v = loads('''
aaa:
  a: 1
  b: 2
  c: c:
    e: 1
    f: f:
      r: 2
      s: 3
  d: 4
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Mapping)
        self.assertEqual(v.sequence, None)
        s = dumps([v])
        self.assertEqual(s, '''aaa{a:1 b:2 c:c{e:1 f:f{r:2 s:3}} d:4}''')
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  a: 1
  b: 2
  c: c:
    e: 1
    f: f:
      r: 2
      s: 3
  d: 4''')
    #
    def test_mapping4(self):
        v = loads('''
aaa:
  a: 1
  b: 2
  c:
    e: 1
    f:
      r: 2
      s: 3
  d:
    4
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Element)
        s = dumps([v])
        self.assertEqual(s, '''aaa{a:1 b:2 c{e:1 f{r:2 s:3}} d{4}}''')
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  a: 1
  b: 2
  c:
    e: 1
    f:
      r: 2
      s: 3
  d:
    4''')
    #
    def test_mapping_dotted_names(self):
        l = {'en.a':1, 'ru.a':2}
        v = mapping('example.aaa', l)
        self.assertEqual(v.mapping, {'en.a':1, 'ru.a':2})
        self.assertEqual(v.name, 'example.aaa')
    #
    def test_mapping_ident1(self):
        v = loads('''
aaa:
\ta:1
        b: 2
        c : 3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Mapping)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, 'aaa{a:1 b:2 c:3}')
    #
    def test_mapping_ident2(self):
        v = loads('''
aaa:
\t\ta:1
        \tb: 2
        \tc : 3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Mapping)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, 'aaa{a:1 b:2 c:3}')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MappingTestCase))
    return suite
