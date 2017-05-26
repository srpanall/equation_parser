#############################################################################
# The overall intent of this module is to evaluate mathematical expressions
# input as strings. This file provides a naming convention for functions as
# well as providing a location for adding any specialized functions required
# for specific applications.
#############################################################################
import math
import collections
import re
from itertools import product
# import fractions
# from pprint import pprint




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


binary_operators = ['^', '*', '/', '+', '-']

# In order for a function to be evaluated in the parser, it needs to be
# in the following list and the equivalent python function also needs to
# be defined. All entries in the list should be in ALL CAPS and functions
# should be named with the preffix 'func_'.
# E.g. sine is SIN in the list and the function func_sin needs to be defined.

func_text = ["ABS", "CEIL", "FLOOR", "MIN", "MAX", "MOD", "RTX", "ROUND",
             "SQRT", "TRUNC", "SIN", "COS", "TAN", "ARCSIN", "ARCCOS",
             "ARCTAN", "EXP", "LN", "LOG", "LOGX"]

# Functions I may need to make nCr, nPr, n!
# combinations, permutations, factorial

func_mapper = {x: 'func_' + x.lower() for x in func_text}

func_mapper = {"ABS": func_abs, "CEIL": func_ceil, "FLOOR": func_floor,
               "MIN": func_min, "MAX": func_max, "MOD": func_mod,
               "RTX": func_rtx, "ROUND": func_round, "SQRT": func_sqrt,
               "TRUNC": func_trunc, "SIN": func_sin, "COS": func_cos,
               "TAN": func_tan, "ARCSIN": func_arcsin, "ARCCOS": func_arccos,
               "ARCTAN": func_arctan, "EXP": func_exp, "LN": func_ln,
               "LOG": func_log, "LOGX": func_logx
               }


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

# complex_re_2 = re.compile(r'[-+]?(\d+(\.\d*)?|\.\d+)')


complex_strings = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
                   '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)']

# 5/25/17
# 16+1.7320508075688772j ['16+1.7320508075688772j']
# 16 + 1.7320508075688772 j ['16+1.7320508075688772j']
# 7-12i ['7-12j']
# 14+2i ['14+2j']
# win no complex numbers
# (7-12i)*(14+2i) ['7-12j', '14+2j']


comp_test_re = re.compile(r'\d[ij]', flags=re.I)

comp_coeff = [r'\d+', r'\d+\.\d*', r'']

comp_reg_list = [x + r'[+-]' + y + r'[ij]'
                 if x != ''
                 else
                 y + r'[ij]'
                 for x, y
                 in product(comp_coeff, repeat=2)
                 ]

c_r_l_n = comp_reg_list.index(r'[ij]')

comp_reg_list[c_r_l_n] = r'[^a-zA-z]' + comp_reg_list[c_r_l_n]

comp_reg = '|'.join(comp_reg_list)

comp_re = re.compile(comp_reg, flags=re.I)

comp_reg_list2 = ['(' + x + r'[+-]' + y + r'[ij])'
                  if x != ''
                  else
                  '(' + y + r'[ij])'
                  for x, y
                  in product(comp_coeff, repeat=2)
                  ]

c_r_l_n2 = comp_reg_list2.index(r'([ij])')

comp_reg_list2[c_r_l_n] = r'([^a-zA-z][ij])'

comp_reg2 = '|'.join(comp_reg_list2)

comp_re2 = re.compile(comp_reg2, flags=re.I)


def find_complex(expr):
    expr_out = expr.replace(' ', '')
    # expr_out = expr_out.upper()
    # test = complex_test_re.search(expr_out) is None
    # print(expr_out, test)
    if comp_test_re.search(expr_out) is None:
        print(expr, 'no complex numbers')
    else:
        # print(expr)
        comp_num = comp_re.findall(expr_out)
        # print(type(comp_num))
        comp_num = [re.sub(r'[iIJ]', 'j', x) for x in comp_num]
        print(expr, comp_num)


def replace_complex(expr):
    expr_out = expr.replace(' ', '')
    if comp_test_re.search(expr_out) is None:
        print(expr, 'no complex numbers')
    else:
        terms = [x for x in comp_re2.split(expr_out)
                 if x is not None and x != ''
                 ]
        upd_terms = [x if comp_test_re.search(x) is None else
                     '(' + re.sub(r'[ijIJ]', 'j', x) + ')' for x in terms
                     ]
        expr_out = ''.join(upd_terms)

        print(expr, expr_out)


if __name__ == '__main__':
    # print(func_mapper)
    for text in complex_strings:
        # find_complex(text)
        replace_complex(text)
