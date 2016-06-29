from __future__ import unicode_literals, print_function
from axon import loads, dumps
import unittest

from axon.test import samples


_dict = {}
for name in dir(samples):
    if name.startswith('text'):
        items = name.split('_')
        _, num, key = items
        d = _dict.setdefault(num, {})
        d[key] = getattr(samples, name)

class SamplesTestCase(unittest.TestCase):
    pass

for key, d in _dict.items():
    text_o, text_0, text_1, text_2 = d['o'], d['0'], d['1'], d['2']
    def ftest(self, text_o=text_o, text_0=text_0, text_1=text_1, text_2=text_2):
        vs = loads(text_o)
        t_0 = dumps(vs, sorted=1)
        t_1 = dumps(vs, pretty=1, braces=1, sorted=1)
        t_2 = dumps(vs, pretty=1, sorted=1)
        #toks = tokens(text_o)
        #t_3 = ''.join(toks)
        #print(t_0, t_1, t_2)
        #print(text_0, text_1, text_2)
        self.assertEqual(t_0, text_0)
        self.assertEqual(t_1, text_1)
        self.assertEqual(t_2, text_2)
        #self.assertEqual(t_3, text_0)
    fname = '_'.join(['test_samples', key])
    #setattr(ftest, str('__name__'), fname)
    setattr(SamplesTestCase, fname, ftest)
    del ftest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SamplesTestCase))
    return suite
