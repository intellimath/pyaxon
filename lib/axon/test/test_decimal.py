# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps
try:
    from cdecimal import Decimal as decimal
except:
    from decimal import Decimal as decimal

class DecimalTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_decimal1(self):
        v = loads('0d')[0]
        self.assertAlmostEqual(v, decimal('0.'))
    def test_decimal2(self):
        v = loads('0.D')[0]
        self.assertAlmostEqual(v, decimal('0.'))
    def test_decimal3(self):
        v = loads('123d')[0]
        self.assertAlmostEqual(v, decimal('123'))
    def test_decimal4(self):
        v = loads('3.141528D')[0]
        self.assertAlmostEqual(v, decimal('3.141528'))
    def test_decimal5(self):
        v = loads('-1.2345e5d')[0]
        self.assertAlmostEqual(v, decimal('-1.2345e5'))
    def test_decimal6(self):
        v = loads('-1.2345e+5d')[0]
        self.assertAlmostEqual(v, decimal('-1.2345e5'))
    def test_decimal7(self):
        v = loads('-1.2345e-5D')[0]
        self.assertAlmostEqual(v, decimal('-1.2345e-5'))
    def test_decimal8(self):
        v = loads('-1.2345e27D')[0]
        self.assertAlmostEqual(v, decimal('-1.2345e27'))
    def test_decimal9(self):
        v = loads('-1.2345e-27d')[0]
        self.assertAlmostEqual(v, decimal('-1.2345e-27'))
    def test_decimal10(self):
        v = loads('1.2345e+27D')[0]
        self.assertAlmostEqual(v, decimal('1.2345e+27'))
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DecimalTestCase))
    return suite
