formula
=======

Formula is a simple arithmetic expression evaluator written in Python.
The main goal of this library is to provide a safer way to evaluate
basic math expressions given in string form.

Internally, it implements a (simplified) version of Dijkstra's "shunting-
yard algorithm".

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

Just pass a string to the `safe_eval()` function:

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

Implementation Background
-------------------------

This library was originally developed to provide a "custom index"
feature.

Suppose you're developing a dashboard application, and a user feeds
a tabular data like this:

```python
>>> dataset
{'2015-06-01': {'price': 100, 'quantity': 200},
 '2015-06-02': {'price': 150, 'quantity': 300},
 '2015-06-03': {'price': 200, 'quantity': 400}}
```

Now it is a trivial task to display these values as a table, but often
users want more. For example, they might think it is very helpful if
'unit price' is calculated automatically and displayed in the table.
Of course, you can implement a some special logic for this case ...
then you find yourself in a whack-a-mole situation. This approach
does not scale well for a large user base.

Instead, you can allow users to 'compose' a custom index through an
input dialog like this:

```
Add a custome column to the table?

  title:   [UnitPrice       ]
  formula: [price / quantity] (max 25 chars)

[OK] [CANCEL]
```

Then you can use the `formula` library to evaluate them:

```python
>>> import formula
>>> for date, values in dataset.items():
...   values[title] = formula.safe_eval(expression, namespace=values)
```


TODO
----

* Support unary minus for negative numbers.
* Memoize `_tokenize()` and `_parse()`
