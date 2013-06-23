# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps

class IntTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_int1(self):
        v = loads('0')[0]
        self.assertEqual(v, 0)
        s = dumps([v])
        self.assertEqual(s, '0')
    def test_int1a(self):
        v = loads('-0')[0]
        self.assertEqual(v, 0)
        s = dumps([v])
        self.assertEqual(s, '0')
    def test_int2(self):
        v = loads('-1')[0]
        self.assertEqual(v, -1)
        s = dumps([v])
        self.assertEqual(s, '-1')
    def test_int3(self):
        v = loads('1')[0]
        self.assertEqual(v, 1)
        s = dumps([v])
        self.assertEqual(s, '1')
    def test_int4(self):
        v = loads('17171717171717171717171717')[0]
        self.assertEqual(v, 17171717171717171717171717)
        s = dumps([v])
        self.assertEqual(s, '17171717171717171717171717')
    def test_int5(self):
        v = loads('17')[0]
        self.assertEqual(v, 17)
        s = dumps([v])
        self.assertEqual(s, '17')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntTestCase))
    return suite
