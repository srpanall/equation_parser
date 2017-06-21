from equation_parser import evaluate
import re

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
