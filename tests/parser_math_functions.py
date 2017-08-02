"""
The overall intent of this package is to evaluate mathematical expressions
input as strings. This module provides a naming convention for functions as
well as a location for adding any functions required for specific applications.
"""

import math


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


"""
In order for a function to be evaluated in the parser, it needs to be in
the following list and the equivalent python function also needs to be
defined. All entries in the list should be in ALL CAPS and functions
should be named with the preffix 'func_'.

E.g. sine is SIN in the list and the function func_sin needs to be defined.
"""

func_text = ["ABS", "CEIL", "FLOOR", "MIN", "MAX", "MOD", "RTX", "ROUND",
             "SQRT", "TRUNC", "SIN", "COS", "TAN", "ARCSIN", "ARCCOS",
             "ARCTAN", "EXP", "LN", "LOG", "LOGX"]

"""
Functions I may need to make:
    nCr:   combinations,
    nPr:   permutations,
    n!:    factorial

"""

func_mapper = {"ABS": func_abs, "CEIL": func_ceil, "FLOOR": func_floor,
               "MIN": func_min, "MAX": func_max, "MOD": func_mod,
               "RTX": func_rtx, "ROUND": func_round, "SQRT": func_sqrt,
               "TRUNC": func_trunc, "SIN": func_sin, "COS": func_cos,
               "TAN": func_tan, "ARCSIN": func_arcsin, "ARCCOS": func_arccos,
               "ARCTAN": func_arctan, "EXP": func_exp, "LN": func_ln,
               "LOG": func_log, "LOGX": func_logx
               }

func_mult_arg = ["MIN", "MAX", "MOD", "RTX", "ROUND", "LOGX", "TRUNC"]

sorted_func = sorted(func_text, key=len, reverse=True)
