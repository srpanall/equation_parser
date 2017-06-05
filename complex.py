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

i_bad = r'([+-])?(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'

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

i_bad_reg = re.compile(i_bad, flags=re.I)

i_update_reg = re.compile(i_update)

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

# for text in complex_strings:
#     temp_text = text.replace(' ', '')

#     if comp_test_re.search(temp_text) is None:
#         print('%s no complex numbers' % text)
#         continue

#     c = ''
#     counter = 0

#     while type(c) is not complex and counter < 10:
#         try:
#             c = complex(temp_text)
#         except ValueError:
#             temp_text = i_bad_reg.sub(r'\1\2j\4', temp_text)
#             counter += 1

#     print(text, c)
complex_strings_2 = [i_bad_reg.sub(r'\1\2j\4', x) for x in complex_strings]

for upd_str in complex_strings_2:
    print(i_update_reg.split(upd_str))
