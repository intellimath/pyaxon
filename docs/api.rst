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

.. autoclass:: Node
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

.. autofunction:: node


----------
Exceptions
----------


.. class:: LoadExit

   Exception for exit load AXON representation from file or text.

