
import re
# import os
# from pprint import pprint
import operator
import fractions as frac
import numpy as np
from parser_functions import *

# ### Evaluation functions


def decimal_place_counter(number):
    """Given a number, finds the number of decimal places and
    returns an integer.
    """
    num_str = str(number)
    if num_str.count('.') == 0:
        return 0
    else:
        return len(num_str) - 1 - num_str.index('.')


def eval_bin_expr(num_1, num_2, bin_op):
    """Given LHS of  num_1 _ num_2 = c returns c with the appropriate
    number of digits in an effort to avoid floating point error
    """

    if bin_op == '/':
        if isinstance(num_1, int) and isinstance(num_2, int):
            return frac.Fraction(num_1, num_2)
        return num_1 / num_2

    num_3 = BIN_OP_DICT[bin_op](num_1, num_2)

    num_1_places = decimal_place_counter(num_1)
    num_2_places = decimal_place_counter(num_2)
    num_3_places = decimal_place_counter(num_3)

    if bin_op == '*':
        r_places = num_1_places * num_2_places
    else:
        r_places = max(num_1_places, num_2_places)

    if num_3_places <= r_places:
        return num_3
    else:
        str_num_3 = str(num_3)
        new_num_3 = str_num_3[:len(str_num_3) - r_places]

    if new_num_3.count('.') == 1:
        return float(new_num_3)
    else:
        return int(new_num_3)


BIN_OP_DICT = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
}


def eval_a_op_b(terms, op):
    '''performs the first calculation according to the order
    of operations in the terms'''
    test_string = str(terms)

    if op == 'md':
        bin_op = mul_div_re.search(test_string).group(0)
    else:
        bin_op = add_sub_re.search(test_string).group(0)

    index_1 = terms.index(bin_op)
    num_1, num_2 = terms[index_1 - 1], terms[index_1 + 1]
    terms[index_1 - 1] = eval_bin_expr(num_1, num_2, bin_op)

    del terms[index_1: index_1 + 2]

    return terms


def first_index(terms, op_1, op_2):
    '''determines'''
    if terms.count(op_1) != 0:
        i_1 = terms.index(op_1)
    else:
        return terms.index(op_2)

    if terms.count(op_2) == 0:
        return i_1
    else:
        return min(i_1, terms.index(op_2))


def eval_expon(terms):
    # print(terms)
    expr_terms = [x for x in terms]
    i = expr_terms.index('^')
    if expr_terms[i + 1] == '-':
        expr_terms[i + 1] = -1 * expr_terms[i + 2]
        del expr_terms[i + 2]

    expr_terms[i - 1] = expr_terms[i - 1] ** expr_terms[i + 1]

    del expr_terms[i: i + 2]

    return expr_terms


mul_div_re = re.compile(r'([\*\/])')
add_sub_re = re.compile(r'([\-\+])')


def evaluate_terms(terms):
    expr_terms = [x for x in terms]

    while expr_terms.count('^') != 0:
        expr_terms = eval_expon(expr_terms)

    while expr_terms.count('*') + expr_terms.count('/') != 0:
        expr_terms = eval_a_op_b(expr_terms, 'md')

    while expr_terms.count('+') + expr_terms.count('-') != 0:
        expr_terms = eval_a_op_b(expr_terms, 'pm')

    return expr_terms[0]


def eval_ready(array):
    string = str(array)
    return 'FUNC' not in string and 'PAREN' not in string


# EXP1 = '5+sin(4*6(3-5))'

# print(bin_op_re.search(EXP1))

print(eval_a_op_b([1, '*', 3], 'md'))

# if __name__ == '__main__':
#     EXP1 = '5+sin(4*6(3-5))'
#     disp_ans(EXP1)

#     EXP2 = '5+sin(-4)'
#     disp_ans(EXP2)

#     EXP3 = '4*6(3-5)'
#     disp_ans(EXP3)

#     EXP4 = '8 - 2(2)(3)'
#     disp_ans(EXP4)

#     EXP5 = '8 - 2*2*3'
#     disp_ans(EXP5)

#     EXPW = '7 + 3 + 1 + 3 + 5 + 3 + 1 +3 '
    # disp_ans(EXPW)
    # neg_base = '-3^0.5'
    # disp_ans(neg_base)

    # neg_base2 = '8-3^2'
    # disp_ans(neg_base2)