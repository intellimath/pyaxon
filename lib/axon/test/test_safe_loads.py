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
        self.assertEqual(v.sequence, [])
        self.assertEqual(v.mapping, {})
        s = dumps([v])
        self.assertEqual(s, 'aaa{}')
    #
    def test_empty2(self):
        v = loads('aaa{}')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, [])
        self.assertEqual(v.mapping, {})
        s = dumps([v], pretty=1)
        self.assertEqual(s, 'aaa{}')
    #
    def test_empty2_special(self):
        v = loads("""'aaa bbb'{}""")[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, [])
        self.assertEqual(v.mapping, {})
        s = dumps([v], pretty=1)
        self.assertEqual(s, """'aaa bbb'{}""")
    #
    def test_empty3(self):
        v = loads('''
aaa:
   ...
''')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, [])
        self.assertEqual(v.mapping, {})
        s = dumps([v], pretty=1)
        self.assertEqual(s, 'aaa{}')
    #
    def test_empty3_special(self):
        v = loads('''
'aaa bbb':
   ...
''')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, [])
        self.assertEqual(v.mapping, {})
        s = dumps([v], pretty=1)
        self.assertEqual(s, """'aaa bbb'{}""")
    #
    def test_empty4(self):
        v = loads('''
aaa:
  ...
''')[0]
        self.assertEqual(type(v), Empty)
        self.assertEqual(v.sequence, [])
        self.assertEqual(v.mapping, {})
        s = dumps([v], pretty=2)
        self.assertEqual(s, '''\
aaa:
  ...''')
    #
    def test_empty5(self):
        v = loads('''
aaa:
  bbb:
    ...
  ccc:
    ...
''')[0]
        s = dumps([v], pretty=2)
        self.assertEqual(s, '''\
aaa:
  bbb:
    ...
  ccc:
    ...''')
    #
    def test_empty6(self):
        v = loads('''
aaa:
  a: 1
  b:2
  bbb:
    ...
  ccc:
    c:1
    ddd:
      ...
''')[0]
        s = dumps([v], pretty=2)
        self.assertEqual(s, '''\
aaa:
  a: 1
  b: 2
  bbb:
    ...
  ccc:
    c: 1
    ddd:
      ...''')
    #
    def test_special_7(self):
        text = """'aaa bbb'{xxx:'nnn#ddd'{vvv{'iii oooo'{}}} 'xxx$yyy':'ccc-ddd'{'qqq vvv':"nill"}}"""
        s = dumps(loads(text))
        self.assertEqual(s, text)
    #
    def test_special_8(self):
        text = """\
'aaa bbb' {
  xxx: 'nnn#ddd' {
    vvv {
      'iii oooo'{}}}
  'xxx$yyy': 'ccc-ddd' {
    'qqq vvv': "nill"}}"""
        s = dumps(loads(text), pretty=1)
        self.assertEqual(s, text)
    #
    def test_special_9(self):
        text = """\
'aaa bbb':
  xxx: 'nnn#ddd':
    vvv:
      'iii oooo':
        ...
  'xxx$yyy': 'ccc-ddd':
    'qqq vvv': null"""
        s = dumps(loads(text), pretty=2)
        self.assertEqual(s, text)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SafeLoadsTestCase))
    return suite
