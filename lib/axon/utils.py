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
	

def xml2axon(from_file, to_file=None):
    '''
    Convert from `XML` to `AXON`.
    
    :from_file:
        The path of input file with `XML`.
        
    :to_file:
        The path of output file with `XML`` (default is `None`). 
        If `to_file` is valid path then result of convertion to `AXON` will write to the file.      
    
    :result:
        If `to_file` is `None` then return string with `AXON`, else return `None`.
    '''
    tree = etree.parse(from_file)
    root = tree._root
    if to_file is None:
        return axon.dumps([root], pretty=1)
    else:
        axon.dump(to_file, [root], pretty=1)

def json2axon(from_file, to_file=None):
    '''
    Convert from `JSON` to `AXON`.
    
    :from_file:
        The path of input file with `JSON`.
        
    :to_file:
        The path of output file with `JSON` (default is `None`). 
        If `to_file` is valid path then result of convertion to `AXON` will write to the file.      
    
    :result:
        If `to_file` is `None` then return string with `AXON`, else return `None`.
    '''
    val = json.load(from_file)
    if to_file is None:
        return axon.dumps([val], pretty=1)
    else:
        axon.dump(to_file, [val], pretty=1)

