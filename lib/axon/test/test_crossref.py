# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

pretty = False

class CrossrefTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_crossref_1(self):
        v1, v2 = loads('&123 [ 17] a{ *123 "abc" }')
        self.assertTrue(v1 is v2.sequence[0])
    #
    def test_crossref_2(self):
        v1, v2 = loads('&_123_ a{ a:1 } b{ *_123_ "abc" }')
        self.assertTrue(v1 is v2.sequence[0])
        text = dumps([v1,v2], crossref=1)
        self.assertEqual(text, '&1 a{a:1}\nb{*1 "abc"}')
    #
    def test_crossref_3(self):
        v1, v2 = loads('&123 a{ a:1 100 200} b{ *123 "abc" }')
        self.assertTrue(v1 is v2.sequence[0])
        text = dumps([v1,v2], crossref=1)
        self.assertEqual(text, '&1 a{a:1 100 200}\nb{*1 "abc"}')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CrossrefTestCase))
    return suite
