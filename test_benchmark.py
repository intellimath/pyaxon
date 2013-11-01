# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) <2011-2013> <Shibzukhov Zaur, szport at gmail dot com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import print_function
import json
import axon

try:
    import yaml
    use_yaml = 1
except:
    use_yaml = 0

use_yaml = 0

import random
import time
try:
    import matplotlib.pyplot as plt
    use_plt = 1
except:
    use_plt = 0

import gc

# <codecell>

def random_string(n):
    text = ''.join(chr(ord('a')+random.randint(1,20)) for i in range(20))
    text = axon.as_unicode(text)
    return text

# <codecell>

yaml_times_dump = []
json_times_dump = []
axon_times_dump = []
yaml_times_load = []
json_times_load = []
axon_times_load = []

def make_test(data):
    if type(data) == dict:
        data = [data]

    t0 = time.time()
    axon_text = axon.dumps(data, sorted=0)
    dt_axon_dump = time.time() - t0
    axon_times_dump.append(dt_axon_dump)

    t0 = time.time()
    v = axon.loads(axon_text)
    dt_axon_load = time.time() - t0
    axon_times_load.append(dt_axon_load)

    t0 = time.time()
    json_text = json.dumps(data)
    dt_json_dump = time.time() - t0
    json_times_dump.append(dt_json_dump)

    t0 = time.time()
    v = json.loads(json_text)
    dt_json_load = time.time() - t0
    json_times_load.append(dt_json_load)

    if use_yaml:
        t0 = time.time()
        yaml_text = yaml.dump(data, Dumper=yaml.CDumper)
        dt_yaml_dump = time.time() - t0
        yaml_times_dump.append(dt_yaml_dump)

        t0 = time.time()
        v = yaml.load(json_text, Loader=yaml.CLoader)
        dt_yaml_load = time.time() - t0
        yaml_times_load.append(dt_yaml_load)
    else:
        dt_yaml_dump, dt_yaml_load = float('nan'), float('nan')

    print('Dump:: axon: %.3f json: %.3f yaml: %.3f' % (dt_axon_dump, dt_json_dump, dt_yaml_dump))
    print('Load:: axon: %.3f json: %.3f yaml: %.3f' % (dt_axon_load, dt_json_load, dt_yaml_load))

# <codecell>

def test_1():
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
    return lst

make_test(test_1())

# <codecell>

def test_2():
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
    return lst

make_test(test_2())

# <codecell>

def test_3():
    d = {}
    for j in range(100):
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
    return d

make_test(test_3())

# <codecell>

def test_4():
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
    return lst

make_test(test_4())

# <codecell>

def test_5():
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
    return lst

make_test(test_5())

# <codecell>

def test_6():
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
    return lst

make_test(test_6())

# <codecell>

def test_7():
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
    return lst

make_test(test_7())

# <codecell>

#import urllib

#text = urllib.urlopen(r'https://raw.github.com/zeMirco/sf-city-lots-json/master/citylots.json').read()
#print(text[:100])
#data = json.loads(text)
#del text

#make_test(data)

# <codecell>

def make_plot():
    tests = range(1,len(axon_times_dump)+1)
    plt.figure(figsize=(10.0, 7.0))

    plt.subplot(2,1,1)
    plt.title('Dumping')
    plt.plot(tests, axon_times_dump, label='axon', marker='o')
    plt.plot(tests, json_times_dump, label='json', marker='o')
    if use_yaml:
        plt.plot(tests, yaml_times_dump, label='yaml', marker='o')
    plt.legend()
    plt.grid()
    plt.minorticks_on()

    plt.subplot(2,1,2)
    plt.title('Loading')
    plt.plot(tests, axon_times_load, label='axon', marker='o')
    plt.plot(tests, json_times_load, label='json', marker='o')
    if use_yaml:
        plt.plot(tests, yaml_times_load, label='yaml', marker='o')
    plt.legend()
    plt.grid()
    plt.minorticks_on()

print('Dumping:')
print('axon:', *[('%.3f' % t) for t in axon_times_dump])
print('json:', *[('%.3f' % t) for t in json_times_dump])
if use_yaml:
    print('yaml:', *[('%.3f' % t) for t in yaml_times_dump])
print('Loading:')
print('axon:', *[('%.3f' % t) for t in axon_times_load])
print('json:', *[('%.3f' % t) for t in json_times_load])
if use_yaml:
    print('yaml:', *[('%.3f' % t) for t in yaml_times_load])
if use_plt:
    make_plot()
    plt.show()


