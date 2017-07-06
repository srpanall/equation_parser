#######################################
#
# Update functions to work in main parser program.
#
#
#######################################

import re

complex_strings = ['3jjj', '16+1.732050j8.075688772', '7-12j',
                   '(7-12j)*(14+2j)']
complex_string2 = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
                   '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii',
                   '16+1.732050j8.075688772', '7-12J']


multiple_i = r'([+-])?(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'
multi_i_reg = re.compile(multiple_i, flags=re.I)


comp_forms = [r'\d[ij]', r'[ij]\d', r'ii+', r'jj+', r'([^a-zA-z][ij])',
              r'([ij][^a-zA-z])', r'([^a-zA-z][ij][^a-zA-z])'
              ]
comp_forms_reg = '|'.join(comp_forms)
comp_test_re = re.compile(comp_forms_reg, flags=re.I)


def expr_update_complex(expr):
    upd_expr = expr.replace(" ", "")

    if comp_test_re.search(upd_expr) is None:
        return '%s contains no complex numbers' % expr
    else:
        upd_expr = multi_i_reg.sub(fix_im, upd_expr)
        return upd_expr


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

    if im_coeff > 0:
        return '+' + str(im_coeff) + 'j'
    else:
        return str(im_coeff) + 'j'


for c_s in complex_string2:
    c_val = expr_update_complex(c_s)
    print(c_s, '=', c_val)
