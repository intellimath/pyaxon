# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps

class StringTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_str1(self):
        v = loads('""')[0]
        self.assertEqual(v, '')
        s = dumps([v])
        self.assertEqual(s, '""')
    def test_str2(self):
        v = loads('"\n"')[0]
        self.assertEqual(v, '\n')
        s = dumps([v])
        self.assertEqual(s, '"\n"')
    def test_str3(self):
        t = '''"\
abc\
def"'''
        v = loads(t)[0]
        self.assertEqual(v, 'abcdef')
        s = dumps([v])
        self.assertEqual(s, '"abcdef"')
    def test_str4(self):
        v = loads('"abc абв"')[0]
        self.assertEqual(v, 'abc абв')
        s = dumps([v])
        self.assertEqual(s, '"abc абв"')
    def test_str5(self):
        t = '"ab\tcd\nef"'
        v = loads(t)[0]
        self.assertEqual(v, 'ab\tcd\nef')
        s = dumps([v])
        self.assertEqual(s, t)
    def test_str6(self):
        t = '''"abfdsfdfd
sdfdfdfdfsdfdwrerwrwerwe
cvbnbnfrtt"'''
        v = loads(t)[0]
        self.assertEqual(v, '''abfdsfdfd
sdfdfdfdfsdfdwrerwrwerwe
cvbnbnfrtt''')
        s = dumps([v])
        self.assertEqual(s, t)
#     def test_str(self):
#         t = '"\\u0041\\U0042"'
#         v = loads(t)[0]
#         self.assertEqual(v, "AB")
#         s = dumps([v])
#         self.assertEqual(s, '"AB"')
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StringTestCase))
    return suite
