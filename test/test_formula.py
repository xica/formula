# -*- coding: utf-8 -*-

import math
import unittest

from formula import Formula


class TestFormula(unittest.TestCase):

    def test_tokenize(self):
        data = [
            ('A',  ('A',)),
            ('A + B * C',  ('A', '+', 'B', '*', 'C')),
            ('A+B*C',      ('A', '+', 'B', '*', 'C')),
            ('(r*r)*3.14',  ('(', 'r', '*', 'r', ')', '*', '3.14')),
            ('((A+1)-B)',  ('(', '(',  'A', '+', '1', ')', '-', 'B', ')')),
        ]
        for string, result in data:
            self.assertEqual(Formula.tokenize(string), result)

    def test_parse(self):
        data = [
            (('A',), ('A',)),
            (('A', '+', 'B', '*', 'C'), ('A', 'B', 'C', '*', '+')),
            (('A', '/', 'B', '*', 'C'), ('A', 'B', '/', 'C', '*')),
            (('A', '*', 'B', '+', 'C'), ('A', 'B', '*', 'C', '+')),
            (('A', '*', '(', 'B', '+', 'C', ')'), ('A', 'B', 'C', '+', '*')),
            (('(', 'A', '-', 'B', ')', '+', 'C'), ('A', 'B', '-', 'C', '+')),
            (('10', '/', '(', '1.0', '-', '0.5', ')'), ('10', '1.0', '0.5', '-', '/'))
        ]
        for tokens, result in data:
            self.assertEqual(Formula.parse(tokens), result)

    def test_safe_eval(self):
        data = [
            ('A', {'A': 1}, 1),
            ('A + B * C', {'A': 1, 'B': 2, 'C': 3}, 7),
            ('A / B * C', {'A': 1, 'B': 2, 'C': 3}, 1.5),
            ('A * B + C', {'A': 1, 'B': 2, 'C': 3}, 5),
            ('A * (B + C)', {'A': 1, 'B': 2, 'C': 3}, 5),
            ('A * A * 3.141592', {'A': 2}, 12.566368),
            ('100 / ( 1.0 - 0.5 )', None, 200.0)
        ]
        for expr, namespace, result in data:
            formula = Formula(expr)
            self.assertEqual(formula.safe_eval(namespace), result)

        # Test for division by zero
        self.assertTrue(math.isnan(Formula('1 / 0').safe_eval()))

        # Invalid expressions
        with self.assertRaises(ValueError):
            Formula('A + 3').safe_eval(None)

        with self.assertRaises(ValueError):
            Formula('B A + 3').safe_eval({'A': 1, 'B': 2})
