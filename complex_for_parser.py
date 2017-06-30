
#######################################
#
# Update functions to work in main parser program.
#
#
#######################################

import re
# from pprint import pprint


complex_strings = ['3jjj', '16+1.732050j8.075688772', '7-12j',
                   '(7-12j)*(14+2j)']

i_update = r'(\d+\.\d*|\d+)([+-])?(\d+\.\d*|\d+)?(j+)(\d+\.\d*|\d+)?'
i_update_reg = re.compile(i_update)

multiple_i = r'([+-])?(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'
multi_i_reg = re.compile(multiple_i, flags=re.I)

comp_forms = [r'\d[ij]', r'[ij]\d', r'ii+', r'jj+', r'([^a-zA-z][ij])',
              r'([ij][^a-zA-z])', r'([^a-zA-z][ij][^a-zA-z])'
              ]

comp_forms_reg = '|'.join(comp_forms)

comp_test_re = re.compile(comp_forms_reg, flags=re.I)


def update_i_coeff(matchobj):
    expr_parts = [x for x in matchobj.groups() if x is not None]
    upd_parts = []
    # print(expr_parts)
    for x in expr_parts:
        n = x.count('j')
        if n != 0:
            upd_parts += [complex('j') ** n]
        elif x in ['+', '-']:
            upd_parts += [x]
        else:
            upd_parts += [complex(x)]

    # pprint(upd_parts)
    return upd_parts


def comp_term_type(array):
    type_out = ''
    # print('array', array)
    for n, term in enumerate(array):
        if term in ['+', '-']:
            type_out += 'o'
        type_out = type_out + str(n) + ' '
    return type_out


def expr_update(expr):
    upd_expr = expr.replace(" ", "")
    if comp_test_re.search(upd_expr) is None:
        return '%s contains no complex numbers' % expr

    else:
        upd_expr = multi_i_reg.sub(fix_im, upd_expr)
        return upd_expr
        # matchobj = i_update_reg.search(upd_expr)
        # expr_terms = update_i_coeff(matchobj)

        # return eval_complex(expr_terms)


def eval_complex(expr_terms):
    c_out = 0

    num_terms = len(expr_terms)

    if num_terms == 3 and expr_terms[1] in ['+', '-']:
        if expr_terms[1] == '+':
            c_out = expr_terms[0] + expr_terms[2]
        else:
            c_out = expr_terms[0] - expr_terms[2]
    elif num_terms == 2:
        c_out = expr_terms[0] * expr_terms[1]
    elif num_terms == 1:
        c_out = expr_terms[0]
    else:
        terms = re.split(r'(o\d)', comp_term_type(expr_terms))
        # print(terms)
        new_terms = []

        for term in terms:
            # print(term)
            if term[0] == 'o':
                new_terms += [expr_terms[1]]
                continue
            n = [int(x) for x in term.split(' ') if x.isdigit()]
            # print(n)
            if len(n) == 1:
                new_terms += [expr_terms[n[0]]]
            else:
                c_temp = expr_terms[n[0]]
                for c in n[1:]:
                    c_temp *= expr_terms[c]
                new_terms += [c_temp]

        c_out = eval_complex(new_terms)

    # print(c_out)
    return c_out


# for c_string in complex_strings:


complex_string2 = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
                   '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii',
                   '16+1.732050j8.075688772', '7-12J']


def fix_im(matchobj):
    # print(matchobj.groups())
    txt = [x for x in matchobj.groups()]
    n_j = txt[2].count(txt[2][0])
    factors = [float(x) if x is not None else 1 for x in [txt[1], txt[3]]]

    if txt[0] == '-':
        sign = -1
    else:
        sign = 1

    com_num = sign * factors[0] * factors[1] * 1j ** n_j

    im_coeff = com_num.imag

    if im_coeff > 0:
        return '+' + str(im_coeff) + 'j'
    else:
        return str(im_coeff) + 'j'

    # return ''.join([x for x in txt if x is not None])


for c_s in complex_string2:
    c_val = expr_update(c_s)
    print(c_s, '=', c_val)
    # c_s_upd = c_s.replace(" ", "")
    # print(c_s, '=', multi_i_reg.sub(fix_im, c_s_upd))
