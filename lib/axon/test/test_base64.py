# coding: utf-8

from __future__ import unicode_literals, print_function
import unittest
from axon import loads, dumps
from axon.types import str_type, unicode_type

import sys

try:
    _chr = unichr
except NameError:
    _chr = chr

class Base64TestCase(unittest.TestCase):

    def setUp(self):
        pass
    if sys.version_info.major == 3:
        def test_1(self):
            from random import randint
            for i in range(10):
                btext = bytes([randint(1,255) for i in range(256)])
                text1= dumps([btext])
                #print('***', btext, '***')
                #print('***', text1, '***')
                btext1 = loads(text1)[0]
                self.assertEqual(btext, btext1)
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Base64TestCase))
    return suite

