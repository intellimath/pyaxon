# coding: utf-8

from distutils.core import setup

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

use_cython = 0

if use_cython:
    from Cython.Distutils import Extension, build_ext
    from Cython.Compiler import Options
    Options.fast_fail = True
    Options.binding = False

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
else:
    from distutils.command.build_ext import build_ext
    from distutils.extension import Extension
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

long_description = open('README.rst').read()

setup(
    name = 'pyaxon',
    version = '0.5.3',
    description = 'Python library for An eXtended Object Notation (AXON)',
    author = 'Zaur Shibzukhov',
    author_email="szport@gmail.com",
    #maintainer="Zaur Shibzukhov",
    #maintainer_email="szport@gmail.com",
    license="MIT License",
    cmdclass = {'build_ext': build_ext, 'build_py': build_py},
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
