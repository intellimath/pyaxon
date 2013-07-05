# coding: utf-8
from __future__ import print_function

import unittest

from axon.test.benchmark.test_vs_json import *
try:
    from axon.test.benchmark.test_vs_yaml import *
    is_yaml = 1
except:
    is_yaml=0

print("Compare performance: JSON")
test_json()
if is_yaml:
    print("Compare performance: YAML")
    test_yaml()
