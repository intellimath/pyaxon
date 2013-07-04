# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps

class FloatTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_float1(self):
        v = loads('0.')[0]
        self.assertAlmostEqual(v, 0.)
    def test_float2(self):
        v = loads('3.141528')[0]
        self.assertAlmostEqual(v, 3.141528)
    def test_float3(self):
        v = loads('-1.2345e5')[0]
        self.assertAlmostEqual(v, -1.2345e5)
    def test_float4(self):
        v = loads('-1.2345e+5')[0]
        self.assertAlmostEqual(v, -1.2345e5)
    def test_float5(self):
        v = loads('-1.2345e-5')[0]
        self.assertAlmostEqual(v, -1.2345e-5)
    def test_float6(self):
        v = loads('-1.2345e27')[0]
        self.assertAlmostEqual(v, -1.2345e27)
    def test_float7(self):
        v = loads('-1.2345e-27')[0]
        self.assertAlmostEqual(v, -1.2345e-27)
    def test_zero(self):
        v = loads('-0.')[0]
        s = dumps([v])
        self.assertEqual(s, '-0.0')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FloatTestCase))
    return suite
