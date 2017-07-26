
import re
from parser_functions import func_mapper
from formatting_functions import initial_prep
from arithmatic import evaluate_terms
from tokenizer import chunk_expr


eval_ready_reg = re.compile(r'FUNC|PAREN', flags=re.I)


def atomizer(chunks):
    terms = []
    for item in chunks:
        if item[0] == 'PARENS':
            if len(item[1]) == 1 and type(item[1][0]) is not list:
                terms += item[1]
            else:
                terms += [atomizer(item[1])]
        elif item[0] == 'FUNC':
            f_term = atomizer(item[1][1])
            terms += [func_mapper[item[1][0].upper()](f_term)]
        else:
            terms += [item[1]]

    while eval_ready_reg.search(str(terms)) is not None:
        terms = atomizer(terms)

    answer = evaluate_terms(terms)

    return answer


def evaluate(expr):
    ud_expr = initial_prep(expr)
    chunk = chunk_expr(ud_expr)
    answer = atomizer(chunk)

    return answer


def disp_ans(expr):
    print(expr, '=', evaluate(expr))


if __name__ == '__main__':
    EXP1 = '5+sin(4*6(3-5))'
    disp_ans(EXP1)

    EXP2 = '5+sin(-4)'
    disp_ans(EXP2)

    EXP3 = '4*6(3-5)'
    disp_ans(EXP3)

    EXP4 = '8 - 2(2)(3)'
    disp_ans(EXP4)

    EXP5 = '8 - 2*2*3'
    disp_ans(EXP5)

    EXP6 = '(5+3j)(5-2j)'
    disp_ans(EXP6)

    EXP7 = '5i + 4*6(3i-5)'
    disp_ans(EXP7)

    neg_base = '-3^0.5'
    disp_ans(neg_base)

    neg_base2 = '8-3^2'
    disp_ans(neg_base2)
