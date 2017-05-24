#############################################################################
# The overall intent of this module is to evaluate mathematical expressions
# input as strings. This file provides a naming convention for functions as
# well as providing a location for adding any specialized functions required
# for specific applications.
#############################################################################
import math
import collections
import re
# import fractions


binary_operators = ['^', '*', '/', '+', '-']

# In order for a function to be evaluated in the parser, it needs to be
# in the following list and the equivalent python function also needs to 
# be defined. All entries in the list should be in ALL CAPS and functions
# should be named with the preffix 'func_'.
# E.g. sine is SIN in the list and the function func_sin needs to be defined.

func_text = ["ABS", "CEIL", "FLOOR", "MIN", "MAX", "MOD", "RTX", "ROUND",
             "SQRT", "TRUNC", "SIN", "COS", "TAN", "ARCSIN", "ARCCOS",
             "ARCTAN", "EXP", "LN", "LOG", "LOGX"]

# , "PERM", "COMB"]

func_mapper = {x: 'func_' + x.lower() for x in func_text}
sorted_func = sorted(func_text, key=len, reverse=True)

Token = collections.namedtuple('Token', ['typ', 'value', 'start', 'stop'])

token_specification = [
    ('NEGNUM', r'^(\-\d+\.?\d*)'),  # Negative integer or decimal number
    ('NUMBER', r'\d+\.?\d*'),       # Integer or decimal number
    ('PI', r'PI'),                  # PI
    ('FUNC', r'`+'),                # Functions
    ('OP', r'[+\-*/\^]'),           # Arithmetic operators
    ('PARENS', r'\(_+\)'),          # Parenthetical terms
    ('OTHER', r'[A-Za-z]+'),        # Any other words
    ('LRP', r'[\(\)]'),             # Any parentheses
    ('MISMATCH', r'.'),             # Any other character
]

comma_re = re.compile(r'(\d)\,(\d\d\d)')
mult_re = re.compile(r'(\d)(\()|(\d)([a-zA-Z])')

tok_reg = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
token_re = re.compile(tok_reg)


def func_abs(x):
    return abs(x)


def func_ceil(a):
    return math.ceil(a)


def func_floor(a):
    return math.floor(a)


def func_min(a):
    return min(a)


def func_max(a):
    return max(a)


def func_mod(a, b):
    return a % b


def func_rtx(n, x):
    return x ** (1 / n)


def func_sqrt(x):
    return math.sqrt(x)


def func_sin(x):
    sin = math.sin(x)
    if abs(sin) < 10 ** -7:
        return 0
    return sin


def func_cos(x):
    cos = math.cos(x)
    if abs(cos) < 10 ** -7:
        return 0
    return cos


def func_tan(x):
    return math.tan(x)


def func_arcsin(x):
    return math.asin(x)


def func_arccos(x):
    return math.acos(x)


def func_arctan(x):
    return math.atan(x)


def func_exp(x):
    return math.exp(x)


def func_ln(x):
    return math.log(x)


def func_log(x):
    return math.log10(x)


def func_logx(n, x):
    return math.log(x, n)


def func_round(n, x):
    return n


def func_trunc(n, x):
    return n


if __name__ == '__main__':
    print(func_mapper)
