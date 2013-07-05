# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import axon
import random
import time
from axon.types import unicode_type
import gc

def random_string(n):
    text = ''.join(chr(ord('a')+random.randint(1,20)) for i in range(20))
    text = axon.as_unicode(text)
    return text

class AXONvsJSON:

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

        axon_text = axon.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)

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

        axon_text = axon.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)

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

        axon_text = axon.dumps([d])
        #print(axon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(d)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)

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

        axon_text = axon.dumps(lst)
        #print(axon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)

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

        axon_text = axon.dumps(lst)
        ldr = axon.iloads(axon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)

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

        axon_text = axon.dumps(lst)
        ldr = axon.iloads(axon_text)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)

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

        axon_text = axon.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0
        gc.enable()

        json_text = json.dumps(lst)
        gc.collect()
        gc.disable()
        t0 = time.time()
        v = json.loads(json_text)
        dt_json = time.time() - t0
        gc.enable()

        print('axon:', dt_axon, 'json', dt_json)


def test_json():
    inst = AXONvsJSON()
    inst.test_vs_json_1()
    inst.test_vs_json_2()
    inst.test_vs_json_3()
    inst.test_vs_json_4()
    inst.test_vs_json_5()
