"""This module evaluates a list of numbers and binary operations and returns
a list containing a single numeric value.
"""
import re
import operator
import fractions as frac
import decimal as dec


BIN_OP_DICT = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

MUL_DIV_RE = re.compile(r'([\*\/])')
ADD_SUB_RE = re.compile(r'([\-\+])')
DEC_RE = re.compile(r'\.(\d+)')


def decimal_place_counter(number):
    """Given a number, finds the number of decimal places and
    returns an integer.
    """
    num_str = str(number)
    if num_str.count('.') == 0:
        return 0
    else:
        return len(DEC_RE.search(num_str).group(1))


def eval_bin_expr(num_1, num_2, bin_op):
    """Evaluates an expression containing 2 numbers and a binary operator
    returns a numerical value with the appropriate precision.
    """
    if bin_op == '/':
        if isinstance(num_1, int) and isinstance(num_2, int):
            return frac.Fraction(num_1, num_2)
        # dec_1 = dec.Decimal(num_1)
        return num_1 / num_2

    return BIN_OP_DICT[bin_op](num_1, num_2)
    # num_3 = BIN_OP_DICT[bin_op](num_1, num_2)

    # num_1_places = decimal_place_counter(num_1)
    # num_2_places = decimal_place_counter(num_2)
    # num_3_places = decimal_place_counter(num_3)

    # if bin_op == '*':
    #     r_places = num_1_places * num_2_places
    # else:
    #     r_places = max(num_1_places, num_2_places)

    # if num_3_places <= r_places:
    #     return num_3
    # else:
    #     str_num_3 = str(num_3)
    #     new_num_3 = str_num_3[:len(str_num_3) - r_places]

    # if new_num_3.count('.') == 1:
    #     return float(new_num_3)
    # else:
    #     return int(new_num_3)


def eval_a_op_b(terms, op_type):
    """Performs the first calculation in the expression based on the order
    of operations and returns an updated list of terms.
    """
    # print(terms)
    test_string = str(terms)

    if op_type == 'md':
        bin_op = MUL_DIV_RE.search(test_string).group(0)
    else:
        bin_op = ADD_SUB_RE.search(test_string).group(0)

    index_1 = terms.index(bin_op)
    num_1, num_2 = terms[index_1 - 1], terms[index_1 + 1]
    terms[index_1 - 1] = eval_bin_expr(num_1, num_2, bin_op)

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

    while ADD_SUB_RE.search(str(expr_terms)) is not None:
        if len(expr_terms) == 1:
            break
        expr_terms = eval_a_op_b(expr_terms, 'pm')

    return expr_terms[0]


# num = '3.1415'

# if __name__ == '__main__':
    # print(decimal_place_counter(num))
    # print(eval_a_op_b([1, '*', 3], 'md')[0])
    # print(evaluate_terms([2, '^', 4]))
