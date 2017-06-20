from equation_parser import disp_ans, evaluate
import re

# bad_exp = '-4,029 - 0.25'
# disp_ans(bad_exp)

# exp1 = '5+sin(4*6(3-5))'
# disp_ans(exp1)

# exp1a = '5+sin(-4)'
# disp_ans(exp1a)

# bad1 = '8+100*-21+63'
# disp_ans(bad1)

# bad2 = '8+-100*-21+63'
# disp_ans(bad2)

# exp2 = '4,029 / -4'
# disp_ans(exp2)

# exp2a = '4,029 * - 0.25'
# disp_ans(exp2a)

# neg_base2 = '8-3^2'
# disp_ans(neg_base2)

# # 5/23/17 neg_base2
# # 8-3^2 = -1

# neg_base3 = '8-(-3)^2'
# disp_ans(neg_base3)

# # 5/23/17  neg_base3
# # 8-(-3)^2 = -1

# neg_base4 = '8--3^2'
# disp_ans(neg_base4)

# # 5/23/17  neg_base4
# # 8--3^2 = 17

# exp1_list = ['5+sin(4*6(3-5))', '5+SIN(4*6(3-5))', '5+Sin(4*6(3-5))']

# for text in exp1_list:
#     disp_ans(text)

#############################################################################
# Have issues:

# neg_base = '-3^0.5'
# disp_ans(neg_base)

# 5/22/17 neg_base = '-3^0.5'
# -3^0.5 = (1.0605752387249068e-16+1.7320508075688772j)
#  Issue: real term should be 0

# complex_1 = '5+3j * 7'
# disp_ans(complex_1)

# 5/23/17 complex_1 = 5+3j * 7
# AttributeError: 'complex' object has no attribute 'replace'
# complex_1 = '5+3j * 7'
# TypeError: can't multiply sequence by non-int of type 'str'

# complex_prod = '(7-12i)*(14+2i)'
# disp_ans(complex_prod)
# 5/26/17 complex_prod
# IndexError: list index out of range


expr_list = ['7*2-5*3+4', '3^2(-6+4)', '8 - 2ab', 'a^2 + b^2 - c^2',
             '(a - c)(c + 5)', '12 - 2(a - b )^2', 'a + ( b - c )^2',
             '(a + b) - ab', '5a^2 + bc^2']

var_vals = {'a': '(2)', 'b': '(3)', 'c': '(-6)'}

for expr in expr_list:
    expr_u = expr
    for var, val in var_vals.items():
        expr_u = re.subn(var, val, expr_u)[0]
        # print(expr_u)
    print(expr, '=', evaluate(expr_u))


# 8 - 2ab = 4 sb -4
# (a - c)(c + 5) = 8 sb -8
# (a + b) - ab = 3 sb -1
# 5a^2 + bc^2 = 23 sb 128
