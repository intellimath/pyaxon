# {{LICENCE}}

from __future__ import unicode_literals
from axon._loader import Loader
from axon._dumper import Dumper
from axon.types import unicode_type, str_type
from axon._objects import as_unicode, StringReader, StringWriter

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

class Reader(object):
    def __init__(self, fd, encoding):
        self.fd = fd
        self.encoding = encoding

    def readline(self):
        line = fd.readline()
        return line.decode(encoding)

    def close(self):
        self.fd.close()

def display(text, pretty=1, nsize=3, sorted=1):
    '''
    Display AXON text in formatted form for easy read.

    :param text:
       `unicode` AXON text

    :returns:
        formatted `unicode` AXON text
    '''
    val = loads(text)
    print(dumps(val, pretty=pretty, crossref=True, nsize=nsize, sorted=1))

def dumps(val, pretty=0, crossref=False, nsize=0, sorted=1):
    '''
    Dump value into unicode text.

    :param val:
       value to convert

    :param simple_dumpers:
       dictionary containing callables for text representation of values of simple types &em;
       int, float, decimal, boolean, unicode text, date/time/datetime &em; in form of
       `type`:`dumper`.

    :param type_reducers:
       dictionary containing callables, which returns reduced data for
       representation in AXON.

    :param pretty:
        flag indicating pretty dumping:

        * True - use pretty dumping
        * False - do not use pretty dumping (default)

    :param crossref:
        flag for crossreferece support in unsafe mode

        * True - use crosserefernce support
        * False - do not use crosserefernce support (default)

    :returns:
        unicode string of AXON representation of `val`.
    '''
    #try:
    #    from io import StringIO
    #except ImportError:
    #    from cStringIO import StringIO

    fd = StringWriter()

    dumper = Dumper(fd, crossref, pretty, nsize, sorted)
    dumper.dump(val)
    v = fd.getvalue()
    fd.close()
    return v

def dump(fpath, val, encoding='utf-8', pretty=0, crossref=False, nsize=0, sorted=1):
    '''\
    Same as :py:func:`dumps` but for dumping into a file.

    :param fpath:
        path to file for dumping.

    For other parameters see :py:func:`dumps`.
    '''
    fd = open(fpath, mode='wt', encoding=encoding)
    dumper = Dumper(fd, crossref, pretty, nsize, sorted)
    dumper.dump(val, pretty)
    fd.close()

def loads(text, mode="safe", errto=None, json=False):
    '''\
    Load values from unicode text.

    :param text:
        `unicode` text in AXON.

    :param mode:
        specifies the method of building python objects for complex values
        (see .. py:func:`load`)

    :param errto:
        name of file for reporting errors

    :param json:
        if true then allow to load from json format

    :returns:
        `list` of values.
    '''
    loader = iloads(text, mode, errto, json)
    return loader.load()

def iloads(text, mode="safe", errto=None, json=False):
    '''\
    Iterative loading values from unicode text.

    :param text:
        unicode text in AXON.

    :param mode:
        specifies the method of building python objects for complex values
        (see .. py:func:`load`)

    :param errto:
        name of file for reporting errors

    :param json:
        if true then allow to load from json format

    :returns:
        iterator object.
    '''
    text = as_unicode(text)
    #fd = StringIO(text)
    fd = StringReader(text)

    return iload(fd, mode, errto, json=json)

def load(fd, mode="safe", errto=None, encoding='utf-8', json=False):
    '''
    Load object from unicode text in AXON.

    :param fd:
        input file name of file object opening as TextIO/StringIO

    :param mode:
        specifies the method of building python objects for complex values.

    :param errto:
        name of file for reporting errors

    :param encoding:
        encoding of input file (default `utf-8`)

    There are values of parameter `mode`:
        * "safe" - use safe object builder
        * "strict" - use unsafe builder with strict name resolution: if there is no registered name
          for building object builder return `undef` object
        * "mixed" - use unsafe object builder with following rule: if there is no registered name
          for building object then use `safe` mode.

    :param json:
        if true then allow to load from json format

    :returns:
        `list` of values.
    '''
    loader = iload(fd, mode, errto, encoding, json)
    return loader.load()

def iload(fd, mode="safe", errto=None, encoding='utf-8', json=False):
    '''\
    Iterative loading values from input file.

    Arguments are same as in .. py:func:`load`.

    :returns:
        iterator object.
    '''

    if type(fd) in (str_type, unicode_type):
        try:
            from io import open
            fd = open(fd, mode='rt', encoding=encoding)
        except ImportError:
            fd = open(fd, mode='rt')
            fd = Reader(fd, encoding)

    loader = Loader(fd, mode, errto, json)

    return loader

