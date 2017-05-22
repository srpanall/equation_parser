#############################################################################
# The overall intent of this module is to evaluate mathematical expressions
# input as strings. This file provides a naming convention for functions as
# well as providing a location for adding any specialized functions required
# for specific applications.
#############################################################################
import math
import collections
import fractions
import prime_factorization as pr_fac

# Function for GSF and GSFR


def simplify_radical(n):
    primes_in_square = pr_fac.factor_n(n)
    g_s_f = 1

    for p, a in primes_in_square.items():
        g_s_f = g_s_f * p ** (a // 2)

    return [g_s_f, n // (g_s_f ** 2)]


def func_abs(x):
    return abs(x)


def func_div(a, b):
    return a // b


def func_ceil(a):
    return math.ceil(a)


def func_floor(a):
    return math.floor(a)


def func_gcf(a, b):
    return fractions.gcd(a, b)


def func_lcm(a, b):
    return (a * b) // fractions.gcd(a, b)


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


def func_gcs(x):
    return simplify_radical(x)[0]


def func_gcsr(x):
    return simplify_radical(x)[1]


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

# Needed lists and dictionaries


binary_operators = ['^', '*', '/', '+', '-']

func_text = ["ABS", "DIV", "CEIL", "FLOOR", "GCF", "LCM", "MIN", "MAX",
             "MOD", "RTX", "ROUND", "SQRT", "TRUNC", "GCS", "GCSR", "SIN",
             "COS", "TAN", "ARCSIN", "ARCCOS", "ARCTAN", "EXP", "LN", "LOG",
             "LOGX"]
# , "PERM", "COMB"]

# Add all functions in dict_funct before it can be used

dict_func = [func_abs, func_div, func_ceil, func_floor, func_gcf, func_lcm,
             func_min, func_max, func_mod, func_rtx, func_round, func_sqrt,
             func_trunc, func_gcs, func_gcsr, func_sin, func_cos, func_tan,
             func_arcsin, func_arccos, func_arctan, func_exp, func_ln,
             func_log, func_logx]

# , func_perm, func_comb]


func_mapper = {x: y for x, y in zip(func_text, dict_func)}
sorted_func = sorted(func_text, key=len, reverse=True)

Token = collections.namedtuple('Token', ['typ', 'value', 'start',
                                         'stop'])
if __name__ == '__main__':
    print(simplify_radical(300))
