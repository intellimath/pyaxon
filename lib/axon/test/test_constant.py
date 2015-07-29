# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps

class ConstantTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_nan2(self):
        v = loads('?')[0]
        s = dumps([v])
        self.assertEqual(s, '?')
    #
    def test_null(self):
        v = loads('null')[0]
        s = dumps([v])
        self.assertEqual(s, 'null')
    #
    def test_true(self):
        v = loads('true')[0]
        s = dumps([v])
        self.assertEqual(s, 'true')
    #
    def test_false(self):
        v = loads('false')[0]
        s = dumps([v])
        self.assertEqual(s, 'false')
    #
    def test_inf1(self):
        v = loads('∞')[0]
        s = dumps([v])
        self.assertEqual(s, '∞')
    #
    def test_ninf1(self):
        v = loads('-∞')[0]
        s = dumps([v])
        self.assertEqual(s, '-∞')
    #
    def test_decimal_nan2(self):
        v = loads('?D')[0]
        s = dumps([v])
        self.assertEqual(s, '?D')
    #
    def test_decimal_inf1(self):
        v = loads('∞D')[0]
        s = dumps([v])
        self.assertEqual(s, '∞D')
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
