======
pyaxon
======

``pyaxon`` is an `MIT Licensed <http://opensource.org/licenses/MIT>`_ python library for `AXON <http://axon.intellimath.org>`_ -
An eXtended Object Notation - simple text based format for interchanging
objects, documents and data.
It tries to combine the best of `JSON <http://www.json.org>`_,
`XML <http://www.w3.org/XML/>`_ and `YAML <http://www.yaml.org>`_.


Features
--------

1. Provide a simple API for loading and dumping of objects.
2. Provide a safe loading and dumping by default.
3. Provide unsafe loading and dumping of objects on the base of registration of factory/reduce callables.
4. Provide a way for fully controlled by application/framework/library unsafe loading and dumping.
5. It's reasonable fast.

Releases
--------

**0.5.4**

1. Make internal timezone class (for python2.7) compatible with datetime.timezone class (for python3.2 and higher).
2. Make creation of custom object builders (both safe and unsafe) easier.

**0.5.3**

1. Dumping is now faster.

**0.5.2**

1. Refactor setup.py so that .py sources of extensions dosn't installed.
2. Ensuire that attribute names and keys loads and dumps correctly.
3. Add explicit flag (use_cython) in order to decide when to use cython compiler.

**0.5.1**

1. Add notebook with performance comparisons with ``JSON`` and ``YAML``.
2. Refactor setup.py so that project could be installed with/without ``Cython`` installation.
3. Some improvements with introductory notebooks.
4. Make project uploadable to ``PyPI`` by ``setup.py``.



**0.5**

   First public release of ``pyaxon``.
