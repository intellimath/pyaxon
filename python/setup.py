# coding: utf-8

from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize
from Cython.Compiler import Options
Options.fast_fail = True
Options.binding = False

import os

'''
ext_modules = [
    Extension(
        "axon._objects",
        ["lib/axon/_objects.py"]
    ),
    Extension(
        "axon._loader",
        ["lib/axon/_loader.py"]
    ),
    Extension(
        "axon._dumper",
        ["lib/axon/_dumper.py"]
    ),
]
'''

ext_modules = cythonize([
     'lib/axon/_objects.py',
     'lib/axon/_loader.py',
     'lib/axon/_dumper.py'])

long_description = '''\
Python library for `AXON <http://axon.intellimath.org>`_.

An eXtended Object Notation (``AXON``) is simple text based format for interchanging
objects, documents and data.
'''

setup(
    name = 'pyaxon',
    version = '0.5',
    description = 'Python library for An eXtended Object Notation (AXON)',
    author = 'Zaur Shibzukhov',
    author_email="szport@gmail.com",
    maintainer="Zaur Shibzukhov",
    maintainer_email="szport@gmail.com",
    license="MIT License",
    ext_modules = ext_modules,
    package_dir = {'': 'lib'},
    packages = ['axon', 'axon.test', 'axon.test.benchmark'],
    url = 'http://axon.intellimath.org',
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
