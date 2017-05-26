from equation_parser import disp_ans

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
