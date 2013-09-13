# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps
from axon.errors import LoaderError

class LoaderErrorTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_unexpected_end_1(self):
        text = 'a{'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_11(self):
        text = '{'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_12(self):
        text = '['
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_2(self):
        text = '"abc'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_3(self):
        text = '''"abc
        qwertyuiop
        '''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_4(self):
        text = 'a{name:'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_41(self):
        text = '{name:'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_5(self):
        text = 'a{name:}'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_51(self):
        text = '{name:}'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_52(self):
        text = '{name:"anne" 17}'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_6(self):
        text = 'a{name:1 age:'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_61(self):
        text = '{name:1 age:'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_7(self):
        text = '[1 2 '
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_71(self):
        text = '[1 2 a:'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_unexpected_end_72(self):
        text = '[1 2 a:7'
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_1(self):
        text = \
'''
aaa:
    a:1
      b: 2
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_2(self):
        text = \
'''
aaa:
    100
  200
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_3(self):
        text = \
'''
aaa:
    a:1
  b: 2
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_4(self):
        text = \
'''
aaa:
    100
      200
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

#
#
#

    def test_invalid_indent_11(self):
        text = \
'''
aaa:
    bbb:
        a:1
          b: 2
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_12(self):
        text = \
'''
aaa:
    bbb:
        100
      200
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_13(self):
        text = \
'''
aaa:
    bbb:
        a:1
      b: 2
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass

    def test_invalid_indent_14(self):
        text = \
'''
aaa:
    bbb:
        100
          200
'''
        try:
            vs = loads(text)
        except LoaderError:
            pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LoaderErrorTestCase))
    return suite
