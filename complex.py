# import math
# import collections
import re
# from itertools import product
from pprint import pprint
# import cmath as cm

complex_strings = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
                   '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii',
                   '16+1.732050j8.075688772', '7-12J']

comp_forms = [r'\d[ij]', r'[ij]\d', r'ii+', r'jj+', r'([^a-zA-z][ij])',
              r'([ij][^a-zA-z])', r'([^a-zA-z][ij][^a-zA-z])'
              ]

comp_forms_reg = '|'.join(comp_forms)

comp_test_re = re.compile(comp_forms_reg, flags=re.I)

i_coeff_list = [r'([+-])?(\d+\.\d*|\d+)(i+|j+)(\d+\.\d*|\d+)',
                r'([+-])?(\d+\.\d*|\d+)(i+|j+)',
                r'([+-])?(i+|j+)(\d+\.\d*|\d+)',
                r'([+-])(i+|j+)(\W)'
                ]

i_update = r'(\d+\.\d*|\d+)([+-])?(\d+\.\d*|\d+)?(j+)(\d+\.\d*|\d+)?'
# ,
#          r'([+-])?(\d+\.\d*|\d+)(i+|j+)',
#          r'([+-])?(i+|j+)(\d+\.\d*|\d+)',
#          r'([+-])(i+|j+)(\W)'
#          ]

# r'([+-])?(ii+|jj+)(\D)'

i_coeff_reg = '|'.join(i_coeff_list)

i_coeff_re = re.compile(i_coeff_reg, flags=re.I)

# i_bad_re = '|'.join(i_bad)

# i_bad_reg = re.compile(i_bad_re, flags=re.I)

i_bad = r'(\d+\.\d*|\d+)?([+-])?(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'
i_bad_reg = re.compile(i_bad, flags=re.I)

i_update_reg = re.compile(i_update)


def find_complex(expr):
    expr_out = expr.replace(' ', '')
    if comp_test_re.search(expr_out) is None:
        print(expr, 'no complex numbers')
    else:
        print(expr)


def ij_update(expr):
    items = [x for x in i_bad_reg.split(expr)
             if x is not None and x != '']
    items_out = []
    for item in items:
        if item[0] in ['i', 'I', 'J']:
            n = item.count(item[0])
            upd_item = n * 'j'
            items_out += [upd_item]
        else:
            items_out += [item]

    return ''.join(items_out)


def update_i_coeff(matchobj):
    print(matchobj.groups())


def expr_update(expr):
    upd_expr = i_update_reg.sub(update_i_coeff, expr)
    upd_expr = re.split(r'(\([^\)]*\))', expr)

    c = ''
    expr_out = []

    for item in upd_expr:
        if item[0] == '(':
            try:
                c = complex(item[1:-1])
            except ValueError:
                c = expr_update(item[1:-1])
                while type(c) is not complex:
                    c = expr_update(c)

            expr_out += [c]
        elif item.count('j') != 0:
            try:
                c = complex(item)
            except ValueError:
                c = expr_update(item)
                while type(c) is not complex:
                    c = expr_update(c)
            expr_out += [item]

    item_type = []

    for item in expr_out:
        if type(item) in [complex, float]:
            item_type += ['n']
        elif item in ['*', '/']:
            item_type += ['md']

        c = re.split(r'(\([^\)]*\))', temp_text)

    # j_loc = 0
    # p_loc = []
    # for n, item in enumerate(expr):
    #     if item[0].isdigit():
    #         upd_expr += [float(item)]
    #         continue
    #     if item[0] == 'j':
    #         j_loc = n
    #     elif item[0] == '(':
    #         p_loc += n
    #     elif item[0] == ')':
    #         p_loc += n
    #     upd_expr += item

    # if p_loc > 2 or p_loc[0] != 0 or len(upd_expr[p_loc[1]]) > 1:
    #     pass

# def j_val_update(val, n):
#     if n == 1:
#         val_out = [val[0], 1]
#     elif n == 3:
#         val_out = [-1 * [val[0], 1]


# for text in complex_strings:
#     temp_text = text.replace(' ', '')
#     terms = i_coeff_re.findall(temp_text)
#     term_out = [[y for y in x if y != ''] for x in terms]
#     for l1 in term_out:
#         val = 1
#         for item in l1:
#             if item[0] in ['i', 'j', 'I', 'J']:
#                 val = val * 1j ** item.count(item[0])
#             elif item == '-':
#                 val *= -1
#             elif item == '+':
#                 continue
#             else:
#                 val *= float(item)
#         print(text, val)


for text in complex_strings:
    temp_text = text.replace(' ', '')

    if comp_test_re.search(temp_text) is None:
        print('%s contains no complex numbers' % text)
        continue

    c = ''

    if temp_text.count('j') == 0:
        temp_text = ij_update(temp_text)

    try:
        c = complex(temp_text)
    except ValueError:
        c = re.split(r'(\([^\)]*\))', temp_text)

    print(text, c)


# complex_strings_2 = [i_bad_reg.sub(r'\1\2j\4', x) for x in complex_strings]

# for upd_str in complex_strings_2:
#     print(i_update_reg.split(upd_str))
