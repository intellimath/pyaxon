======
PYAXON
======

``pyaxon`` is an `MIT Licensed <http://opensource.org/licenses/MIT>`_ python library for `AXON <http://axon.intellimath.org>`_ -
An eXtended Object Notation - simple text based format for interchanging
objects, documents and data.
It tries to combine the best of `JSON <http://www.json.org>`_,
`XML <http://www.w3.org/XML/>`_ and `YAML <http://www.yaml.org>`_.

Main repository for ``pyaxon`` is on `bitbucket <https://bitbucket.org/intellimath/pyaxon>`_.
There is an mirror on `github <https://github.com/intellimath/pyaxon>`_

Features
--------

1. Provide simple API for loading and dumping of objects.
2. Provide safe loading and dumping by default.
3. Provide unsafe loading and dumping of objects on the base of registration of factory/reduce callables.
4. Provide a way for fully controlled by application/framework/library unsafe loading and dumping.
5. It's sufficiently fast so as to be useful.

History
-------

**0.5.6**

1. Fix support for decimal ``Infinity`` and ``NaN``.
2. Fix support for ``base64`` in ``python2.7``.
3. Add support for complex names like ``a.b.c.d``.

**0.5.5**

1. Make creation of custom builders of atomic values easier too (in ``cython`` only).
2. Make creation of custom object builders easier (both in ``cython`` and ``python``).
   This allows you to implement custom import/export for data in ``XML`` and ``YAML``
   representation.
3. Add plotting of results to simple benchmark script.

**0.5.4**

1. Make internal timezone class (for ``python2.7``) compatible with datetime.timezone class (for ``python3.2`` and higher).
2. Make creation of custom object builders (both safe and unsafe) easier (in ``cython`` only).

**0.5.3**

1. Dumping is now faster.

**0.5.2**

1. Refactor setup.py so that .py sources of extensions dosn't installed.
2. Ensuire that attribute names and keys loads and dumps correctly.
3. Add explicit flag (``use_cython``) in order to decide when to use cython compiler.

**0.5.1**

1. Add notebook with performance comparisons with ``JSON`` and ``YAML``.
2. Refactor setup.py so that project could be installed with/without ``Cython`` installation.
3. Some improvements with introductory notebooks.
4. Make project uploadable to ``PyPI`` by ``setup.py``.



**0.5**

   First public release of ``pyaxon``.
