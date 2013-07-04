.. _api:

===
API
===


.. module:: axon

This part of the documentation covers interfaces of *axon*.


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

   Exception for exit load AXON representation from file or text.

