# coding: utf-8

# The MIT License (MIT)
# 
# Copyright (c) <2011-2014> <Shibzukhov Zaur, szport at gmail dot com>
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

from axon._objects import defname, factory, type_factory
from axon._objects import convert, reset_factory, reset_type_factory
from axon._objects import undef, as_unicode, as_list, as_dict, as_tuple, as_name
from axon._dumper import reduce, dump_as_str


import axon
import xml.etree.ElementTree as etree
import json

@reduce(etree.Element)
def reduce_ElementTree(e):
	attrs = {axon.as_unicode(name):val for name,val in e.attrib.items()}
	if e.text:
		vals = [e.text]
	else:
		vals = []
	for child in e.getchildren():
		vals.append(child)
		if child.tail:
			vals.append(child.tail)
			child.tail = None
	if len(attrs) == 0:
		attrs = None
	if len(vals) == 0:
		vals = None
	return axon.node(axon.as_unicode(e.tag), attrs, vals)
    
del reduce_ElementTree
	

def xml2axon(from_, to_=None, pretty=1, braces=0):
    '''
    Convert from `XML` to `AXON`.
    
    :from:
        The path of input file with `XML` or `XML` string.
        
    :to:
        The path of output file with `XML`` (default is `None`). 
        If `to` is valid path then result of convertion to `AXON` will write to the file.      
    
    :result:
        If `to` is `None` then return string with `AXON`, else return `None`.
    '''
    _text = from_.lstrip()
    if _text.startswith('<'):
        tree = etree.fromstring(from_)
    else:
        tree = etree.parse(from_)
    root = tree._root
    
    if to_ is None:
        return axon.dumps([root], pretty=pretty, braces=braces)
    else:
        axon.dump(to_, [root], pretty=pretty, braces=braces)

def json2axon(from_, to_=None, pretty=1, braces=1):
    '''
    Convert from `JSON` to `AXON`.
    
    :from:
        The path of input file with `JSON` or `JSON` string.
        
    :to:
        The path of output file with `JSON` (default is `None`). 
        If `to` is valid path then result of convertion to `AXON` will write to the file.      
    
    :result:
        If `to` is `None` then return string with `AXON`, else return `None`.
    '''
    text = from_.lstrip()
    if text.startswith('[') or text.startswith('{'):
        val = json.loads(from_)
    else:
        val = json.load(from_)

    if to_ is None:
        return axon.dumps([val], pretty=pretty, braces=braces)
    else:
        axon.dump(to_, [val], pretty=pretty, braces=braces)
