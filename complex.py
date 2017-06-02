# import math
# import collections
import re
# from itertools import product
from pprint import pprint
# import cmath as cm

complex_strings = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
                   '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii',
                   '16+1.732050j8075688772', '7-12J']

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

i_bad = r'([+-])?(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'
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

i_bad_reg = re.compile(i_bad, flags=re.I)

def find_complex(expr):
    expr_out = expr.replace(' ', '')
    if comp_test_re.search(expr_out) is None:
        print(expr, 'no complex numbers')
    else:
        print(expr)


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

    try:
        c = complex(temp_text)
        print('works', c)
    except ValueError:
        # temp = i_bad_reg.findall(temp_text)
        # pprint(temp)
        upd_text = i_bad_reg.sub(r'\1\2j\4', temp_text)
        print(temp_text, upd_text)


    # terms = i_coeff_re.split(temp_text)
    # term_out = [x for x in terms if x is not None and x != '']

    # pprint(term_out)

    # pprint(term_out)

# comp_coeff = [r'\d+', r'\d+\.\d*', r'']

# comp_reg_list = [x + r'[+-]' + y + r'[ij]'
#                  if x != ''
#                  else
#                  y + r'[ij]'
#                  for x, y
#                  in product(comp_coeff, repeat=2)
#                  ]

# c_r_l_n = comp_reg_list.index(r'[ij]')

# comp_reg_list[c_r_l_n] = r'[^a-zA-z]' + comp_reg_list[c_r_l_n]

# comp_reg = '|'.join(comp_reg_list)

# comp_re = re.compile(comp_reg, flags=re.I)

# comp_reg_list2 = ['(' + x + r'[+-]' + y + r'[ij])'
#                   if x != ''
#                   else
#                   '(' + y + r'[ij])'
#                   for x, y
#                   in product(comp_coeff, repeat=2)
#                   ]

# comp_reg_list2.remove(r'([ij])')

# comp_reg_list2 += [r'([^a-zA-z][ij])', r'([ij][^a-zA-z])',
#                    r'([^a-zA-z][ij][^a-zA-z])', r'(i+)', r'(j+)'
#                    ]

# comp_reg2 = '|'.join(comp_reg_list2)

# comp_re2 = re.compile(comp_reg2, flags=re.I)


# def find_complex(expr):
#     expr_out = expr.replace(' ', '')
#     # expr_out = expr_out.upper()
#     # test = complex_test_re.search(expr_out) is None
#     # print(expr_out, test)
#     if comp_test_re.search(expr_out) is None:
#         print(expr, 'no complex numbers')
#     else:
#         # print(expr)
#         comp_num = comp_re.findall(expr_out)
#         # print(type(comp_num))
#         comp_num = [re.sub(r'[iIJ]', 'j', x) for x in comp_num]
#         print(expr, comp_num)


# def replace_complex(expr):
#     expr_out = expr.replace(' ', '')
#     if comp_test_re.search(expr_out) is None:
#         print(expr, 'no complex numbers')
#     else:
#         terms = [x for x in comp_re2.split(expr_out)
#                  if x is not None and x != ''
#                  ]
#         upd_terms = [x if comp_test_re.search(x) is None else
#                      '(' + re.sub(r'[ijIJ]', 'j', x) + ')' for x in terms
#                      ]
#         expr_out = ''.join(upd_terms)

#         print(expr, expr_out)