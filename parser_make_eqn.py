########################################
# Goal: Create a file containing random expressions to test equation parser
# Idea: While creating the expression, also create a list so that the
#       expression can be evaluated. Then the expression and value are
#       outputed to a file as expression = value. This way, a test can be
#       written.
#
#       test_vals = [line.split('=') for line in file]
#       for lhs, rhs in test_vals:
#           if evaluate(lhs) == float(rhs):
#               return True
#           else: return False

import random
import operator as ops
# from pprint import pprint
import equation_parser


dict_op = {'-': ops.sub, '+': ops.add, '*': ops.mul, '/': ops.truediv,
           '^': ops.pow}


def pow_mul_div(l_in, bin_op):
    if type(bin_op) == list:
        o_p = min(l_in.index('*'), l_in.index('/'))
    else:
        o_p = l_in.index(bin_op)

    l_in[o_p - 1] = dict_op[l_in[o_p]](l_in[o_p - 1], l_in[o_p + 1])
    l_out = l_in[:o_p] + l_in[o_p + 2:]

    return l_out


def find_rhs(rhs_list):
    uptd = [x for x in rhs_list]
    while len(uptd) > 1:
        while uptd.count('^') > 0:
            uptd = pow_mul_div(uptd, '^')
        times = uptd.count('*')
        div = uptd.count('/')
        if times + div == 0:
            while len(uptd) > 1:
                uptd[2] = dict_op[uptd[1]](uptd[0], uptd[2])
                uptd = uptd[2:]
            return uptd[0]
        elif div == 0:
            uptd = pow_mul_div(uptd, '*')
        elif times == 0:
            uptd = pow_mul_div(uptd, '/')
        else:
            uptd = pow_mul_div(uptd, ['*', '/'])

    return uptd[0]


# list_op = ['+', '-', '*', '/']
list_op = ['+', '-', '*', '/', '^']

equations = []
eval_expr = []

num_eqn = 50

for n in range(num_eqn):
    n1 = random.randint(1, 100)
    # n1 = n1 * random.choice([-1, 1])
    lhs = str(n1)
    rhs = [n1]
    num_ops = random.randint(1, 5)

    for t in range(num_ops):
        op = random.choice(list_op)
        if op == '^':
            n_max = 5
        else:
            n_max = 100
        n1 = random.randint(1, n_max)
        n1 = n1 * random.choice([-1, 1])
        temp_lhs = op + str(n1)
        lhs += temp_lhs
        rhs += [op, n1]
    # print(rhs)
    rhs = find_rhs(rhs)

    try:
        lhs_val = equation_parser.evaluate(lhs)
        if abs(lhs_val - rhs) < 10 ** -10:
            eval_expr += [[lhs, lhs_val, rhs]]
    except TypeError:
        print(lhs)

    # print(lhs, ' = ', rhs)

# pprint(equations)
# pprint(eval_expr)
