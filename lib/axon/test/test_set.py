# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

pretty = False

class SetTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty_set1(self):
        v = loads('∅')[0]
        self.assertEqual(type(v), set)
        self.assertEqual(v, set())
        s = dumps([v])
        self.assertEqual(s, '∅')
    #
    def test_empty_set2(self):
        v = loads('∅')[0]
        self.assertEqual(type(v), set)
        self.assertEqual(v, set())
        s = dumps([v], pretty=True)
        self.assertEqual(s, '∅')
    #
    def test_set1(self):
        v = loads('{1 2}')[0]
        self.assertEqual(type(v), set)
        self.assertEqual(list(sorted(v)), [1,2])
    #

def suite():
    suite = unittest.SetSuite()
    suite.addTest(unittest.makeSuite(SetTestCase))
    return suite
