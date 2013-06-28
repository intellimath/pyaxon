
..
    =================================
    AXON: An eXtended Object Notation
    =================================

.. Contents:
..
.. .. toctree::
..    :maxdepth: 2
..

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

What is AXON
------------

An eXtended Object Notation (``AXON``) is simple text based format for interchanging
objects, documents and data.
Simple language constructions mainly borrowed from ``JSON``,
``TextFormat`` of ``Google Protocol Buffers`` and ``Python``'s indented statement syntax.

``AXON`` is designed as text based language for streaming data exchange
in first place.
It was tried to learn lessons from the experience of
``XML``, ``JSON``, ``YAML`` and ``Google Protocol Buffers``.

* ``AXON`` is easy to understand, read and write.

* ``AXON`` is easy to parse and generate.

* Syntax of ``AXON`` is independent of programming languages.

* ``AXON`` can be used as simple text based language for serialization of objects,
  documents and variety of data.

Creation of ``AXON`` had following objectives:

* Overcoming lack of support in ``JSON`` of date/time, decimal and binary data.

* Overcoming inability to represent in ``JSON`` complex data
  with cross-references natively.

* Extension of ``JSON`` for native support of named/taged data structures
  (typed complex data, elements of documents etc.) in order to act in
  cases where ``XML`` is more suitable than ``JSON``.

* Removing ``','`` as mandatory character-separator for items in containers.

* Saving relative simplicity of the language compared to ``JSON``.

``AXON`` is designed as text based format that has compact form and
formatted form in both `C` and `Python` style for ease of developers.

Expression form::

    axon {
        name: "An eXtended Object Notation"
        short_name: "AXON"
        python_library: "pyaxon"
        atomic_values {
            int: [0 -1 17]
            float: [3.1428 1.5e-17]
            decimal: [10$ 1000.35$ -1.25e6$]
            bool: [true false]
            'unicode string': "abc абв 中文本"
            'unicode multiline string': "one
    two
    three"
            date: 2012-12-31
            time: [12:00 12:30:34 12:35:12.000120 12:35+03]
            datetime: [2012-12-31T12:30:34 2012-12-31T12:35+03]
            binary: |UTcJFhV3cl97ZEk+BA0hWggDUj8lbE0bQH5rUy0nNjwmZDpANClsAj4WeDsfCW
    kcW2Bdc0VNQCQVZCBhXxFGJBpSLGs3HGlcbSdgdH4ab34UBTwndTs2MXdSOxIGB
    gdYclFQYnlDH3NfUSI1LEcHDARDeFcDCBwiPTAZODU=
        }
        complex_values {
            anonymous {
                list: ["one" "two" "three"]
                dict: {"one":1 "two":2 "three":3}
                tuple: ("nodes" "edges")
            }
            named {
                mapping: rgb {
                    red:16 green:32 blue:64}
                element: node {
                    id: 1
                    node {
                        id: 2
                        class: "A"}
                    node {
                        id: 3
                        class: "B"}
                    }
                sequence: primes {
                    2 3 5 7 11 13 17 19 23 29 31}
                instance: row {
                    12 2003-12-01 12:00
                    T: 12.1 R:0.5 W:5 D:"W"}
            }
    }


Statement form::

    axon:
        name: "An eXtended Object Notation"
        short_name: "AXON"
        python_library: "pyaxon"
        atomic_values:
            int: [0 -1 17]
            float: [3.1428 1.5e-17]
            decimal: [10$ 1000.35$ -1.25e6$]
            bool: [true false]
            'unicode string': "abc абв 中文本"
            'unicode multiline string': "one
    two
    three"
            date: 2012-12-31
            time: [12:00 12:30:34 12:35:12.000120 12:35+03]
            datetime: [2012-12-31T12:30:34 2012-12-31T12:35+03]
            binary: |UTcJFhV3cl97ZEk+BA0hWggDUj8lbE0bQH5rUy0nNjwmZDpANClsAj4WeDsfCW
    kcW2Bdc0VNQCQVZCBhXxFGJBpSLGs3HGlcbSdgdH4ab34UBTwndTs2MXdSOxIGB
    gdYclFQYnlDH3NfUSI1LEcHDARDeFcDCBwiPTAZODU=
        complex_values:
            anonymous:
                list: ["one" "two" "three"]
                dict: {"one":1 "two":2 "three":3}
                tuple: ("nodes" "edges")
            named:
                mapping: rgb:
                    red:16 green:32 blue:64
                element: node:
                    id: 1
                    node:
                        id: 2
                        class: "A"
                    node:
                        id: 3
                        class: "B"
                sequence: primes:
                    2 3 5 7 11 13 17 19 23 29 31
                instance: row:
                    12 2003-12-01 12:00
                    T: 12.1 R:0.5 W:5 D:"W"


Python pyaxon library
---------------------

`pyaxon <https://pypi.python.org/pypi/pyaxon>`_ is an `MIT Licensed <http://opensource.org/licenses/MIT>`_
`python <http://www.python.org>`_ library for ``AXON``.

There are introductory `IPython` notebooks:

* `Tutorial <http://nbviewer.ipython.org/url/intellimath.bitbucket.org/axon/notebooks/axon_tutorial.ipynb>`_
* `Examples <http://nbviewer.ipython.org/url/intellimath.bitbucket.org/axon/notebooks/axon_examples.ipynb>`_
* `Patterns <http://nbviewer.ipython.org/url/intellimath.bitbucket.org/axon/notebooks/axon_patterns.ipynb>`_
* `Syntax <http://nbviewer.ipython.org/url/intellimath.bitbucket.org/axon/notebooks/axon_syntax.ipynb>`_

Repository for ``AXON`` and ``pyaxon`` is `here <https://bitbucket.org/intellimath/axon>`_.

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api
