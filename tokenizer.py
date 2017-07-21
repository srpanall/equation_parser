
import re
# import os
# from pprint import pprint
# import operator
import collections
import fractions as frac
import numpy as np
from parser_functions import *
from formatting_functions import find_all_parens



Token = collections.namedtuple('Token', ['typ', 'value', 'start', 'stop'])

token_specification = [
    ('NEGNUM', r'^(\-\d+\.?\d*)'),  # Negative integer or decimal number
    ('NUMBER', r'\d+\.?\d*'),       # Integer or decimal number
    ('PI', r'PI'),                  # PI
    ('FUNC', r'`+'),                # Functions
    ('OP', r'[+\-*/\^]'),           # Arithmetic operators
    ('PARENS', r'\(_+\)'),          # Parenthetical terms
    ('OTHER', r'[A-Za-z]+'),        # Any other words
    ('MISMATCH', r'.'),             # Any other character
]

tok_reg = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
token_re = re.compile(tok_reg)








def id_paren(expr):
    """Replaces the contents of all sets of parentheses with underscores
    and returns a string.
    """
    expr_out = expr

    paren_loc = find_all_parens(expr)
    paren_start = sorted(paren_loc.keys())

    for start in paren_start:
        if expr_out[start] == '(':
            old = expr_out[start: paren_loc[start]]
            new = '(' + '_' * (len(old) - 2) + ')'
            expr_out = expr_out.replace(old, new, 1)

    return expr_out


def id_funct(expr):
    """Replaces all named mathematical functions and their arguments with `
    and returns a string.
    """
    expr_out = expr

    for item in sorted_func:
        while expr_out.count(item) != 0:
            match = re.search(item, expr_out, re.I)
            expr_start, expr_end = match.span()
            paren_loc = find_all_parens(expr_out)
            old = expr_out[expr_start: paren_loc[expr_end]]
            expr_out = expr_out.replace(old, '`' * len(old))

    return expr_out


def token_prep(expr):
    """Prepares expression for Tokenizer by replacing parentheses and
    contents as well as functions and their arguments with symbols and
    returns a string.
    """
    expr_out = id_paren(expr)
    expr_out = id_funct(expr_out)

    return expr_out


def tokenize(code):
    """Returns a list of named tuples containing the type of chunk, its
    content, as well as the start and end point in the function and it's
    position in the string"""
    dict_kinds = {'FUNC': '`', 'PARENS': '(_)'}

    for mobj in token_re.finditer(code):
        kind = mobj.lastgroup

        if kind in dict_kinds:
            value = dict_kinds[kind]
        else:
            value = mobj.group(kind)

        if kind == 'MISMATCH':
            raise RuntimeError('%r unexpected in %s' % (value, code))
        elif kind == 'OTHER':
            raise RuntimeError('%r unknown text in %s' % (value, code))
        else:
            start, end = mobj.span()
            yield Token(kind, value, start, end)


# ### Chunk Functions


def op_chunk(*tupe):
    """Returns the binary operator in the chunk"""
    return tupe[1][1]


def num_chunk(*tupe):
    """converts number from string to numerical value"""
    num = tupe[1][1]
    if num.count('.') == 1:
        return float(num)
    return int(num)


def func_chunk(expr, tupe):
    """Returns a list of the form [mathematical function, argument]"""
    func_in = expr[tupe[2]:tupe[3]]

    func = re.match(r'[A-Za-z]+\(', func_in).group()
    func_out = func[:-1]
    x_val = func_in[len(func): -1]

    return [func_out.upper(), chunk_expr(x_val)]


def paren_chunk(expr, tupe):
    """Recursively chunks the contents of the parentheses in the expression"""
    return chunk_expr(expr[tupe[2] + 1:tupe[3] - 1])


def other_chunk(*tupe):
    """Returns any unknown word, serves to identify unknown functions"""
    return tupe[1][1]


# def lrp_chunk(*tupe):
#     return tupe[1][1]


def pi_chunk(*tupe):
    """Returns pi if present"""
    return np.pi

# dictionary mapping chunk type to appropriate function


DCHUNK = {
    'NEGNUM': num_chunk,
    'NUMBER': num_chunk,
    'FUNC': func_chunk,
    'OP': op_chunk,
    'PARENS': paren_chunk,
    'OTHER': other_chunk,
    # 'LRP': lrp_chunk,
    'PI': pi_chunk,
}

# ### Parsing


def chunk_expr(expr):
    """Parses the expression and returns a list of numbers, binary operators,
    """
    mod_expr = token_prep(expr)

    tokens = [token for token in tokenize(mod_expr)]

    chunks = [[token[0], DCHUNK[token[0]](expr, token)] for token in tokens]

    return chunks


##############################################
# Here
##############################################

def atomizer(chunks):
    terms = []
    # print(chunks)
    for item in chunks:
        # print(item)
        if item[0] == 'PARENS':
            terms += [atomizer(item[1])]
        elif item[0] == 'FUNC':
            f_term = atomizer(item[1][1])
            # print(['item', type(item), item])
            # print(func_mapper[item[1][0]])
            terms += [func_mapper[item[1][0].upper()](f_term)]
        else:
            terms += [item[1]]

    while not eval_ready(terms):
        terms = atomizer(terms)

    answer = evaluate_terms(terms)

    return answer


def evaluate(expr):
    ud_expr = initial_prep(expr)
    chunk = chunk_expr(ud_expr)

    answer = atomizer(chunk)

    if isinstance(answer, frac.Fraction):
        answer = float(answer)

    # print(answer, type(answer))

    return answer


def disp_ans(expr):
    print(expr, '=', evaluate(expr))


# def tracefunc(frame, event, arg, indent=[0]):
#     if event == "call":
#         indent[0] += 2
#         print("-" * indent[0] + "> call function", frame.f_code.co_name)
#     elif event == "return":
#         print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
#         indent[0] -= 2
#     return tracefunc


# import sys
# sys.settrace(tracefunc)

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

    # neg_base = '-3^0.5'
    # disp_ans(neg_base)

    # neg_base2 = '8-3^2'
    # disp_ans(neg_base2)
