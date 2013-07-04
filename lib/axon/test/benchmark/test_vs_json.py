# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import xon
import random
import time
import unittest
from xon.types import unicode_type
import gc

def random_string(n):
    text = ''.join(chr(ord('a')+random.randint(1,20)) for i in range(20))
    text = xon.as_unicode(text)
    #assert type(text) is unicode_type
    return text

class SimpleONvsJSONTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_vs_json_1(self):
        lst = []
        for i in range(4000):
            lst.append([
                random_string(8), random.random(),
                random_string(8), random.randint(1,99999),
                random_string(8), random_string(32),
                random_string(8), random.random(),
                random_string(8), random.randint(1,99999),
                random_string(8), random_string(32),
                random_string(8), random.random(),
                random_string(8), random.randint(1,99999),
                random_string(8), random_string(32),
                random_string(8), random.random(),
                random_string(8), random.randint(1,99999),
                random_string(8), random_string(32),
            ])

        xon_text = xon.dumps(lst)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

    def test_vs_json_2(self):
        lst = []
        for i in range(4000):
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
                random_string(8): random.random(),
                random_string(8): random.randint(1,99999),
                random_string(8): random_string(32),
            })

        xon_text = xon.dumps(lst)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

    def test_vs_json_3(self):
        d = {}
        for j in range(70):
            lst = []
            for i in range(100):
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
            d[random_string(8)] = lst

        xon_text = xon.dumps([d])
        #print(xon_text)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(d)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

    def test_vs_json_4(self):
        lst = []
        for i in range(4000):
            lst.append([
                random_string(8), random_string(32),
                random_string(32), random_string(8),
                random_string(8), random_string(32),
                random_string(32), random_string(32),
                random_string(8), random_string(8),
                random_string(32), random_string(32),
                random_string(8), random_string(8),
                random_string(32), random_string(8),
                random_string(8), random_string(32),
                random_string(32), random_string(8),
                random_string(8), random_string(8),
                random_string(32), random_string(32),
                random_string(8), random_string(8),
                random_string(32), random_string(8),
                random_string(8), random_string(32),
            ])

        xon_text = xon.dumps(lst)
        #print(xon_text)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

    def test_vs_json_5(self):
        lst = []
        for i in range(5000):
            lst.extend([
                random_string(8), random_string(8),
                random_string(32), random_string(8),
                random_string(32), random_string(32),
                random_string(8), random_string(8),
                random_string(8), random_string(8),
                random_string(32), random_string(8),
                random_string(8), random_string(32),
                random_string(32), random_string(8),
                random_string(32), random_string(32),
                random_string(8), random_string(8),
                random_string(32), random_string(8),
                random_string(32), random_string(32),
            ])

        xon_text = xon.dumps(lst)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

    def test_vs_json_6(self):
        lst = []
        for i in range(5000):
            lst.extend([
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
                random.randint(1,99999), random.randint(1,99999),
            ])
        lst = [lst]

        xon_text = xon.dumps(lst)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

    def test_vs_json_7(self):
        lst = []
        for i in range(5000):
            lst.extend([
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
                random.random(), random.random(),
            ])
        lst = [lst]

        xon_text = xon.dumps(lst)
        ldr = xon.iloads(xon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = ldr.load()
        dt_xon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('\nxon:', dt_xon, 'json', dt_json)

        #self.assertTrue(dt_xon < dt_json)

def run():
    inst = SimpleONvsJSONTestCase()
    inst.test_vs_json_1()
    inst.test_vs_json_2()
    inst.test_vs_json_3()
    inst.test_vs_json_4()
    inst.test_vs_json_5()

#run()
