import re
from pprint import pprint


complex_strings = ['3jjj', '16+1.732050j8.075688772', '7-12j',
                   '(7-12j)*(14+2j)']

i_update = r'(\d+\.\d*|\d+)([+-])?(\d+\.\d*|\d+)?(j+)(\d+\.\d*|\d+)?'
i_update_reg = re.compile(i_update)

i_bad = r'(\d+\.\d*|\d+)?(i+|j+)(\d+\.\d*|\d+)?'
i_bad_reg = re.compile(i_bad, flags=re.I)


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


def type_terms(array):
    type_out = ''
    # print('array', array)
    for n, term in enumerate(array):
        if term in ['+', '-']:
            type_out += 'o'
        type_out = type_out + str(n) + ' '
    return type_out


def expr_update(expr):
    upd_expr = expr.replace(" ", "")
    matchobj = i_update_reg.search(upd_expr)
    expr_terms = update_i_coeff(matchobj)

    return eval_complex(expr_terms)


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
        terms = re.split(r'(o\d)', type_terms(expr_terms))
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
#     c_val = expr_update(c_string)
#     print(c_string, '=', c_val)

complex_string2 = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
                   '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii',
                   '16+1.732050j8.075688772', '7-12J']


def fix_im(matchobj):
    # print(matchobj.groups())
    text_in = [x for x in matchobj.groups()]
    n_j = text_in[1].count(text_in[1][0])
    text_in[1] = 'j' * n_j
    return ''.join([x for x in text_in if x is not None])


for c_s in complex_string2:
    c_s_upd = c_s.replace(" ", "")
    print(c_s, i_bad_reg.sub(fix_im, c_s_upd))
