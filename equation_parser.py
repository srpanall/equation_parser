
import re
# import os
# from pprint import pprint
import numpy as np
import fractions as frac
from parser_functions import *

# ### Preparing the Expression


def find_all_parens(expression):
    '''returns a list containing the location of each set of parentheses
    as [lp_pos,rp_pos]'''

    paren_info = [[x.group(), x.start(), x.end()]
                  for x in re.finditer('\([^\(\)]+\)', expression)]
    exprs = [x[0] for x in paren_info]
    paren_loc = [[x[1], x[2]] for x in paren_info]

    for item in exprs:
        expression = expression.replace(item, '_' + item[1:-1] + '_')

    if expression.count('(') != 0:
        paren_loc += [[x, y] for x, y in find_all_parens(expression).items()]

    return {x: y for x, y in paren_loc}


def remove_double_parens(expr):
    '''returns the expression after eliminating any double sets of
    parentheses if necessary. e.g. 3((x+y)) beomces 3(x+y)'''

    paren_loc = find_all_parens(expr)
    paren_doub = {x: y - 1 for x, y in paren_loc.items()
                  if paren_loc.get(x - 1, 0) == y + 1}
    doub_loc = list(paren_doub.keys()) + list(paren_doub.values())

    return ''.join([y for x, y in enumerate(expr) if x not in doub_loc])


def remove_doub_ops(expr):
    '''Returns the expression after replacing an operator followed by a negative
    sign with a mathematically equivalent operation'''
    ud_expr = expr
    double_ops = [('+-', '-'), ('--', '+'), ('*-', '*(-1)*'), ('/-', '*(-1)/')]

    for old_op, new_op in double_ops:
        while ud_expr.count(old_op) > 0:
            ud_expr = ud_expr.replace(old_op, new_op)

    return ud_expr


def remove_comma_format(expr):
    '''removes commas from all numbers to eliminate potential conversion
    errors from string to number'''
    if expr.count(',') == 0:
        return expr

    exp_1 = expr
    exp_2 = comma_re.sub(r'\1\2', expr)

    while exp_1 != exp_2:
        exp_1 = exp_2
        exp_2 = comma_re.sub(r'\1\2', exp_1)

    return exp_2


def make_mult_explicit(expr):
    '''returns an expression where any sort of implicit multiplication is
    expressed as a binary operation E.g. 5(9) -> 5*9.'''
    if expr[0] == '-' and not expr[1].isdigit():
        exp_1 = '(-1)*' + expr[1:]
    else:
        exp_1 = expr

    exp_2 = mult_re.sub(r'\1*\2', expr)

    while exp_1 != exp_2:
        exp_1 = exp_2
        exp_2 = comma_re.sub(r'\1*\2', exp_1)

    return exp_2


def initial_prep(expr):
    '''formats expression to eliminate ambiguity and make chunking easier'''
    expr_out = expr.replace(' ', '')
    expr_out = expr_out.upper()
    expr_out = remove_doub_ops(expr_out)
    expr_out = remove_comma_format(expr_out)
    expr_out = remove_double_parens(expr_out)
    expr_out = make_mult_explicit(expr_out)

    return expr_out


def id_paren(expr):
    '''returns the expression after replacing all parentheses and their
    content with underscores'''
    expr_out = expr

    if expr_out.count('((') * expr_out.count('))') != 0:
        expr_out = remove_double_parens(expr_out)

    paren_loc = find_all_parens(expr)
    paren_start = sorted(paren_loc.keys())

    for start in paren_start:
        if expr_out[start] == '(':
            old = expr_out[start: paren_loc[start]]
            new = '(' + '_' * (len(old) - 2) + ')'
            expr_out = expr_out.replace(old, new, 1)

    return expr_out


def id_funct(expr):
    '''returns the expression after replacing all functions and their
    arguments with ` '''
    expr_out = expr

    for item in sorted_func:
        while expr_out.count(item) != 0:
            match = re.search(item, expr_out, re.I)
            x, y = match.span()
            paren_loc = find_all_parens(expr_out)
            old = expr_out[x: paren_loc[y]]
            expr_out = expr_out.replace(old, '`' * len(old))

    return expr_out


def token_prep(expr):
    '''prepares for Tokenizer by replacing contents of parentheses/functions
    with symbols'''
    expr_out = id_paren(expr)
    expr_out = id_funct(expr_out)

    return expr_out


# ### Chunk Functions


def op_chunk(expr, tupe):
    return tupe[1]


def num_chunk(expr, tupe):
    '''converts number from string to numerical value'''
    num = tupe[1]
    if num.count('.') == 1:
        return float(num)
    return int(num)


def func_chunk(expr, tupe):
    '''Returns a list of the form [mathematical function, argument]'''
    func_in = expr[tupe[2]:tupe[3]]

    func = re.match('[A-Za-z]+\(', func_in).group()
    func_out = func[:-1]
    x_val = func_in[len(func): -1]

    return [func_out.upper(), chunk_expr(x_val)]


def paren_chunk(expr, tupe):
    return chunk_expr(expr[tupe[2] + 1:tupe[3] - 1])


def other_chunk(expr, tupe):
    return tupe[1]


def lrp_chunk(expr, tupe):
    pass


def pi_chunk(expr, tupe):
    return np.pi

# dictionary mapping chunk type to appropriate function


d_chunk = {
    'NEGNUM': num_chunk,
    'NUMBER': num_chunk,
    'FUNC': func_chunk,
    'OP': op_chunk,
    'PARENS': paren_chunk,
    'OTHER': other_chunk,
    'LRP': lrp_chunk,
    'PI': pi_chunk,
}

# ### Parsing


def tokenize(code):
    '''Returns a list of named tuples containing the type of chunk, its
    content, as well as the start and end point in the function and it's
    position in the string'''
    dict_kinds = {'FUNC': '`', 'PARENS': '(_)'}

    for mo in token_re.finditer(code):
        kind = mo.lastgroup

        if kind in dict_kinds:
            value = dict_kinds[kind]
        else:
            value = mo.group(kind)
        if kind == 'MISMATCH':
            raise RuntimeError('%r unexpected in %s' % (value, code))
        else:
            start, end = mo.span()
            yield Token(kind, value, start, end)


def chunk_expr(expr):
    '''Reduces the complexity of the expression inside a set of parentheses
    or the argument of a function and returns a list of chunks'''
    mod_expr = token_prep(expr)

    tokens = [x for x in tokenize(mod_expr)]

    chunks = [[x[0], d_chunk[x[0]](expr, x)] for x in tokens]

    return chunks


# ### Evaluation functions


def decimal_place_counter(number):
    '''Returns the number of digits to the right of the decimal point'''
    n = str(number)
    if n.count('.') == 0:
        return(0)
    else:
        return len(n) - 1 - n.index('.')


def sig_figs(a, b, c, op):
    '''returns c with the appropriate number of digits in an effort to avoid
    floating point error'''
    place_a = decimal_place_counter(a)
    place_b = decimal_place_counter(b)
    place_c = decimal_place_counter(c)

    if op == '*':
        r_place = place_a * place_b
    else:
        r_place = max(place_a, place_b)

    if place_c <= r_place:
        return c
    else:
        str_c = str(c)
        new_c = str_c[:len(str_c) - r_place]

    if new_c.count('.') == 1:
        return float(new_c)
    else:
        return int(new_c)


def d_plus(a, b):
    c = a + b
    if isinstance(c, int):
        return c
    else:
        return sig_figs(a, b, c, '+')


def d_minus(a, b):
    c = a - b
    if isinstance(c, int):
        return c
    else:
        return sig_figs(a, b, c, '-')


def d_times(a, b):
    c = a * b
    if isinstance(c, int):
        return c
    else:
        return sig_figs(a, b, c, '*')


def d_divide(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return frac.Fraction(a, b)
    return a / b


bin_op_dict = {
    '+': d_plus,
    '-': d_minus,
    '*': d_times,
    '/': d_divide
}


def first_index(terms, op_1, op_2):
    if terms.count(op_1) != 0:
        i_1 = terms.index(op_1)
    else:
        return terms.index(op_2)

    if terms.count(op_2) == 0:
        return i_1
    else:
        return min(i_1, terms.index(op_2))


def eval_expon(terms):
    # print(terms)
    expr_terms = [x for x in terms]
    i = expr_terms.index('^')
    if expr_terms[i + 1] == '-':
        expr_terms[i + 1] = -1 * expr_terms[i + 2]
        del expr_terms[i + 2]

    expr_terms[i - 1] = expr_terms[i - 1] ** expr_terms[i + 1]

    del expr_terms[i: i + 2]

    return expr_terms


def eval_a_op_b(terms, op_1, op_2):
    i = first_index(terms, op_1, op_2)
    terms[i - 1] = bin_op_dict[terms[i]](terms[i - 1], terms[i + 1])

    del terms[i: i + 2]

    return terms


def evaluate_terms(terms):
    expr_terms = [x for x in terms]

    while expr_terms.count('^') != 0:
        expr_terms = eval_expon(expr_terms)

    while expr_terms.count('*') + expr_terms.count('/') != 0:
        expr_terms = eval_a_op_b(expr_terms, '*', '/')

    while expr_terms.count('+') + expr_terms.count('-') != 0:
        expr_terms = eval_a_op_b(expr_terms, '+', '-')

    return expr_terms[0]


def eval_ready(array):
    string = str(array)
    return 'FUNC' not in string and 'PAREN' not in string


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
            # print('item', type(item), item)
            # print(func_mapper[item[1][0]])
            terms += [func_mapper[item[1][0]](f_term)]
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


if __name__ == '__main__':
    exp1 = '5+sin(4*6(3-5))'
    disp_ans(exp1)

    exp1a = '5+sin(-4)'
    disp_ans(exp1a)
    # neg_base = '-3^0.5'
    # disp_ans(neg_base)

    # neg_base2 = '8-3^2'
    # disp_ans(neg_base2)
