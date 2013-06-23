.. _api:

===
API
===


.. module:: axon

This part of the documentation covers all the interfaces of *xon*.  For
parts where *xon* depends on external libraries, we document the most
important right here and provide links to the canonical documentation.

-------
Classes
-------


.. autoclass:: Loader
   :members:

.. autoclass:: Dumper
   :members:
   :inherited-members:

.. autoclass:: Empty
   :members:
   :inherited-members:

.. autoclass:: Sequence
   :members:
   :inherited-members:

.. autoclass:: Mapping
   :members:
   :inherited-members:

.. autoclass:: Element
   :members:
   :inherited-members:

.. autoclass:: Instance
   :members:
   :inherited-members:

---------
Functions
---------

Loading and dumping
-------------------

.. autofunction:: display

.. autofunction:: load

.. autofunction:: loads

.. autofunction:: iload

.. autofunction:: iloads

.. autofunction:: dump

.. autofunction:: dumps

Factory functions for safe mode complex values
----------------------------------------------

.. autofunction:: empty

.. autofunction:: mapping

.. autofunction:: sequence

.. autofunction:: element

.. autofunction:: instance


----------
Exceptions
----------


.. class:: LoadExit

   Exception for exit load SimpleON file or text.

