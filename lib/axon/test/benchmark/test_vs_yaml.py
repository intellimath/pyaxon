# -*- coding: utf-8 -*-
from __future__ import print_function

import yaml
import random
import time
import axon

def random_string(n):
    text = ''.join([chr(ord('a')+random.randint(1,20)) for i in range(20)])
    return axon.as_unicode(text)

class AXONvsYAML:

    def test_vs_yaml_1(self):
        lst = []
        for i in range(2000):
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

        axon_text = axon.dumps(lst, pretty=False)
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0

        print('axon:', dt_axon, 'yaml', dt_yaml)

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

        axon_text = axon.dumps([d], pretty=False)
        #print(axon_text)
        t0 = time.time()
        v = axon.loads(axon_text)
        dt_axon = time.time() - t0

        print('axon:', dt_axon, 'yaml', dt_yaml)

def test_yaml():
    inst = AXONvsYAML()
    inst.test_vs_yaml_1()
    inst.test_vs_yaml_2()



