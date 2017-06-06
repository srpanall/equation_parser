import re
from pprint import pprint



complex_strings = ['3jjj', '16+1.732050j8.075688772', '7-12j',
                   '(7-12j)*(14+2j)']

i_update = r'(\d+\.\d*|\d+)([+-])?(\d+\.\d*|\d+)?(j+)(\d+\.\d*|\d+)?'


i_update_reg = re.compile(i_update)


def update_i_coeff(matchobj):
    expr_parts = [x for x in matchobj.groups() if x is not None]
    upd_parts = []
    print(expr_parts)
    for x in expr_parts:
        n = x.count('j')
        if n != 0:
            upd_parts += [complex('j') ** n]
        elif x in ['+', '-']:
            upd_parts += [x]
        else:
            upd_parts += [complex(x)]

    pprint(upd_parts)


def expr_update(expr):
    upd_expr = expr.replace(" ", "")
    matchobj = i_update_reg.search(upd_expr)
    update_i_coeff(matchobj)


for c_string in complex_strings:
    expr_update(c_string)


