# -*- coding: utf-8 -*-

import re
import operator


#
# Utils

def is_float(s):
    """Check if a number literal"""
    return re.match('^\d+(\.\d+)?$', s)


def safediv(x, y):
    """Perform "x/y" as floating point division.
    (Nan is returned if y == 0)
    """
    try:
        return operator.truediv(x, y)
    except ZeroDivisionError:
        return float('nan')

#
# Parse settings

OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': safediv,
}

PRECEDENCE = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
}

PAREN_LEFT = '('
PAREN_RIGHT = ')'
PARENS = [PAREN_LEFT, PAREN_RIGHT]

WHITESPACES = [' ']


#
# Lexical analysis / parser functions

def _tokenize(string):
    """Split `string` into tokens.

    >>> _tokenize('A / (10 - B)')
    ['A', '/', '(', '10', '-', 'B', ')']
    """
    tokens = []
    buf = ''
    for char in string:
        if char in PARENS or char in OPERATORS:
            tokens.append(buf)
            tokens.append(char)
            buf = ''
        elif char in WHITESPACES:
            tokens.append(buf)
            buf = ''
        else:
            buf += char
    return tuple(token for token in (tokens + [buf]) if token)


def _parse(tokens):
    """Convert a list of tokens to reverse Polish notation.

    >>> _parse(['A', '/', '(', '10', '-', 'B', ')'])
    ['A', '10', 'B', '-', '/']
    """
    queue = []
    stack = []
    for token in tokens:
        if token in OPERATORS:
            # Pop operators with less than or equal precedence
            # from the stack.
            while stack and stack[-1] in OPERATORS:
                if PRECEDENCE[stack[-1]] >= PRECEDENCE[token]:
                    queue.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == PAREN_LEFT:
            # Left parentheses should be always stacked up.
            stack.append(token)
        elif token == PAREN_RIGHT:
            # If the token is a right parenthesis, pop from the stack
            # until the corresponding left parenthesis is found.
            while stack:
                token = stack.pop()
                if token != PAREN_LEFT:
                    queue.append(token)
                else:
                    break
            else:
                raise ValueError('parentheses mismatch')
        else:
            # Push other tokens (number/variable) to the stack.
            queue.append(token)
    while stack:
        queue.append(stack.pop())
    return tuple(queue)


#
# Entry point

class Formula:

    def __init__(self, expr):
        self.expr = expr
        self.parsed = _parse(_tokenize(expr))

    def safe_eval(self, namespace=None):
        """Evaluate an arithmetic expression using `namespace`.

        >>> from formula import Formula
        >>> formula = Formula('(A + 1) * 100')
        >>> formula.safe_eval({'A': 5'})
        600
        """
        if namespace is None:
            namespace = {}

        stack = []
        for token in self.parsed:
            # Evaluate an expression in reverse Polish notation.
            if token in namespace:
                stack.append(namespace[token])
            elif is_float(token):
                stack.append(float(token))
            elif token in OPERATORS:
                arg2 = stack.pop()
                arg1 = stack.pop()
                stack.append(OPERATORS[token](arg1, arg2))
            else:
                raise ValueError('unknown token: %s' % token)

        if len(stack) != 1:
            raise ValueError('invalid formula: %s' % self.expr)

        return stack.pop()
