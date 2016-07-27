# -*- coding: utf-8 -*-

import math
import unittest

from formula import _tokenize, _parse, safe_eval


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
            self.assertEqual(_tokenize(string), result)

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
            self.assertEqual(_parse(tokens), result)

    def test_safe_eval(self):
        data = [
            (('A', {'A': 1}), 1),
            (('A + B * C', {'A': 1, 'B': 2, 'C': 3}), 7),
            (('A / B * C', {'A': 1, 'B': 2, 'C': 3}), 1.5),
            (('A * B + C', {'A': 1, 'B': 2, 'C': 3}), 5),
            (('A * (B + C)', {'A': 1, 'B': 2, 'C': 3}), 5),
            (('A * A * 3.141592', {'A': 2}), 12.566368),
            (('100 / ( 1.0 - 0.5 )', None), 200.0)
        ]
        for params, result in data:
            self.assertEqual(safe_eval(*params), result)

        # Test for division by zero
        self.assertTrue(math.isnan(safe_eval('1 / 0')))

        # Invalid expressions
        with self.assertRaises(ValueError):
            safe_eval('A + 3', None)

        with self.assertRaises(ValueError):
            safe_eval('B A + 3', {'A': 1, 'B': 2})