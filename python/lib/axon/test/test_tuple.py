# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

pretty = False

class TupleTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty_tuple1(self):
        v = loads('()')[0]
        self.assertEqual(type(v), tuple)
        self.assertEqual(v, ())
        s = dumps([v])
        self.assertEqual(s, '()')
    #
    def test_empty_tuple2(self):
        v = loads('()')[0]
        self.assertEqual(type(v), tuple)
        self.assertEqual(v, ())
        s = dumps([v], pretty=True)
        self.assertEqual(s, '()')
    #
    def test_tuple1(self):
        v = loads('(1 2)')[0]
        self.assertEqual(type(v), tuple)
        self.assertEqual(v, (1,2))
    #
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TupleTestCase))
    return suite
