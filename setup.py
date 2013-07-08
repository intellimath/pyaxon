# coding: utf-8

from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

from Cython.Compiler import Options
Options.fast_fail = True
Options.binding = False

import os

if use_cython:
    ext_modules = [
        Extension(
            "axon._objects",
            sources=["lib/axon/_objects.py"],
            depends=["lib/axon/_objects.pxd"]
        ),
        Extension(
            "axon._loader",
            sources=["lib/axon/_loader.py"],
            depends=["lib/axon/_loader.pxd"]
        ),
        Extension(
            "axon._dumper",
            sources=["lib/axon/_dumper.py"],
            depends=["lib/axon/_dumper.pxd"]
        ),
    ]
else:
    ext_modules = [
        Extension(
            "axon._objects",
            sources=["lib/axon/_objects.c"]
        ),
        Extension(
            "axon._loader",
            sources=["lib/axon/_loader.c"],
        ),
        Extension(
            "axon._dumper",
            sources=["lib/axon/_dumper.c"]
        ),
    ]

for ext_mod in ext_modules:
    for i, f in enumerate(ext_mod.sources):
        if not os.path.exists(f) and f.endswith('.py'):
            ext_mod.sources[i] = ext_mod.sources[i].replace('.py', '.c')
            ext_mod.depends = []

long_description = '''\
A `MIT licensed <http://opensource.org/licenses/MIT>`_ Python library for `AXON <http://axon.intellimath.org>`_.

An eXtended Object Notation (``AXON``) is simple text based format for interchanging
objects, documents and data.
'''

setup(
    name = 'pyaxon',
    version = '0.5.1',
    description = 'Python library for An eXtended Object Notation (AXON)',
    author = 'Zaur Shibzukhov',
    author_email="szport@gmail.com",
    #maintainer="Zaur Shibzukhov",
    #maintainer_email="szport@gmail.com",
    license="MIT License",
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
    package_dir = {'': 'lib'},
    packages = ['axon', 'axon.test', 'axon.test.benchmark'],
    url = 'http://axon.intellimath.org',
    download_url = 'https://bitbucket.org/intellimath/pyaxon',
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
