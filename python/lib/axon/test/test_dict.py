# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

class DictTestCase(unittest.TestCase):

    def setUp(self):
        pass
    #
    def test_empty_dict1(self):
        v = loads('{}')[0]
        self.assertEqual(type(v), dict)
        self.assertEqual(v, {})
        s = dumps([v])
        self.assertEqual(s, '{}')
    #
    def test_empty_dict2(self):
        v = loads('{}\n')[0]
        self.assertEqual(type(v), dict)
        self.assertEqual(v, {})
        s = dumps([v], pretty=True)
        self.assertEqual(s, '{}')
    #
    def test_dict1(self):
        v = loads('{a:1 b:2}')[0]
        self.assertEqual(type(v), dict)
        self.assertEqual(list(sorted(v.items())), [('a',1),('b',2)])
    #
    def test_dict1_1(self):
        v = loads('{a:1, b:2}', json=True)[0]
        self.assertEqual(type(v), dict)
        self.assertEqual(list(sorted(v.items())), [('a',1),('b',2)])
    #
    def test_dict2(self):
        v = loads('{a:[1,2] b:{c:3}}', json=True)[0]
        self.assertEqual(type(v), dict)
        self.assertEqual(list(sorted(v.items())), [('a',[1,2]),('b',{'c':3})])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DictTestCase))
    return suite
