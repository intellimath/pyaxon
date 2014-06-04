# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

class SequenceTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_empty_sequence(self):
        v = sequence('aaa', [])
        self.assertEqual(v.name, 'aaa')
        self.assertFalse(v.sequence)
        self.assertEqual(v.sequence, [])
        self.assertFalse(v.mapping)
        self.assertEqual(v.mapping, None)
    #
    def test_sequence_init2(self):
        l = [1,2,3]
        v = sequence('aaa', l)
        self.assertEqual(v.sequence, l)
    #
    def test_sequence1(self):
        v = loads('aaa{1 2 3}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        self.assertEqual(v.sequence, [1, 2, 3])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3}')
    #
    def test_sequence1_1(self):
        v = loads('''
aaa:
  1
  2
  3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        self.assertEqual(v.sequence, [1, 2, 3])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3}')
    #
    def test_sequence1_2(self):
        v = loads('''
aaa:
    1 2
    3 4
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        self.assertEqual(v.sequence, [1, 2, 3, 4])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3 4}')
    #
    def test_sequence1_3(self):
        v = loads('''
aaa:
  1 2
  bbb {1 2 3}
  3 4
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        #self.assertEqual(v.sequence, [1, 2, 3, 4])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 bbb{1 2 3} 3 4}')
    #
    def test_sequence1_4(self):
        v = loads('''
aaa:
  1 2
  bbb:
    1 2
    3
  3 4
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        #self.assertEqual(v.sequence, [1, 2, 3, 4])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 bbb{1 2 3} 3 4}')
    #
    def test_sequence2(self):
        v = loads('aaa{1 2 3}')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        self.assertEqual(v.sequence, [1, 2, 3])
        self.assertEqual(v.mapping, None)
        s = dumps([v], pretty=1)
        self.assertEqual(s, \
'''aaa:
  1
  2
  3''')
    #
    def test_sequence_ident1(self):
        v = loads('''
aaa:
\t1
        2\t
\t3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        self.assertEqual(v.sequence, [1,2,3])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3}')
    #
    def test_sequence_ident2(self):
        v = loads('''
aaa:
                1\t
\t        2
        \t3
''')[0]
        self.assertEqual(v.name, 'aaa')
        self.assertEqual(type(v), Sequence)
        self.assertEqual(v.sequence, [1,2,3])
        self.assertEqual(v.mapping, None)
        s = dumps([v])
        self.assertEqual(s, 'aaa{1 2 3}')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SequenceTestCase))
    return suite
