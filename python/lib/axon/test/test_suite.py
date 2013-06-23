# coding: utf-8

from __future__ import unicode_literals
import unittest

import test_int
import test_float
import test_decimal
import test_string
import test_constant
import test_datetime
import test_anonymous
import test_element
import test_mapping
import test_sequence
import test_construct
import test_safe_loads
import test_unsafe_loads
import test_crossref
import test_base64
import test_errors
import test_vs_json
import test_vs_yaml

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(test_int.IntTestCase))
    suite.addTest(unittest.makeSuite(test_float.FloatTestCase))
    suite.addTest(unittest.makeSuite(test_decimal.DecimalTestCase))
    suite.addTest(unittest.makeSuite(test_string.StringTestCase))
    suite.addTest(unittest.makeSuite(test_constant.ConstantTestCase))
    suite.addTest(unittest.makeSuite(test_datetime.DateTimeTestCase))
    suite.addTest(unittest.makeSuite(test_anonymous.AnonymousTestCase))
    suite.addTest(unittest.makeSuite(test_element.ElementTestCase))
    suite.addTest(unittest.makeSuite(test_mapping.MappingTestCase))
    suite.addTest(unittest.makeSuite(test_sequence.SequenceTestCase))
    suite.addTest(unittest.makeSuite(test_construct.ConstructTestCase))
    suite.addTest(unittest.makeSuite(test_safe_loads.SafeLoadsTestCase))
    suite.addTest(unittest.makeSuite(test_unsafe_loads.UnsafeLoadsTestCase))
    suite.addTest(unittest.makeSuite(test_crossref.CrossrefTestCase))
    suite.addTest(unittest.makeSuite(test_base64.Base64TestCase))
    suite.addTest(unittest.makeSuite(test_errors.LoaderErrorTestCase))
    suite.addTest(unittest.makeSuite(test_vs_json.SimpleONvsJSONTestCase))
    suite.addTest(unittest.makeSuite(test_vs_json.SimpleONvsYAMLTestCase))

    return suite

