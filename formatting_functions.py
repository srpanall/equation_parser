"""Functions for initial formating of expressions in the equation parser."""

import re

PAREN_RE = re.compile(r'\([^\(\)]+\)')

MULT_RE = re.compile(r'(\d)(\()|(\d)([a-zA-Z])')

MULTI_I_RE = re.compile(r'([+-])?'                           # sign of term
                        r'(\d+\.\d*|\d+)?'                   # coeff
                        r'(?<![A-HK-Z])(i+|j+)(?![A-HK-Z])'  # multiple i or j
                        r'(\d+\.\d*|\d+)?',                  # coeff
                        flags=re.I)


def update_complex(expr_in):
    """Replaces all imaginary terms in an expression with terms in standard
    form and returns a string.
    """
    upd_expr = expr_in
    return MULTI_I_RE.subn(fix_im, upd_expr)[0]


def fix_im(matchobj):
    """Takes an imaginary term found in the expression and returns the
    the string '+(bJ)'.
    """
    txt = [item for item in matchobj.groups()]
    n_j = txt[2].count(txt[2][0])
    factors = [float(x) if x is not None else 1 for x in [txt[1], txt[3]]]

    if txt[0] == '-':
        sign = -1
    else:
        sign = 1

    com_num = sign * factors[0] * factors[1] * 1j ** n_j
    im_coeff = com_num.imag

    exp_out = '(' + str(im_coeff) + '*j)'
    if im_coeff < 0 or txt[0] is not None:
        exp_out = '+' + exp_out

    return exp_out


def find_all_parens(expr_in):
    """Locates all pairs of parentheses in an expression and returns
    a dictionary with entries lp_pos: rp_pos.
    """
    paren_info = [[paren_obj.group(), paren_obj.start(), paren_obj.end()]
                  for paren_obj in PAREN_RE.finditer(expr_in)]
    paren_loc = [[span[1], span[2]] for span in paren_info]
    expr_list = list(expr_in)

    for p_start, p_end in paren_loc:
        expr_list[p_start] = '_'
        expr_list[p_end - 1] = '_'

    upd_expr = ''.join(expr_list)

    if upd_expr.count('(') != 0:
        paren_loc += [[p_start, p_end] for p_start, p_end in
                      find_all_parens(upd_expr).items()]

    return {x: y for x, y in paren_loc}


def remove_double_parens(expr_in):
    """Replaces double parentheses around an expression with single parentheses
    and returns a string.
    """
    paren_loc = find_all_parens(expr_in)
    paren_doub = {x: y - 1 for x, y in paren_loc.items()
                  if paren_loc.get(x - 1, 0) == y + 1}
    doub_loc = list(paren_doub.keys()) + list(paren_doub.values())

    return ''.join([y for x, y in enumerate(expr_in) if x not in doub_loc])


def remove_doub_ops(expr_in):
    """Replaces binary operators followed by negative signs with mathematically
    equivalent operations and returns a string.
    """
    ud_expr = expr_in
    double_ops = [('+-', '-'), ('--', '+'), ('*-', '*(-1)*'), ('/-', '*(-1)/')]

    for old_op, new_op in double_ops:
        while ud_expr.count(old_op) > 0:
            ud_expr = ud_expr.replace(old_op, new_op)

    return ud_expr


def make_mult_explicit(expr_in):
    """Replaces implicit multiplication with * and returns a string."""
    if expr_in[0] == '-' and not expr_in[1].isdigit():
        exp_out = '(-1)*' + expr_in[1:]
    else:
        exp_out = expr_in

    exp_out = MULT_RE.subn(r'\1*\2', exp_out)[0]

    if exp_out.count(')(') != 0:
        exp_out = re.subn(r'(\))(\()', ')*(', exp_out)[0]

    return exp_out


def initial_prep(expr_in):
    """Formats expression to eliminate ambiguity and returns a string"""
    expr_out = expr_in.replace(' ', '')
    expr_out = expr_out.upper()
    expr_out = remove_doub_ops(expr_out)
    expr_out = update_complex(expr_out)
    expr_out = remove_double_parens(expr_out)
    expr_out = make_mult_explicit(expr_out)

    return expr_out


COMP_STR = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
            '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii']



# if __name__ == '__main__':
#     EXP1 = '5+sin(4*6(3-5))'
#     EXP2 = '5i+sin(4*6(3j-5))'
#     EXP3 = '5+sin(4*6(3j-5))'
#     EXP4 = '8 - 2(2)(3)'
#     EXP5 = '5i + int(4*6(3j-5))'

#     print(EXP1)
#     print(initial_prep(EXP1))
#     print()
#     print(EXP2)
#     print(initial_prep(EXP2))
#     print()
#     print(EXP3)
#     print(initial_prep(EXP3))
#     print()
#     print(EXP5)
#     print(initial_prep(EXP5))
#     for expr in COMP_STR:
#         print(expr)
#         print(initial_prep(expr))
