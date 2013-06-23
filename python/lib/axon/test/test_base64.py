# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

try:
    _builtins_unicode = builtins.unicode
    _builtins_str = builtins.str
    _chr = unichr
except AttributeError:
    _builtins_unicode = builtins.str
    _builtins_str = builtins.str
    _chr = chr

class Base64TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_1(self):
        from random import randint
        for i in range(10):
            text = ''.join([_chr(randint(1,255)) for i in range(256)])
            if type(text) is _builtins_unicode:
                btext = text.encode('latin1')
            else:
                btext = bytes(text)
            text1= dumps([btext])
            print('***', btext, '***')
            print('***', text1, '***')
            btext1 = loads(text1)[0]
            self.assertEqual(btext, btext1)
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Base64TestCase))
    return suite

