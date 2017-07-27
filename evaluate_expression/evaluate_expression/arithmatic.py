"""
The overall intent of this package is to evaluate mathematical expressions
input as strings. This module collects the functions used to evaluate an
expression given as a list of numbers and binary operation using the order
of operations and ultimately returns a list containing a single numeric entry.
"""

import re
import operator


# Constants

BIN_OP_DICT = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# Regular expressions used in module

MUL_DIV_RE = re.compile(r'([\*\/])')


def eval_a_op_b(terms, op_type):
    """Performs the first calculation in the expression based on the order
    of operations and returns an updated list of terms.
    """
    # print(terms)
    test_string = str(terms)

    if op_type == 'md':
        bin_op = MUL_DIV_RE.search(test_string).group(0)
        index_1 = terms.index(bin_op)
    else:
        bin_op = terms[1]
        index_1 = 1

    num_1, num_2 = terms[index_1 - 1], terms[index_1 + 1]
    terms[index_1 - 1] = BIN_OP_DICT[bin_op](num_1, num_2)

    del terms[index_1: index_1 + 2]

    return terms


def eval_expon(terms):
    """Evaluates the first exponential expression in the expression and returns
    an updated list of terms.
    """
    pow_dex = terms.index('^')
    if terms[pow_dex + 1] == '-':
        terms[pow_dex + 1] = -1 * terms[pow_dex + 2]
        del terms[pow_dex + 2]

    terms[pow_dex - 1] = terms[pow_dex - 1] ** terms[pow_dex + 1]

    del terms[pow_dex: pow_dex + 2]

    return terms


def evaluate_terms(terms):
    """Evaluates an expression given as a list of numbers and operations
    following the order of operations and returns a numeric value.
    """
    expr_terms = [x for x in terms]

    while expr_terms.count('^') != 0:
        expr_terms = eval_expon(expr_terms)

    while MUL_DIV_RE.search(str(expr_terms)) is not None:
        expr_terms = eval_a_op_b(expr_terms, 'md')

    while len(expr_terms) != 1:
        expr_terms = eval_a_op_b(expr_terms, 'pm')

    return expr_terms[0]
