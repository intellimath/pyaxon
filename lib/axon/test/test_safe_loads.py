# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

pretty = False

class SafeLoadsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty1(self):
        v = loads('aaa{}')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{}')
    #
    def test_empty2(self):
        v = loads('aaa{}')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, None)
        s = dumps([v], pretty=1, braces=1)
        self.assertEqual(s, 'aaa {}')
    #
    def test_empty3(self):
        v = loads('''
aaa:
    
''')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, None)
        s = dumps([v], pretty=1, braces=1)
        self.assertEqual(s, 'aaa {}')
    #
    def test_empty4(self):
        v = loads('''
aaa:
    
''')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, None)
        self.assertEqual(v.mapping, None)
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''aaa:''')
    #
    def test_empty5(self):
        v = loads('''
aaa:
  bbb:
  ccc:''')[0]
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  bbb:
  ccc:''')
    #
    def test_empty6(self):
        v = loads('''
aaa:
  a: 1
  b:2
  bbb:
    
  ccc:
    c:1
    ddd:

''')[0]
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  a: 1
  b: 2
  bbb:
  ccc:
    c: 1
    ddd:''')
    #
    def test_empty7(self):
        v = loads('''
aaa:
  a: 1
  b:2 c:  4
  bbb:
    
  ccc:
    c:1 d:  23
    ddd:

''')[0]
        s = dumps([v], pretty=1)
        self.assertEqual(s, '''\
aaa:
  a: 1
  b: 2
  c: 4
  bbb:
  ccc:
    c: 1
    d: 23
    ddd:''')
    #


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SafeLoadsTestCase))
    return suite
