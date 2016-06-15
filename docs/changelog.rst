History of changes
------------------

**0.9**

1. Now date/time/datetime values have prefix ``^`` in order to be more explicit 
   (``12:00`` --> ``^12:00``, ``2010-12-31`` --> ``^2010-12-31``).
   This change is important for adding support for more wider range of simple type values
   for keys in dicts in the next version ``0.10``.
   In 0.9.x loading of old notation of date/time/datetime values are allowed. 
   In ``0.10`` old notation will be removed. 
   In order to convert ``pyaxon`` text in safe mode to new date/time/datetime notation ``0.9``::

      import axon
	  
	  axon.dumps(axon.loads(text))
	  axon.dump(path, axon.loads(path, text))

**0.8.2**

1. Fix dump of toplevel dict when sort=1.

**0.8.1**

1. Now node objects support access to subnodes using attribute access.
2. Now pyaxon support continues integration via appveyor.

**0.8**

1. Now name of complex value in formatted form without {} hasn't suffix ':'. For example::

      person
         name: "Alex"
         age: 36
		
   instead of::

       person:
          name: "Alex"
          age: 36

2. Introduce used defined constants using ``defname(name, value)`` function.
   Such names in ``AXON`` message always have ``$`` prefix (for example, ``$one``, ``$PI``).
3. Attributes of the ``Node`` objects are ``axon.OrederDict`` instance now to preserve order
   of attributes.
4. Introduce new syntax for oredered dict: ``[... key:val ...]`` and ``[:]`` for empty ordered dict.
   Later ``<>``-syntax for ordered dicts will be removed.
5. Extend ``AXON`` for converting text into ``axon.OrderedDict`` object  
   and dumping instances of ``collections.MutableMapping`` to text containing sequence 
   of ``key:val`` pairs. 
   For example::

		name: "Alex"
		age: 32
		email: "mail@example.com"
		
   will converted to ``axon.OrderedDict([('name','Alex'), ('age',32), ('email','mail@example.com')])``. 
		
6. ``pyaxon`` now builds with MSVC.


**0.7**

1. Safe mode loading/dumping on named complex values are based on general ``Node`` objects.
2. Attributes in safe mode are represented as ``Attribute`` objects.
3. Named complex values are now sensitive to an order of containing values and attributes.
4. The protocol for unsafe loading/dumping of named complex values is changed.
5. Old safe mode loading/dumping are still here in the ``mode='safe_old'``

**0.6**

1. Use compiled `decimal` module when possible.
2. Add syntax "< ... key:value ... >" to AXON in order to load/dump ordered dicts.
3. Add cython implementation of ordered dict `axon.odict`.
   (API compatible with `collections.OrderedDict`).
4. Fix bug with number-like string keys in dicts.

**0.5.11**

1. Add ability to dump custom class objects as dict, list or tuple.
2. Add support (`axon.convert`) to convertion of safely loaded objects to given type.
3. Fix several bugs.

Special credit to `sbant <https://bitbucket.org/sbant1983>`_.

**0.5.10**

1. Make error messages in loader more useful.
2. Refactoring of comment handling with addition of some tests.
3. Fix crossreference issue with unsafe mode of loading/dumping.
4. Add windows installers.

**0.5.9**

1. Some errors with processing of comment lines are fixed.
2. It's possible now to use "d"/"D" suffix instead of "$" to indicate decimal values.
3. Fix problem with mixing of tabs ('\t') with other spacing characters.
4. Fix example of AXON in index.rst to use "d/D" suffix for decimal values.

**0.5.8**

1. Fix 2.7/3.3 compatibility error with reading from files.
2. Pretty dumping now is more compact in simple cases.
3. Now default pretty dumping mode (``pretty=1``) is indented without braces (like YAML);
   new parameter ``braces=1`` with ``pretty=1`` specifies formatted mode with braces (like JSON).

**0.5.7**

1. Refine indentation control when loading complex objects in indented form.
2. Restore support of names as quoted strings a.k.a. ``'the name'``.
3. Make ``date/time/datetime`` creation code compatible with pure python mode.
4. Add ``hsize`` parameter in pretty dumping mode. It specifies maximum number of
   simple data items in the line.
5. Add more tests by examples.

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

.. raw:: html

    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-42353741-1', 'bitbucket.org');
      ga('send', 'pageview');
    </script>
