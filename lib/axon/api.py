# The MIT License (MIT)
#
# Copyright (c) <2011-2015> <Shibzukhov Zaur, szport at gmail dot com>
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

from __future__ import unicode_literals, print_function
from axon._loader import Loader
from axon._dumper import Dumper
from axon.types import unicode_type, str_type
from axon._objects import as_unicode, StringReader, StringWriter

import io

def display(text, pretty=1, braces=0, sorted=1, hsize=0, crossref=0):
    '''
    Display AXON text in formatted form for easy read.

    :param text:
       Unicode AXON text

    :returns:
        Formatted form of AXON encoded text.
    '''
    vals = loads(text)
    print(dumps(vals, pretty, braces, sorted, hsize, crossref))
    
def display_html(vals):
    '''
    Convert objects into three AXON forms for output in IPython notebook.

    :param vals:
       List of objects or ordered dict.

    :returns:
        IPython TabbedView widget.
    '''
    from IPython.html.widgets import Tab, HTML

    # Compact form
    p1 = dumps(vals, crossref=1)
    # Formatted form without braces
    p2 = dumps(vals, pretty=1, crossref=1)
    # Formatted form with braces
    p3 = dumps(vals, pretty=1, braces=1, crossref=1)
    
    wg = Tab(
        ( HTML("<pre>%s</pre>" % p1), 
          HTML("<pre>%s</pre>" % p2), 
          HTML("<pre>%s</pre>" % p3))
    )
    wg.set_title(0, "Compact")
    wg.set_title(1, "Formatted")
    wg.set_title(2, "Formatted with {}")
    wg.selected_index = 1

    return wg    

def dumps(vals, pretty=0, braces=0, sorted=1, hsize=0, crossref=0):
    '''
    Dump sequence of values into unicode text.

    :param vals:
       Sequence of values to convert.

    :param pretty:
        Flag indicating pretty dumping:

        * `True` - use pretty dumping
        * `False` - compact dumping (default)

    :param braces:
        Flag indicating using braces (JSON-style) during formatting:

        * `True` - use formatting with braces (JSON-style)
        * `False` - use formatting without braces (YAML-style, default)

    :param crossref:
        Flag for crossreferece support in unsafe mode

        * `True` - use reference to the object on duplicate
        * `False` - use copy of the object on duplicate (default)

    :returns:
        Unicode text in AXON format.
    '''
    fd = StringWriter()

    dumper = Dumper(fd, pretty, braces, sorted, hsize, crossref)
    dumper.dump(vals)
    v = fd.getvalue()
    fd.close()
    return v

def dump(fpath, val, pretty=0, braces=0, sorted=1, hsize=0, crossref=0, encoding='utf-8'):
    '''\
    Same as :py:func:`dumps` but for dumping into a file.

    :param fpath:
        Path to file for dumping.

    For other parameters see :py:func:`dumps`.
    '''
    fd = io.open(fpath, mode='w', encoding=encoding)

    dumper = Dumper(fd, pretty, braces, sorted, hsize, crossref)
    dumper.dump(val)
    fd.close()

def loads(text, mode="safe", errto=None):
    '''\
    Load values from unicode text.

    :param text:
        Unicode text.

    :param mode:
        Specifies the method of building python objects for complex values
        (see .. py:func:`load`)

    :param errto:
        Name of file for reporting errors

    :returns:
        List of values.
    '''
    text = as_unicode(text)
    fd = StringReader(text)

    loader = Loader(fd, mode, errto)
    return loader.load()

def load(fd, mode="safe", errto=None, encoding='utf-8'):
    '''
    Load object from unicode text.

    :param fd:
        Input file name of file object opening as TextIO/StringIO.

    :param mode:
        Specifies the method of building python objects for complex values.

        There are values of parameter `mode`:
            * `safe` - use safe object builder
            * `strict` - use unsafe builder with strict name resolution: if there is no registered name
              for building object builder return `undef` object
            * `mixed` - use unsafe object builder with following rule: if there is no registered name
              for building object then use `safe` mode.

    :param errto:
        Name of file for reporting errors

    :param encoding:
        Encoding of input file (default `utf-8`).

    :returns:
        List of values.
    '''
    if type(fd) in (str_type, unicode_type):
        fd = io.open(fd, mode='r', encoding=encoding)

    loader = Loader(fd, mode, errto)
    return loader.load()

def iload(fd, mode="safe", errto=None, encoding='utf-8'):
    '''\
    Iterative loading values from input file.

    Arguments are same as in .. py:func:`load`.

    :returns:
        iterator object.
    '''

    if type(fd) in (str_type, unicode_type):
        fd = io.open(fd, mode='r', encoding=encoding)

    loader = Loader(fd, mode, errto)
    for val in loader.iload():
        yield val
    
def iloads(text, mode="safe", errto=None):
    '''\
    Iterative loading values from unicode text.

    :param text:
        Unicode text.

    :param mode:
        Specifies the method of building python objects for complex values
        (see .. py:func:`load`)

    :param errto:
        Name of file for reporting errors

    :returns:
        Iterator object. It returns values during iteration.
    '''
    text = as_unicode(text)
    fd = StringReader(text)

    loader = Loader(fd, mode, errto)
    for val in loader.iload():
        yield val
    

# def itokens(text, mode="safe", errto=None, encoding='utf-8'):
#     text = as_unicode(text)
#     fd = StringReader(text)
#
#     loader = Loader(fd, mode, errto)
#
#     for tok in loader.itokens():
#         yield tok
#
