# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import *

pretty = False

class ListTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_empty_list1(self):
        v = loads('[]')[0]
        self.assertEqual(type(v), list)
        self.assertEqual(v, [])
        s = dumps([v])
        self.assertEqual(s, '[]')
    #
    def test_empty_list2(self):
        v = loads('[]')[0]
        self.assertEqual(type(v), list)
        self.assertEqual(v, [])
        s = dumps([v], pretty=True)
        self.assertEqual(s, '[]')
    #
    def test_list1(self):
        v = loads('[1 2]')[0]
        self.assertEqual(type(v), list)
        self.assertEqual(v, [1,2])
    #
    def test_list2(self):
        v = loads('[[1 2] [2 3]]')[0]
        self.assertEqual(type(v), list)
        self.assertEqual(v, [[1,2], [2,3]])
    #
    def test_list3(self):
        v = loads('''
            [
                [1 2]
                [2 3]
            ]'''
        )[0]
        self.assertEqual(type(v), list)
        self.assertEqual(v, [[1,2], [2,3]])
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ListTestCase))
    return suite
