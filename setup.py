# coding: utf-8

# The MIT License (MIT)
# 
# Copyright (c) <2011-2016> <Shibzukhov Zaur, szport at gmail dot com>
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

from io import open

#from distutils.core import setup
from setuptools import setup

from distutils.command.build_py import build_py as _build_py

class build_py(_build_py):
    def find_package_modules(self, package, package_dir):
        modules = _build_py.find_package_modules(self, package, package_dir)
        py_ext_modules = []
        for ext in self.distribution.ext_modules:
            for src in ext.sources:
                if src.endswith('.py'):
                    py_ext_modules.append(src)
        if py_ext_modules:
            modules = [m for m in modules if m[2] not in py_ext_modules]
        return modules

use_cython = 1

if use_cython:
    from Cython.Distutils import Extension, build_ext
    from Cython.Compiler import Options
    Options.fast_fail = True
    #Options.emit_code_comments = False
    

    ext_modules = [
        Extension(
            "axon._objects",
            ["lib/axon/_objects.py"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
        Extension(
            "axon._loader",
            ["lib/axon/_loader.py"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
        Extension(
            "axon._dumper",
            ["lib/axon/_dumper.py"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
        Extension(
            "axon.odict",
            ["lib/axon/odict.pyx"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
    ]
else:
    from distutils.command.build_ext import build_ext
    from distutils.extension import Extension
    ext_modules = [
        Extension(
            "axon._objects",
            sources=["lib/axon/_objects.c"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
        Extension(
            "axon._loader",
            sources=["lib/axon/_loader.c"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
        Extension(
            "axon._dumper",
            sources=["lib/axon/_dumper.c"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
        Extension(
            "axon.odict",
            ["lib/axon/odict.c"],
            #extra_compile_args=['-Wno-unused-function', '-Wno-unreachable-code'],
        ),
    ]

long_description = open('README.rst', encoding='utf-8').read()


setup(
    name = 'pyaxon',
    version = '0.9',
    description = 'Python library for AXON',
    author = 'Zaur Shibzukhov',
    author_email = 'szport@gmail.com',
    #maintainer = 'Zaur Shibzukhov',
    #maintainer_email = 'szport@gmail.com',
    license = "MIT License",
    cmdclass = {'build_ext': build_ext, 'build_py': build_py},
    ext_modules = ext_modules,
    package_dir = {'': 'lib'},
    packages = ['axon', 'axon.test', 'axon.test.benchmark'],
    scripts = ['bin/xml2axon', 'bin/json2axon'],
    url = 'http://intellimath.bitbucket.org/axon',
    download_url = 'https://bitbucket.org/intellimath/pyaxon',
    long_description = long_description,
    platforms = 'Linux, Mac OS X, Windows',
    keywords = ['Object Notation', 'Serialization', 'Configuration'],
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
