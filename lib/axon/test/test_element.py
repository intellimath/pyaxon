# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

class ElementTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_empty_element(self):
        v = element('aaa', {}, [])
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(v.mapping, {})
        self.assertEqual(v.sequence, [])
    #
    def test_element_init(self):
        l = {'a':1, 'b':2}
        v = element('aaa', {'a':1, 'b':2}, [1,2,3])
        self.assertEqual(v.mapping, {'a':1, 'b':2})
        self.assertEqual(v.sequence, [1,2,3])
    #
    def test_element1(self):
        v = loads('aaa{a:1 b:2 c:3 4 5 6}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Element)
        self.assertEqual(v.sequence, [4, 5, 6])
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, "aaa{a:1 b:2 c:3 4 5 6}")
    #
    def test_element1_1(self):
        v = loads('''
aaa:
   a:1
   b:2
   c:3
   4 5 6
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Element)
        self.assertEqual(v.sequence, [4, 5, 6])
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, \
            'aaa{' + \
            ' '.join("%s:%s" % (k,x) for k,x in sorted(v.mapping.items())) + ' ' + \
            ' '.join("%s" % x for x in v.sequence) + \
            '}')
    #
    def test_element2(self):
        v = loads('aaa {a:1 b:2 c:3 4 5 6}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Element)
        self.assertEqual(v.sequence, [4, 5, 6])
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v], pretty=1)
        self.assertEqual(s, \
            'aaa:\n  ' + \
            '\n  '.join(\
                      "%s: %s" % (k,x) \
                      for k,x in sorted(v.mapping.items())) + \
            '\n  ' + \
            '\n  '.join("%s" % x for x in v.sequence)
            )
    #
    def test_element_ident1(self):
        v = loads('''
aaa:
\ta:1
        b: 2
        c : 3
\t1
        2\t
\t3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Element)
        self.assertEqual(v.sequence, [1,2,3])
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, 'aaa{a:1 b:2 c:3 1 2 3}')
    #
    def test_element_ident2(self):
        v = loads('''
aaa:
\t\ta:1
        \tb: 2
        \tc : 3
                1\t
\t        2
        \t3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Element)
        self.assertEqual(v.sequence, [1,2,3])
        self.assertEqual(v.mapping, {'a': 1, 'b': 2, 'c': 3})
        s = dumps([v])
        self.assertEqual(s, 'aaa{a:1 b:2 c:3 1 2 3}')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ElementTestCase))
    return suite
