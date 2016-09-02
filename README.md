formula
=======

Formula is a simple arithmetic expression evaluator written in Python.
The main goal of this library is to provide a safer way to evaluate
basic math expressions given in a string form.

Internally, it implements a (simplified) version of Dijkstra's "shunting-
yard algorithm".

Features
--------

* Support basic operators:

    * add (`+`), subtract (`-`), multiply (`*`), divide (`/`)
    * ... and parenthesis `()` for denoting precedence.

* Support "variables" (see 'How to use' below)
* NOT support unary operators.
* Support both Python 2.7 and Python 3.3 (or later)

How to install
--------------

Clone the repository and run setup.py:

    $ git clone https://github.com/xica/formula
    $ cd formula
    $ python setup.py install

Or you can install this library using pip:

    $ pip install git+https://github.com/xica/formula

How to use
----------

Here is a simple example how to use it:

```python
>>> from formula import Formula
>>> Formula('7 * 2.5').safe_eval()
17.5
>>> Formula('(5 + 10) / 3').safe_eval()
5.0
>>> Formula('1 / 0').safe_eval()
nan
```

Also, we can embed variables using `namespace` parameter:

```python
>>> formula = Formula('mile * 1.609')
>>> formula.safe_eval(namespace={'mile': 3})
4.827
>>> formula = Formula('(x2-x1)/t')
>>> formula.safe_eval({'x1': 1, 'x2': 5, 't': 3})
1.3333333333333333
```

Why we developed this library
-----------------------------

This library was originally developed to provide a "custom index"
feature.

Suppose you're developing a business intelligence application, and your
customer feeds a tabular data like this:

```python
>>> dataset
{'2015-06-01': {'price': 100, 'quantity': 200},
 '2015-06-02': {'price': 150, 'quantity': 300},
 '2015-06-03': {'price': 200, 'quantity': 400}}
```

Now it is a trivial task to display these values as a table, but often
customers want more. For example, they might think it is very helpful if
'unit price' is calculated automatically and displayed in the table.
Of course, you can implement a some special logic for this case ...
then you find yourself in a whack-a-mole situation. This approach
does not scale well.

Instead, you can allow customers to 'compose' a custom index through an
input dialog like this:

```
Add a custome column to the table?

  title:   [UnitPrice       ]
  formula: [price / quantity]

[OK] [CANCEL]
```

Then you can use the `formula` library to evaluate them:

```python
>>> from formula import Formula
>>> fm = Formula(expr)
>>> for date, values in dataset.items():
...   values[title] = fm.safe_eval(values)
```


LICENSE
-------

MIT License

TODO
----

* Support unary minus for negative numbers.
