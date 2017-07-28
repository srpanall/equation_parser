"""
'evaluate_expression' provides a function to evaluate a mathematical
expression given as a string.

Examples:

    evaluate('5+sin(4*6(3-5))') = 5.768254661323667

    evaluate('5+sin(-4)') = 5.756802495307928

    evaluate('4*6(3-5)') = -48

    evaluate('8 - 2(2)(3)') = -4

    evaluate('8 - 2*2*3') = -4

    evaluate('(5+3j)(5-2j)') = (31+5j)

    evaluate('5i + 4*6(3i-5)') = (-120+77j)

    evaluate('-3^0.5') = (1.0605752387249068e-16+1.7320508075688772j)

    evaluate('8-3^2') = -1

"""

from expression_parser import evaluate
