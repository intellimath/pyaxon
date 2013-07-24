# coding: utf-8

from __future__ import unicode_literals
import unittest
from axon import loads, dumps
from datetime import date, time, datetime, tzinfo

class DateTimeTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_date1(self):
        v = loads('2010-12-01')[0]
        self.assertEqual(type(v), date)
        s = dumps([v])
        self.assertEqual(s, '2010-12-01')
    #
    def test_date2(self):
        v = loads('1900-01-01')[0]
        self.assertEqual(type(v), date)
        s = dumps([v])
        self.assertEqual(s, '1900-01-01')
    #
    def test_date3(self):
        v = loads('12-01-01')[0]
        self.assertEqual(type(v), date)
        s = dumps([v])
        self.assertEqual(s, '12-01-01')
    #
    def test_date4(self):
        v = loads('0-00-00')[0]
        self.assertEqual(type(v), date)
        s = dumps([v])
        self.assertEqual(s, '0-00-00')
    #
    def test_time1(self):
        v = loads('00:00')[0]
        self.assertEqual(type(v), time)
        s = dumps([v])
        self.assertEqual(s, '00:00')
    #
    def test_time2(self):
        v = loads('23:59:59')[0]
        self.assertEqual(type(v), time)
        s = dumps([v])
        self.assertEqual(s, '23:59:59')
    #
    def test_time3(self):
        v = loads('23:59:59.000123')[0]
        self.assertEqual(type(v), time)
        s = dumps([v])
        self.assertEqual(s, '23:59:59.000123')
    #
    def test_time4(self):
        v = loads('23:59:59+00:00')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59+00')
        self.assertEqual(v.utcoffset().seconds, 0)
    #
    def test_time5(self):
        v = loads('23:59:59+01:00')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59+01')
        self.assertEqual(v.utcoffset().seconds/60, 60)
    #
    def test_time6(self):
        v = loads('23:59:59-01:00')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59-01')
        self.assertEqual(v.utcoffset().seconds/60, 23*60)
    #
    def test_time7(self):
        v = loads('23:59:59+12:00')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59+12')
        self.assertEqual(v.utcoffset().seconds/60, 12*60)
    #
    def test_time8(self):
        v = loads('23:59:59+23:00')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59+23')
        self.assertEqual(v.utcoffset().seconds/60, 23*60)
    #
    def test_time9(self):
        v = loads('23:59:59-23:00')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59-23')
        self.assertEqual(v.utcoffset().seconds/60, 60)
    #
    def test_time10(self):
        v = loads('23:59:59+3:15')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59+03:15')
        self.assertEqual(v.utcoffset().seconds/60, 3*60+15)
    #
    def test_time11(self):
        v = loads('23:59:59-3:15')[0]
        self.assertEqual(type(v), time)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '23:59:59-03:15')
        self.assertEqual(v.utcoffset().seconds/60, 1440-3*60-15)
    #
    def test_datetime1(self):
        v = loads('2010-01-01T00:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertEqual(v.tzinfo, None)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T00:00')
    #
    def test_datetime2(self):
        v = loads('1-01-01T23:59:59')[0]
        self.assertEqual(type(v), datetime)
        self.assertEqual(v.tzinfo, None)
        s = dumps([v])
        self.assertEqual(s, '1-01-01T23:59:59')
    #
    def test_datetime3(self):
        v = loads('2010-01-01T23:59:59.000123')[0]
        self.assertEqual(type(v), datetime)
        self.assertEqual(v.tzinfo, None)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59.000123')
    #
    def test_datetime4(self):
        v = loads('2010-01-01T23:59:59+00:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59+00')
        self.assertEqual(v.utcoffset().seconds, 0)
    #
    def test_datetime5(self):
        v = loads('2010-01-01T23:59:59+01:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59+01')
        self.assertEqual(v.utcoffset().seconds/60, 60)
    #
    def test_datetime6(self):
        v = loads('2010-01-01T23:59:59-01:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59-01')
        self.assertEqual(v.utcoffset().seconds/60, 23*60)
    #
    def test_datetime7(self):
        v = loads('2010-01-01T23:59:59+12:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59+12')
        self.assertEqual(v.utcoffset().seconds/60, 12*60)
    #
    def test_datetime8(self):
        v = loads('2010-01-01T23:59:59+23:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59+23')
        self.assertEqual(v.utcoffset().seconds/60, 23*60)
    #
    def test_datetime9(self):
        v = loads('2010-01-01T23:59:59-23:00')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59-23')
        self.assertEqual(v.utcoffset().seconds/60, 60)
    #
    def test_datetime10(self):
        v = loads('2010-01-01T23:59:59+3:15')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59+03:15')
        self.assertEqual(v.utcoffset().seconds/60, 3*60+15)
    #
    def test_datetime11(self):
        v = loads('2010-01-01T23:59:59-3:15')[0]
        self.assertEqual(type(v), datetime)
        self.assertIsInstance(v.tzinfo, tzinfo)
        s = dumps([v])
        self.assertEqual(s, '2010-01-01T23:59:59-03:15')
        self.assertEqual(v.utcoffset().seconds/60, 1440-3*60-15)
    #

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DateTimeTestCase))
    return suite
