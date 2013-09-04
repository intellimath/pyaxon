
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

An eXtended Object Notation (``AXON``) is a simple text based format for interchanging of
objects, documents and data.

It tries to combine the best of `JSON <http://www.json.org>`_,
`XML <http://www.w3.org/XML/>`_ and `YAML <http://www.yaml.org>`_.


``AXON`` is designed as text based language for data exchange in first place.

* ``AXON`` is easy to understand, read and write.

* ``AXON`` is easy to parse and generate.

* Syntax of ``AXON`` is independent of programming languages.

* ``AXON`` can be used as simple text based language for serialization of objects,
  documents and variety of data.

Creation of ``AXON`` had following objectives:

* Overcoming lack of support of date/time, decimal and binary data in ``JSON``.

* Overcoming inability to represent in ``JSON`` complex data
  with cross-references natively.

* Extension of ``JSON`` for native support of named/taged data structures
  (typed complex data, elements of documents etc.) in order to act in
  cases where ``XML`` is more suitable than ``JSON``.

* Removing ``','`` as mandatory character-separator for items in containers.

* Saving relative simplicity of the language compared to ``JSON``.

``AXON`` is designed as text based format that has compact form and
formatted form in both `C` and `Python` style for ease of developers.

``AXON`` is an object notation for data, which are composed from atomic values
by several rules of composition:

.. raw:: html

    <table>
    <style type="text/css">
    table {
     /*border: 1px solid black;*/
    }
    td, th {
     padding: 5px;
    }
    th {
     text-align: left;
     background: black;
     color: white;
    }
    </style>
    <thead><th>Name</th><th>Rule</th><th>Example</th></thead>
    <tr><td>list</td><td>[ <b>V</b> … <b>V</b> ]</td>
    <td><pre>
    [1 3.14 3.25$ -∞ ?]
    </pre></td></tr>

    <tr><td>tuple</td><td>( <b>V</b> … <b>V</b> )</td>
    <td><pre>
    (true 12:00 2001-12-31 2001-12-31T12:00)
    </pre></td></tr>

    <tr><td>dictionary</td><td>{ <b>K</b>:<b>V</b> … <b>K</b>:<b>V</b> }</td>
    <td><pre>
    {alpha:1 beta:2 gamma:3 "other chars":4}
    </pre></td></tr>
   
    <tr><td>mapping</td><td><b>N</b> { <b>N</b>:<b>V</b> … <b>N</b>:<b>V</b> }</td>
    <td><pre>
    greek {alpha:123 beta:212 gamma:322}
    </pre></td></tr>

    <tr><td>sequence</td><td><b>N</b> { <b>V</b> … <b>V</b> }</td>
    <td><pre>
    primes {2 3 5 7 11 13 17 19 23}
    </pre></td></tr>

    <tr><td>element</td><td><b>N</b> { <b>N</b>:<b>V</b> … <b>N</b>:<b>V</b> <b>V</b> … <b>V</b> }</td>
    <td><pre>
    node {id:1 node{id:2 "AAA"} node{id:3 "BBB"}}
    </pre></td></tr>
   
    <tr><td>instance</td><td><b>N</b> { <b>V</b> … <b>V</b> <b>N</b>:<b>V</b> … <b>N</b>:<b>V</b> }</td>
    <td><pre>
    datarow { 1 2003-12-01T12:30 T:12.5 R:0.95 W:11 D:"NW"}
    </pre></td></tr>

    <tr><td>empty</td><td><b>N</b> { }</td>
    <td><pre>
    empty { }
    </pre></td></tr>
    </table>

where **N** denotes a *name*, **K** denotes a *key*, **V** denotes a *value*.

Here is an example of ``AXON`` message:

.. raw:: html

    <table>
    <tr><th>formatted expression form</th><th>statement form</th></tr>
    <tr><td><pre>
    axon {
        name: "An eXtended Object Notation"
        short_name: "AXON"
        python_library: "pyaxon"
        atomic_values {
            int: [0 -1 17]
            float: [3.1428 1.5e-17]
            decimal: [10$ 1000.35$ -1.25e6$]
            bool: [true false]
            string: "abc абв 中文本"
            multiline_string: "one
    two
    three"
            date: 2012-12-31
            time: [12:30:34 12:35:12.000120 12:35+03]
            datetime: [2012-12-31T12:30 2012-12-31T12:35+03]
            binary: |UTcJFhV3cl97ZEk+BA0hWggDUj8lbE0bQH5r
    Uy0nNjwmZDpANClsAj4WeDsfCWkcW2Bdc0VNQ
    CQVZCBhXxFGJBpSLGs3HGlcbSdgdH4ab34UBT
    wndTs2MXdSOxIGBgdYclFQYnlDH3NfUSI1LEc
    HDARDeFcDCBwiPTAZODU=
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
    }
    </pre></td>
    <td><pre>
    axon:
        name: "An eXtended Object Notation"
        short_name: "AXON"
        python_library: "pyaxon"
        atomic_values:
            int: [0 -1 17]
            float: [3.1428 1.5e-17]
            decimal: [10$ 1000.35$ -1.25e6$]
            bool: [true false]
            string: "abc абв 中文本"
            multiline_string: "one
    two
    three"
            date: 2012-12-31
            time: [12:30:34 12:35:12.000120 12:35+03]
            datetime: [2012-12-31T12:30 2012-12-31T12:35+03]
            binary: |UTcJFhV3cl97ZEk+BA0hWggDUj8lbE0bQH5r
    Uy0nNjwmZDpANClsAj4WeDsfCWkcW2Bdc0VNQ
    CQVZCBhXxFGJBpSLGs3HGlcbSdgdH4ab34UBT
    wndTs2MXdSOxIGBgdYclFQYnlDH3NfUSI1LEc
    HDARDeFcDCBwiPTAZODU=
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
    </pre></td></tr>
    <tr><th colspan=2>compact expression form</th></tr>
    <tr><td colspan=2><pre>
    axon{name:"An eXtended Object Notation" python_library:"pyaxon" short_name:"AXON"
    atomic_values{binary:|UTcJFhV3cl97ZEk+BA0hWggDUj8lbE0bQH5rUy0nNjwmZDpANClsAj4We
    DsfCWkcW2Bdc0VNQCQVZCBhXxFGJBpSLGs3HGlcbSdgdH4ab34UBTwndTs2MXdSOxIGBgdYclFQYnlDH
    3NfUSI1LEcHDARDeFcDCBwiPTAZODU=
    bool:[true false] date:2012-12-31 datetime:[2012-12-31T12:30 2012-12-31T12:35+03]
    decimal:[10$ 1000.35$ -1.25E+6$] float:[3.1428 1.5e-17] int:[0 -1 17] multiline_string:"one
    two
    three" string:"abc абв 中文本" time:[12:30:34 12:35:12.000120 12:35+03]}
    complex_values{anonymous{dict:{one:1 three:3 two:2} list:["one" "two" "three"]
    tuple:("nodes" "edges")} named{element:node{id:1 node{class:"A" id:2} node{class:"B" id:3}}
    instance:row{12 2003-12-01 12:00 D:"W" R:0.5 T:12.1 W:5} mapping:rgb{blue:64 green:32 red:16}
    sequence:primes{2 3 5 7 11 13 17 19 23 29 31}}}}
    </pre></td></tr>
    </table>                    


Python pyaxon library
---------------------

`pyaxon <https://pypi.python.org/pypi/pyaxon>`_ is an `MIT Licensed <http://opensource.org/licenses/MIT>`_
`python <http://www.python.org>`_ library for ``AXON``.

There are introductory `IPython` notebooks:

* `Tutorial <notebooks/axon_tutorial.html>`_
* `Examples <notebooks/axon_examples.html>`_
* `Patterns <notebooks/axon_patterns.html>`_
* `Syntax <notebooks/axon_syntax.html>`_
* `What & Why <notebooks/axon_what.html>`_
* `Benchmarks <notebooks/axon_bench.html>`_

Repository for ``AXON`` and ``pyaxon`` is `here <https://bitbucket.org/intellimath/pyaxon>`_.
Here is also `mirror <https://github.com/intellimath/pyaxon>`_.

API Reference
-------------

.. toctree::
   :maxdepth: 2

   api

.. raw:: html

    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-42353741-1', 'bitbucket.org');
      ga('send', 'pageview');

    </script>
