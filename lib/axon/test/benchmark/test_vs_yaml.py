# -*- coding: utf-8 -*-
from __future__ import print_function

import yaml
import random
import time
import unittest
import xon

def random_string(n):
    text = ''.join([chr(ord('a')+random.randint(1,20)) for i in range(20)])
    return xon.as_unicode(text)

class SimpleONvsYAMLTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_vs_yaml_1(self):
        lst = []
        for i in range(1000):
            lst.append({
                random_string(8): random.random(),
                random_string(8): random.randint(1,99999),
                random_string(8): random_string(32),
                random_string(8): random.random(),
                random_string(8): random.randint(1,99999),
                random_string(8): random_string(32),
                random_string(8): random.random(),
                random_string(8): random.randint(1,99999),
                random_string(8): random_string(32),
            })
        yaml_text = yaml.dump(lst, Dumper=yaml.CDumper)
        t0 = time.time()
        v = yaml.load(yaml_text, Loader=yaml.CLoader)
        dt_yaml = time.time() - t0

        xon_text = xon.dumps([lst], quote=True, pretty=False)
        t0 = time.time()
        v = xon.loads(xon_text)
        dt_xon = time.time() - t0

        print('\nxon:', dt_xon, 'yaml', dt_yaml)

        self.assertTrue(dt_xon < dt_yaml)

    def test_vs_yaml_2(self):
        d = {}
        for j in range(50):
            lst = []
            for i in range(100):
                lst.append({
                    random_string(8): random.random(),
                    random_string(8): random.randint(1,99999),
                    random_string(8): random_string(32),
                    random_string(8): random.random(),
                    random_string(8): random.randint(1,99999),
                    random_string(8): random_string(32),
                })
            d[random_string(8)] = lst
        yaml_text = yaml.dump(d, Dumper=yaml.CDumper)
        t0 = time.time()
        v = yaml.load(yaml_text, Loader=yaml.CLoader)
        dt_yaml = time.time() - t0

        xon_text = xon.dumps([d], quote=True, pretty=False)
        #print(xon_text)
        t0 = time.time()
        v = xon.loads(xon_text)
        dt_xon = time.time() - t0

        print('\nxon:', dt_xon, 'yaml', dt_yaml)

        self.assertTrue(dt_xon < dt_yaml)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleONvsYAMLTestCase))
    return suite




