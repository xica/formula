formula
=======

Formula is a simple arithmetic expression evaluator written in Python.
The main goal of this library is to provide a safe way to evaluate
basic math expressions given in string form.

Features
--------

* Support basic operators:

    * add (`+`), subtract (`-`), multiply (`*`), divide (`/`)
    * ... and parenthesis `()` for denoting precedence.

* Support "variables" (see 'How to use' below)
* Support both Python 2.7 and Python 3.3 (or later)
* NOT support unary operators.

How to install
--------------

Clone the repository and run setup.py:

    $ git clone https://github.com/xica/formula
    $ cd formula
    $ python setup.py install

How to use
----------

Just pass a string to evaluate to the `safe_eval()` function:

```python
>>> import formula
>>> formula.safe_eval('7 * 2.5')
17.5
>>> formula.safe_eval('(5 + 10) / 3')
5.0
>>> formula.safe_eval('1 / 0')
nan
```

Also we can embed variables using `namespace` parameter:

```python
>>> formula.safe_eval('mile * 1.609', namespace={'mile': 3})
4.827
>>> formula.safe_eval('(x2-x1)/t', {'x1': 1, 'x2': 5, 't': 3})
1.3333333333333333
```

TODO
----

* Support more operators (like exponents "^").
* Support unary minus for negative numbers.
* Memoize `_tokenize()` and `_parse()`
