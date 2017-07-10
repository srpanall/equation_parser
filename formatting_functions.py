
import re
# import os
# from pprint import pprint
# import operator
# import fractions as frac
# import numpy as np
from parser_functions import *

# ### Preparing the Expression

paren_re = re.compile(r'\([^\(\)]+\)')


def find_all_parens(expression):
    '''returns a list containing the location of each set of parentheses
    as [lp_pos,rp_pos]'''

    paren_info = [[paren_obj.group(), paren_obj.start(), paren_obj.end()]
                  for paren_obj in paren_re.finditer(expression)]
    exprs = [paren_list[0] for paren_list in paren_info]
    paren_loc = [[span[1], span[2]] for span in paren_info]

    # print(paren_loc)

    expr_list = list(expression)

    # print(expr_list)

    for p_start, p_end in paren_loc:
        expr_list[p_start] = '_'
        expr_list[p_end - 1] = '_'

    expression = ''.join(expr_list)

    # for item in exprs:
    #     # print(expression)
    #     expression = expression.replace(item, '_' + item[1:-1] + '_')
    #     # print(expression)

    if expression.count('(') != 0:
        paren_loc += [[p_start, p_end] for p_start, p_end in find_all_parens(expression).items()]

    return {x: y for x, y in paren_loc}


def remove_double_parens(expr):
    '''returns the expression after eliminating any double sets of
    parentheses if necessary. e.g. 3((x+y)) beomces 3(x+y)'''

    paren_loc = find_all_parens(expr)
    paren_doub = {x: y - 1 for x, y in paren_loc.items()
                  if paren_loc.get(x - 1, 0) == y + 1}
    doub_loc = list(paren_doub.keys()) + list(paren_doub.values())

    return ''.join([y for x, y in enumerate(expr) if x not in doub_loc])


def remove_doub_ops(expr):
    '''Returns the expression after replacing an operator followed by a negative
    sign with a mathematically equivalent operation'''
    ud_expr = expr
    double_ops = [('+-', '-'), ('--', '+'), ('*-', '*(-1)*'), ('/-', '*(-1)/')]

    for old_op, new_op in double_ops:
        while ud_expr.count(old_op) > 0:
            ud_expr = ud_expr.replace(old_op, new_op)

    return ud_expr


def remove_comma_format(expr):
    '''removes commas from all numbers to eliminate potential conversion
    errors from string to number'''
    if expr.count(',') == 0:
        return expr

    exp_1 = expr
    exp_2 = comma_re.sub(r'\1\2', expr)

    while exp_1 != exp_2:
        exp_1 = exp_2
        exp_2 = comma_re.sub(r'\1\2', exp_1)

    return exp_2


def make_mult_explicit(expr):
    '''returns an expression where any sort of implicit multiplication is
    expressed as a binary operation E.g. 5(9) -> 5*9.'''
    if expr[0] == '-' and not expr[1].isdigit():
        exp_1 = '(-1)*' + expr[1:]
    else:
        exp_1 = expr

    exp_2 = mult_re.subn(r'\1*\2', exp_1)[0]

    if exp_2.count(')(') != 0:
        exp_2 = re.subn(r'(\))(\()', ')*(', exp_2)[0]

    # while exp_1 != exp_2:
    #     exp_1 = exp_2
    #     exp_2 = comma_re.sub(r'\1*\2', exp_1)

    return exp_2


def initial_prep(expr):
    '''formats expression to eliminate ambiguity and make chunking easier'''
    expr_out = expr.replace(' ', '')
    expr_out = expr_out.upper()
    expr_out = remove_doub_ops(expr_out)
    expr_out = remove_comma_format(expr_out)
    expr_out = remove_double_parens(expr_out)
    expr_out = make_mult_explicit(expr_out)

    # print(expr_out)

    return expr_out


if __name__ == '__main__':
    EXP1 = '5+sin(4*6(3-5))'
    EXP4 = '8 - 2(2)(3)'

    print(EXP1)
    print(find_all_parens(EXP1))
    print()
    print(EXP4)
    print(find_all_parens(EXP4))


    # disp_ans(EXP1)

    # EXP2 = '5+sin(-4)'
    # disp_ans(EXP2)

    # EXP3 = '4*6(3-5)'
    # disp_ans(EXP3)
    
    # EXP4 = '8 - 2(2)(3)'
    # find_all_parens(EXP4)
    # disp_ans(EXP4)

    # EXP5 = '8 - 2*2*3'
    # disp_ans(EXP5)
    
    # neg_base = '-3^0.5'
    # disp_ans(neg_base)

    # neg_base2 = '8-3^2'
    # disp_ans(neg_base2)
