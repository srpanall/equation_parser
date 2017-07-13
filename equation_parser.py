
import re
# import os
# from pprint import pprint
import operator
import fractions as frac
import numpy as np
from parser_functions import *

# ### Preparing the Expression


def find_all_parens(expression):
    '''returns a list containing the location of each set of parentheses
    as [lp_pos,rp_pos]'''

    paren_info = [[x.group(), x.start(), x.end()]
                  for x in re.finditer(r'\([^\(\)]+\)', expression)]
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

    exp_2 = mult_re.subn(r'\1*\2', exp_1)[0]

    if exp_2.count(')(') != 0:
        exp_2 = re.subn(r'(\))(\()', ')*(', exp_2)[0]

    # while exp_1 != exp_2:
    #     exp_1 = exp_2
    #     exp_2 = comma_re.sub(r'\1*\2', exp_1)

    return exp_2


def initial_prep(expr):
    '''formats expression to eliminate ambiguity and make chunking easier'''
    expr_out = expr.replace(' ', '')
    expr_out = expr_out.upper()
    expr_out = remove_doub_ops(expr_out)
    expr_out = remove_comma_format(expr_out)
    expr_out = remove_double_parens(expr_out)
    expr_out = make_mult_explicit(expr_out)

    # print(expr_out)

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
            expr_start, expr_end = match.span()
            paren_loc = find_all_parens(expr_out)
            old = expr_out[expr_start: paren_loc[expr_end]]
            expr_out = expr_out.replace(old, '`' * len(old))

    return expr_out


def token_prep(expr):
    '''prepares for Tokenizer by replacing contents of parentheses/functions
    with symbols'''
    expr_out = id_paren(expr)
    expr_out = id_funct(expr_out)

    return expr_out


# ### Chunk Functions


def op_chunk(*tupe):
    '''Returns the binary operator in the chunk'''
    return tupe[1][1]


def num_chunk(*tupe):
    '''converts number from string to numerical value'''
    num = tupe[1][1]
    if num.count('.') == 1:
        return float(num)
    return int(num)


def func_chunk(expr, tupe):
    '''Returns a list of the form [mathematical function, argument]'''
    func_in = expr[tupe[2]:tupe[3]]

    func = re.match(r'[A-Za-z]+\(', func_in).group()
    func_out = func[:-1]
    x_val = func_in[len(func): -1]

    return [func_out.upper(), chunk_expr(x_val)]


def paren_chunk(expr, tupe):
    '''Recursively chunks the contents of the parentheses in the expression'''
    return chunk_expr(expr[tupe[2] + 1:tupe[3] - 1])


def other_chunk(*tupe):
    '''Returns any unknown word, serves to identify unknown functions'''
    return tupe[1][1]


# def lrp_chunk(*tupe):
#     return tupe[1][1]


def pi_chunk(*tupe):
    '''Returns pi if present'''
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


def tokenize(code):
    '''Returns a list of named tuples containing the type of chunk, its
    content, as well as the start and end point in the function and it's
    position in the string'''
    dict_kinds = {'FUNC': '`', 'PARENS': '(_)'}

    for mobj in token_re.finditer(code):
        kind = mobj.lastgroup

        if kind in dict_kinds:
            value = dict_kinds[kind]
        else:
            value = mobj.group(kind)
        if kind == 'MISMATCH':
            raise RuntimeError('%r unexpected in %s' % (value, code))
        else:
            start, end = mobj.span()
            yield Token(kind, value, start, end)


def chunk_expr(expr):
    '''Parses the expression and returns a list of numbers, binary operators,
    '''
    mod_expr = token_prep(expr)

    tokens = [token for token in tokenize(mod_expr)]

    chunks = [[token[0], DCHUNK[token[0]](expr, token)] for token in tokens]

    return chunks


# ### Evaluation functions


def decimal_place_counter(number):
    '''Returns the number of digits to the right of the decimal point'''
    num_str = str(number)
    if num_str.count('.') == 0:
        return 0
    else:
        return len(num_str) - 1 - num_str.index('.')


def eval_bin_expr(num_1, num_2, bin_op):
    '''returns c with the appropriate number of digits in an effort to avoid
    floating point error'''

    if bin_op == '/':
        if isinstance(num_1, int) and isinstance(num_2, int):
            return frac.Fraction(num_1, num_2)
        return num_1 / num_2

    num_3 = BIN_OP_DICT[bin_op](num_1, num_2)

    num_1_places = decimal_place_counter(num_1)
    num_2_places = decimal_place_counter(num_2)
    num_3_places = decimal_place_counter(num_3)

    if bin_op == '*':
        r_places = num_1_places * num_2_places
    else:
        r_places = max(num_1_places, num_2_places)

    if num_3_places <= r_places:
        return num_3
    else:
        str_num_3 = str(num_3)
        new_num_3 = str_num_3[:len(str_num_3) - r_places]

    if new_num_3.count('.') == 1:
        return float(new_num_3)
    else:
        return int(new_num_3)


BIN_OP_DICT = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
}


def eval_a_op_b(terms, op_1, op_2):
    '''performs the first calculation according to the order
    of operations in the terms'''
    index_1 = first_index(terms, op_1, op_2)
    num_1, num_2 = terms[index_1 - 1], terms[index_1 + 1]
    bin_op = terms[index_1]

    terms[index_1 - 1] = eval_bin_expr(num_1, num_2, bin_op)

    del terms[index_1: index_1 + 2]

    return terms


def first_index(terms, op_1, op_2):
    '''determines'''
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

    EXPW = '7 + 3 + 1 + 3 + 5 + 3 + 1 +3 '
    disp_ans(EXPW)
    # neg_base = '-3^0.5'
    # disp_ans(neg_base)

    # neg_base2 = '8-3^2'
    # disp_ans(neg_base2)
