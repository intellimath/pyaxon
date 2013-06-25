# coding: utf-8

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

from Cython.Compiler import Options
Options.fast_fail = True
Options.binding = False

import os

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

to_cythonize = 1
# for ext in ext_modules:
#     for i, source in enumerate(ext.sources):
#         print '***', source
#         if source.endswith('.py'):
#             c_source = source.replace('.py', '.c')
#             if os.path.exists(c_source):
#                 ext.sources[i] = c_source
#                 to_cythonize = 0

if to_cythonize:
    ext_modules = cythonize(ext_modules)

setup(
    name = 'axon',
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
    long_description = """\
Python library for An eXtended Object Notation (AXON).

AXON is simple text based format for interchanging objects,
documents and almost any data.

This is reference implementation for AXON. It's reasonable fast.""",
    classifiers = [
        'Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Serialization',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
