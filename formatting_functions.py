"""Functions for initial formating of expressions in the equation parser."""

import re

paren_re = re.compile(r'\([^\(\)]+\)')
comma_re = re.compile(r'(\d)\,(\d\d\d)')
mult_re = re.compile(r'(\d)(\()|(\d)([a-zA-Z])')

multiple_i = r'([+-])?(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'
multi_i_re = re.compile(multiple_i, flags=re.I)

comp_forms = [r'\d[ij]', r'[ij]\d', r'ii+', r'jj+', r'([^a-zA-z][ij])',
              r'([ij][^a-zA-z])', r'([^a-zA-z][ij][^a-zA-z])'
              ]
comp_forms_reg = '|'.join(comp_forms)
comp_test_re = re.compile(comp_forms_reg, flags=re.I)


def update_complex(expr):
    upd_expr = multi_i_re.subn(fix_im, expr)

    return upd_expr[0]


def fix_im(matchobj):
    '''takes the imaginary term found in the expression and converts it to
    the form bi'''
    txt = [item for item in matchobj.groups()]
    n_j = txt[2].count(txt[2][0])
    factors = [float(x) if x is not None else 1 for x in [txt[1], txt[3]]]

    if txt[0] == '-':
        sign = -1
    else:
        sign = 1

    com_num = sign * factors[0] * factors[1] * 1j ** n_j
    im_coeff = com_num.imag

    return '+(' + str(im_coeff) + 'j)'


def find_all_parens(expression):
    """Locates all pairs of parentheses in an expression and returns
    a dictionary with entries lp_pos: rp_pos.
    """
    paren_info = [[paren_obj.group(), paren_obj.start(), paren_obj.end()]
                  for paren_obj in paren_re.finditer(expression)]
    paren_loc = [[span[1], span[2]] for span in paren_info]
    expr_list = list(expression)

    for p_start, p_end in paren_loc:
        expr_list[p_start] = '_'
        expr_list[p_end - 1] = '_'

    expression = ''.join(expr_list)

    if expression.count('(') != 0:
        paren_loc += [[p_start, p_end] for p_start, p_end in
                      find_all_parens(expression).items()]

    return {x: y for x, y in paren_loc}


def remove_double_parens(expr):
    """Replaces double parentheses around an expression with single parentheses
    and returns a string.
    """
    paren_loc = find_all_parens(expr)
    paren_doub = {x: y - 1 for x, y in paren_loc.items()
                  if paren_loc.get(x - 1, 0) == y + 1}
    doub_loc = list(paren_doub.keys()) + list(paren_doub.values())

    return ''.join([y for x, y in enumerate(expr) if x not in doub_loc])


def remove_doub_ops(expr):
    """Replaces binary operators followed by negative signs with mathematically
    equivalent operations and returns a string.
    """
    ud_expr = expr
    double_ops = [('+-', '-'), ('--', '+'), ('*-', '*(-1)*'), ('/-', '*(-1)/')]

    for old_op, new_op in double_ops:
        while ud_expr.count(old_op) > 0:
            ud_expr = ud_expr.replace(old_op, new_op)

    return ud_expr


# Need to address issue of comma seperating 2 arguments of a function


def remove_comma_format(expr):
    """Removes commas from numbers and returns string."""
    if expr.count(',') == 0:
        return expr

    # funcs_w_args = []

    # while func_arg_re.search(expr) is not None:
    #     func_w_arg = func_arg_re.search(expr).group(0)
    #     print(func_w_arg)
    #     expr = expr.replace(func_w_arg, '_')
    #     funcs_w_args += [func_w_arg]

    # print(expr)

    exp_1 = expr
    exp_2 = comma_re.sub(r'\1\2', expr)

    while exp_1 != exp_2:
        exp_1 = exp_2
        exp_2 = comma_re.sub(r'\1\2', exp_1)

    for item in funcs_w_args:
        exp_2 = exp_2.replace('_', item)

    return exp_2


def make_mult_explicit(expr):
    """Replaces implicit multiplication with * and returns a string."""
    if expr[0] == '-' and not expr[1].isdigit():
        exp_out = '(-1)*' + expr[1:]
    else:
        exp_out = expr

    exp_out = mult_re.subn(r'\1*\2', exp_out)[0]

    if exp_out.count(')(') != 0:
        exp_out = re.subn(r'(\))(\()', ')*(', exp_out)[0]

    return exp_out


def initial_prep(expr):
    """Formats expression to eliminate ambiguity and returns a string"""
    expr_out = expr.replace(' ', '')
    expr_out = expr_out.upper()
    expr_out = remove_doub_ops(expr_out)
    # expr_out = remove_comma_format(expr_out)
    expr_out = remove_double_parens(expr_out)
    expr_out = make_mult_explicit(expr_out)

    return expr_out


# EXP2 = 'SIN(3,568)'
# print(remove_comma_format(EXP2))

# EXP3 = '456,789 * SIN(3,568)'
# print(remove_comma_format(EXP3))

# EXP4 = '456,789 * SIN(SIN(7)*3,568)'
# print(remove_comma_format(EXP4))

if __name__ == '__main__':
    EXP1 = '5+sin(4*6(3-5))'
    EXP4 = '8 - 2(2)(3)'

    print(EXP1)
    print(find_all_parens(EXP1))
    print()
    print(EXP4)
    print(find_all_parens(EXP4))
