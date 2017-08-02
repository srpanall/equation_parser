"""
The overall intent of this package is to evaluate mathematical expressions
input as strings. This module collects the functions used to tokenize and
parse the expression into a list of numbers, binary operators, functions
with arguments, and parentheses with contents.
"""

import re
import collections
import fractions as frac
import numpy as np
from parser_math_functions import sorted_func
from formatting_functions import find_all_parens


Token = collections.namedtuple('Token', ['typ', 'value', 'start', 'stop'])

TOKEN_SPECIFICATION = [
    ('NEGNUM', r'^(\-\d+\.?\d*)'),  # Negative integer or decimal number
    ('NUMBER', r'\d+\.?\d*'),       # Integer or decimal number
    ('PI', r'PI'),                  # PI
    ('FUNC', r'`+'),                # Functions
    ('OP', r'[+\-*/\^]'),           # Arithmetic operators
    ('PARENS', r'\(_+\)'),          # Parenthetical terms
    ('OTHER', r'[A-Za-z]+'),        # Any other words
    ('MISMATCH', r'.'),             # Any other character
]

TOK_REG = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
TOKEN_RE = re.compile(TOK_REG)

# Formatting functions


def id_paren(expr):
    """Replaces the contents of all sets of parentheses with underscores
    and returns a string.
    """
    expr_out = expr

    paren_loc = find_all_parens(expr)
    paren_start = sorted(paren_loc.keys())

    for start in paren_start:
        if expr_out[start] == '(':
            old = expr_out[start: paren_loc[start]]
            new = '(' + '_' * (len(old) - 2) + ')'
            expr_out = expr_out.replace(old, new, 1)

    return expr_out


def id_funct(expr):
    """Replaces all named mathematical functions and their arguments with `
    and returns a string.
    """
    expr_out = expr

    for item in sorted_func:
        while expr_out.count(item) != 0:
            match = re.search(item, expr_out, re.I)
            expr_start, expr_end = match.span()
            paren_loc = find_all_parens(expr_out)
            old = expr_out[expr_start: paren_loc[expr_end]]
            expr_out = expr_out.replace(old, '`' * len(old))

    return expr_out


def token_prep(expr):
    """Prepares expression for Tokenizer by replacing parentheses and
    contents as well as functions and their arguments with symbols and
    returns a string.
    """
    expr_out = id_paren(expr)
    expr_out = id_funct(expr_out)

    return expr_out

# Tokenizing


def tokenize(code):
    """Returns a list of named tuples containing the type of chunk, its
    content, as well as the start and end point in the function and it's
    position in the string"""
    dict_kinds = {'FUNC': '`', 'PARENS': '(_)'}

    for mobj in TOKEN_RE.finditer(code):
        kind = mobj.lastgroup

        if kind in dict_kinds:
            value = dict_kinds[kind]
        else:
            value = mobj.group(kind)

        if kind == 'MISMATCH':
            raise RuntimeError('%r unexpected in %s' % (value, code))
        elif kind == 'OTHER':
            raise RuntimeError('%r unknown text in %s' % (value, code))
        else:
            start, end = mobj.span()
            yield Token(kind, value, start, end)

# Parsing


def chunk_expr(expr):
    """Parses the expression and returns a list of numbers, binary operators,
    functions with arguments, and parenthesis with contents.
    """
    mod_expr = token_prep(expr)

    tokens = [token for token in tokenize(mod_expr)]

    chunks = [[token[0], DCHUNK[token[0]](expr, token)] for token in tokens]

    return chunks


# Chunk processing


def op_chunk(*tupe):
    """Returns the binary operator in the chunk as a string."""
    return tupe[1][1]


def num_chunk(*tupe):
    """Returnse the value of the string as a Fraction object."""
    num = tupe[1][1]
    return frac.Fraction(num)


def func_chunk(expr, tupe):
    """Returns a list of the form [mathematical function, argument]"""
    func_in = expr[tupe[2]:tupe[3]]

    func = re.match(r'[A-Za-z]+\(', func_in).group()
    func_out = func[:-1]
    x_val = func_in[len(func): -1]

    return [func_out.upper(), chunk_expr(x_val)]


def paren_chunk(expr, tupe):
    """Recursively chunks the contents of nested parentheses and returns a
    list.
    """
    expr_in = expr[tupe[2] + 1:tupe[3] - 1]

    if expr_in == 'j':
        return [1j]

    return chunk_expr(expr_in)


def pi_chunk(*tupe):
    """Returns pi as a numpi object."""
    return np.pi


# dictionary mapping chunk type to appropriate function

DCHUNK = {
    'NEGNUM': num_chunk,
    'NUMBER': num_chunk,
    'FUNC': func_chunk,
    'OP': op_chunk,
    'PARENS': paren_chunk,
    'PI': pi_chunk,
}
