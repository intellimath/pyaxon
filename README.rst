======
PYAXON
======

``pyaxon`` is an `MIT Licensed <http://opensource.org/licenses/MIT>`_ python library
for `AXON <http://intellimath.bitbucket.org/axon>`_. 
AXON is eXtended Object Notation. It's a simple text based format for interchanging
objects, documents and data.
It tries to combine the best of `JSON <http://www.json.org>`_,
`XML <http://www.w3.org/XML/>`_ and `YAML <http://www.yaml.org>`_.

links
-----

* Main repository for ``pyaxon`` is on `bitbucket <https://bitbucket.org/intellimath/pyaxon>`_.
* Mirror on `github <https://github.com/intellimath/pyaxon>`_
* `Blog <http://intellimath.bitbucket.org/blog/categories/axon.html>`_ about AXON.
* History of `changes <http://intellimath.bitbucket.org/axon/changelog.html>`_.

Installation
------------

``pyaxon`` runs under Python 2.7, 3.3, 3.4 and 3.5

It can be installed via pip::

	pip install pyaxon
	
It can be installed from sources::

	python setup.py install

Quick start
-----------

First import `axon` module::

	>>> import axon

Load and dump lists, dicts, tuples::

	>>> from decimal import Decimal
	>>> from datetime import datetime, time, date
	>>> text = axon.dumps([['abc абв', 1, 3.14, True],
	[datetime.now(), Decimal('3.14')]])
	>>> print(text)
	["abc абв" 1 3.14 true]
	[^2015-05-12T13:08:37.078189 3.14D]
	
	>>> vals = [{'id':1, 'nickname':'nick', 'time':time(12, 31, 34), 'text':'hello!'},
	{'id':2, 'nickname':'mark', 'time':time(12, 32, 3), 'text':'hi!'}]
	>>> text = axon.dumps(vals)
	>>> print(text)
	{id:1 nickname:"nick" text:"hello!" time:^12:31:34}
	{id:2 nickname:"mark" text:"hi!" time:^12:32:03}	
	>>> text = axon.dumps(vals, pretty=1)
	>>> print(text)
	{ id: 1
	  nickname: "nick"
	  text: "hello!"
	  time: ^12:31:34}
	{ id: 2
	  nickname: "mark"
	  text: "hi!"
	  time: ^12:32:03}
	>>> vals == axon.loads(text)
	True
	  
	>>> vals = [[{'a':1, 'b':2, 'c':3}, {'a':[1,2,3], 'b':(1,2,3), 'c':{1,2,3}}]]
	>>> text = axon.dumps(vals)
	>>> print(text)
	[{a:1 b:2 c:3} {a:[1 2 3] b:(1 2 3) c:{1 2 3}}]
	>>> text = axon.dumps(vals, pretty=1)
	>>> print(text)
	[ { a: 1
	    b: 2
	    c: 3}
	  { a: [1 2 3]
	    b: (1 2 3)
	    c: {1 2 3}}]
	>>> vals == axon.loads(text)
	True

Dump, load objects in "safe" mode::
	
    >>> vals = axon.loads('person{name:"nick" age:32 email:"nail@example.com"}')
    >>> print(type(vals[0]))
    <class 'axon._objects.Node'>
    >>> print(vals[0])
    node('person', {'email': 'nail@example.com', 'age': 32, 'name': 'nick'})

    >>> text = axon.dumps(vals)
    >>> print(text)
    person{age:32 email:"nail@example.com" name:"nick"}
    >>> text = axon.dumps(vals, pretty=1)
    >>> print(text)
    person
      age: 32
      email: "nail@example.com"
      name: "nick"
    >>> text = axon.dumps(vals, pretty=1, braces=1)
    >>> print(text)
    person {
      age: 32
      email: "nail@example.com"
      name: "nick"}

Dump, load objects in unsafe mode::

	class Person:
	    def __init__(self, name, age, email):
	        self.name = name
	        self.age = age
	        self.email = email
        
	    def __str__(self):
	        return "Person(name=%r, age=%r, email=%r)" % (self.name, self.age, self.email)

	@axon.reduce(Person)
	def reduce_Person(p):
	    return axon.node('person', {'name':p.name, 'age':p.age, 'email': p.email})

	@axon.factory('person')
	def factory_Person(attrs, vals):
	    return Person(name=attrs['name'], age=attrs['age'], email=attrs['email'])
	
	>>> p = Person('nick', 32, 'mail@example.com')
	>>> text = axon.dumps([p])
	>>> print(text)
	person{age:32 email:"mail@example.com" name:"nick"}
	>>> val = axon.loads(text, mode='strict')[0]
	>>> print(val)
	Person(name='nick', age=32, email='mail@example.com')
	
Features
--------

1. Provide simple API for loading and dumping of objects in textual AXON format.
2. Provide safe loading and dumping by default.
3. Provide unsafe loading and dumping of objects on the base of registration of factory/reduce callables.
4. Provide a way for fully controlled by application/framework/library unsafe loading and dumping.
5. It's sufficiently fast so as to be useful.
