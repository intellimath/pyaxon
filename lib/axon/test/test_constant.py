# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps

class ConstantTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_nan(self):
        v = loads('NaN')[0]
        s = dumps([v])
        self.assertEqual(s, '?')
    #
    def test_nan2(self):
        v = loads('?')[0]
        s = dumps([v])
        self.assertEqual(s, '?')
    #
    def test_inf(self):
        v = loads('Infinity')[0]
        s = dumps([v])
        self.assertEqual(s, '∞')
    #
    def test_inf1(self):
        v = loads('∞')[0]
        s = dumps([v])
        self.assertEqual(s, '∞')
    #
    def test_ninf(self):
        v = loads('-Infinity')[0]
        s = dumps([v])
        self.assertEqual(s, '-∞')
    #
    def test_ninf1(self):
        v = loads('-∞')[0]
        s = dumps([v])
        self.assertEqual(s, '-∞')
    #
    def test_decimal_nan(self):
        v = loads('NaN$')[0]
        s = dumps([v])
        self.assertEqual(s, '?D')
    #
    def test_decimal_nan2(self):
        v = loads('?D')[0]
        s = dumps([v])
        self.assertEqual(s, '?D')
    #
    def test_decimal_inf(self):
        v = loads('Infinity$')[0]
        s = dumps([v])
        self.assertEqual(s, '∞D')
    #
    def test_decimal_inf1(self):
        v = loads('∞D')[0]
        s = dumps([v])
        self.assertEqual(s, '∞D')
    #
    def test_decimal_ninf(self):
        v = loads('-Infinity$')[0]
        s = dumps([v])
        self.assertEqual(s, '-∞D')
    #
    def test_decimal_ninf1(self):
        v = loads('-∞D')[0]
        s = dumps([v])
        self.assertEqual(s, '-∞D')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConstantTestCase))
    return suite
