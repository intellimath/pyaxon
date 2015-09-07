
..
    =================================
    AXON is eXtended Object Notation
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

AXON is eXtended Object Notation (``AXON``). It's a simple text based format
for interchanging of objects, documents and data.
There is `railroad diagram <http://intellimath.bitbucket.org/axon/ebnf/index.html>`_ 
in order to describe `AXON`.

It tries to combine the best of `JSON <http://www.json.org>`_,
`XML <http://www.w3.org/XML/>`_ and `YAML <http://www.yaml.org>`_.

``AXON`` is designed as text based language for data exchange in first place.

It combines in itself:

* **simplicity** of ``JSON``, 

* **extensibility** of ``XML`` and 

* **readability** of ``YAML``.

Creation of ``AXON`` had following objectives:

* Overcoming lack of support of date/time, decimal and binary data in ``JSON``.

* Overcoming inability to represent in ``JSON`` complex data
  with cross-references natively.

* Extension of ``JSON`` for native support of named/taged data structures
  (typed complex data, elements of documents etc.) in order to act in
  cases where ``XML`` is more suitable than ``JSON``.
  
* Support both ``JSON``-style and ``YAML``-style of formatting ``AXON`` messages.

* Removing ``','`` as mandatory character-separator for items in containers.

* Saving relative simplicity of the language compared to ``JSON``.

``AXON`` is designed as text based format that has compact form and
formatted form in both `JSON/C` and `YAML/Python` style for ease of developers.

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
    [1 3.14 3.25D ∞ -∞ ?]
    </pre></td></tr>

    <tr><td>tuple</td><td>( <b>V</b> … <b>V</b> )</td>
    <td><pre>
    (true 12:00 2001-12-31 2001-12-31T12:00)
    </pre></td></tr>

    <tr><td>dict</td><td>{ <b>K</b>:<b>V</b> … <b>K</b>:<b>V</b> }</td>
    <td><pre>
    {alpha:1 beta:2 gamma:3 "other chars":4}
    </pre></td></tr>

    <tr><td>ordered dict</td><td>[ <b>K</b>:<b>V</b> … <b>K</b>:<b>V</b> ]</td>
    <td><pre>
    [alpha:1 beta:2 gamma:3 "other chars":4]
    </pre></td></tr>
   
    <tr><td>node</td><td><b>N</b> { <b>N</b>:<b>V</b> … <b>N</b>:<b>V</b> <b>V</b> … <b>V</b> }</td>
    <td><pre>
    greek {alpha:123 beta:212 gamma:322}
    primes {2 3 5 7 11 13 17 19 23}
    tree {id:1 leaf{id:2 "AAA"} leaf{id:3 "BBB"}}
    </pre></td></tr>
    </table>

where **N** denotes a *name*, **K** denotes a *key*, **V** denotes a *value*.

Here is an example of ``AXON`` message:

.. raw:: html

    <table>
    <tr><th>statement form</th><th>formatted expression form</th></tr>
    <tr>
    <td><pre>
	axon
	  name: "AXON is eXtended Object Notation"
	  short_name: "AXON"
	  python_library: "pyaxon"
	  atomic_values
	    int: [0 -1 17]
	    float: [3.1428 1.5e-17]
	    decimal: [10D 1000.35D -1.25E+6D]
	    bool: [true false]
	    string: "abc абв 中文本"
	    multiline_string: "one
	two
	three"
	    date: 2012-12-31
	    time: [12:30:34 12:35:12.000120 12:35+03]
	    datetime: [2012-12-31T12:30 2012-12-31T12:35+03]
	    binary: |QVhPTiBpcyBlWHRlbmRlZCBPYmplY3QgTm90YXRpb24=

	complex_values
	    list: ["one" "two" "three"]
	    dict: {
	      one: 1
	      three: 3
	      two: 2}
	    odered_dict: [
	      one: 1
	      three: 3
	      two: 2]
	    tuple: ("nodes" "edges")
	    node: person
	      name: "Alex"
	      age: 32
    </pre></td>
    <td><pre>
	axon {
	  name: "AXON is eXtended Object Notation"
	  short_name: "AXON"
	  python_library: "pyaxon"
	  atomic_values {
	    int: [0 -1 17]
	    float: [3.1428 1.5e-17]
	    decimal: [10D 1000.35D -1.25E+6D]
	    bool: [true false]
	    string: "abc абв 中文本"
	    multiline_string: "one
	two
	three"
	    date: 2012-12-31
	    time: [12:30:34 12:35:12.000120 12:35+03]
	    datetime: [2012-12-31T12:30 2012-12-31T12:35+03]
	    binary: |QVhPTiBpcyBlWHRlbmRlZCBPYmplY3QgTm90YXRpb24=
	}
	complex_values {
	    list: ["one" "two" "three"]
	    dict: {
	      one: 1
	      three: 3
	      two: 2}
	    odered_dict: [
	      one: 1
	      three: 3
	      two: 2]
	    tuple: ("nodes" "edges")
	    node: person {
	      name: "Alex"
	      age: 32}}}
    </pre></td>
    </tr>
    <tr><th colspan=2>compact expression form</th></tr>
    <tr><td colspan=2><pre>
	axon{name:"AXON is eXtended Object Notation" short_name:"AXON" python_library:"pyaxon"
	atomic_values{int:[0 -1 17] float:[3.1428 1.5e-17] decimal:[10D 1000.35D -1.25E+6D] 
	bool:[true false] string:"abc абв 中文本" multiline_string:"one
	two
	three" date:2012-12-31 time:[12:30:34 12:35:12.000120 12:35+03]
	datetime:[2012-12-31T12:30 2012-12-31T12:35+03]
	binary:|QVhPTiBpcyBlWHRlbmRlZCBPYmplY3QgTm90YXRpb24=
	} complex_values{list:["one" "two" "three"] dict:{one:1 three:3 two:2}
	odered_dict:[one:1 two:2 three:3] tuple:("nodes" "edges") node:person{name:"Alex" age:32}}}
    </pre></td></tr>
    </table>                    



Python pyaxon library
---------------------

`pyaxon <https://pypi.python.org/pypi/pyaxon>`_ is an `MIT Licensed <http://opensource.org/licenses/MIT>`_
`python <http://www.python.org>`_ library for ``AXON``.

There are some `IPython` `notebooks <https://bitbucket.org/intellimath/pyaxon/src/default/examples>`_.

`Repository <https://bitbucket.org/intellimath/pyaxon>`_ for ``AXON`` and ``pyaxon``.
Mirror on `github <https://github.com/intellimath/pyaxon>`_.

`Blog <http://intellimath.bitbucket.org/blog/categories/axon.html>`_ about AXON.

History of `changes <http://intellimath.bitbucket.org/axon/changelog.html>`_.

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
