import re
import collections

# Parser functions

Token = collections.namedtuple('Token', ['typ', 'value', 'start', 'stop'])

token_specification = [
    ('NEGNUM', r'^(\-\d+\.?\d*)'),  # Negative integer or decimal number
    ('NUMBER', r'\d+\.?\d*'),       # Integer or decimal number
    ('PI', r'PI'),                  # PI
    ('FUNC', r'`+'),                # Functions
    ('OP', r'[+\-*/\^]'),           # Arithmetic operators
    ('PARENS', r'\(_+\)'),          # Parenthetical terms
    ('OTHER', r'[A-Za-z]+'),        # Any other words
    # ('LRP', r'[\(\)]'),             # Any parentheses
    ('MISMATCH', r'.'),             # Any other character
]

tok_reg = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

token_re = re.compile(tok_reg)

mult_re = re.compile(r'(\d)(\()|(\d)([a-zA-Z])')

comma_re = re.compile(r'(\d)\,(\d\d\d)')

# arithmetic.py

MUL_DIV_RE = re.compile(r'([\*\/])')
ADD_SUB_RE = re.compile(r'([\-\+])')
DEC_RE = re.compile(r'\.(\d+)')

# Formatting Functions

PAREN_RE = re.compile(r'\([^\(\)]+\)')

MULT_RE = re.compile(r'(\d)(\()|(\d)([a-zA-Z])')

MULTI_I_RE = re.compile(r'([+-])?'                           # sign of term
                        r'(\d+\.\d*|\d+)?'                   # coeff
                        r'(?<![A-HK-Z])(i+|j+)(?![A-HK-Z])'  # multiple i or j
                        r'(\d+\.\d*|\d+)?',                  # coeff
                        flags=re.I)

# Complex 


MULTI_I_RE = re.compile(r'([+-])?'                           # sign of term
                        r'(\d+\.\d*|\d+)?'                   # coeff
                        r'(?<![A-HK-Z])(i+|j+)(?![A-HK-Z])'  # multiple i or j
                        r'(\d+\.\d*|\d+)?',                  # coeff
                        flags=re.I)

COMP_REG = [r'(?P<sign>[+-])?',                            # sign of term
            r'(?P<fac1>\d+\.\d*|\d+)?',                    # coeff
            r'(?<![A-HK-Z])(?P<im>(i+|j+))(?![A-HK-Z])',   # multiple i/j
            r'(?P<fac2>\d+\.\d*|\d+)?'                     # coeff
            ]

COMP_RE = re.compile(''.join(COMP_REG), flags=re.I)

COMP_STR = ['16+1.7320508075688772j', '16 + 1.7320508075688772 j',
            '7-12i', '14+2i', 'win', '(7-12i)*(14+2i)', '3iii']

names = ['sign', 'fac1', 'im', 'fac2']

# for expr in COMP_STR:
#     print(expr)
#     matchobj = COMP_RE.search(expr)
#     print([[name, matchobj.group(name)] for name in names
#            if matchobj is not None])

# comma_re = r'(?<![A-Z]\()(\d{1,3}(?:\,\d{3})+)[^\)]'
comma_re = r'(\d{1,3}\,\d{3}(?:\,\d{3})?)\D?'
COMMA_REG = re.compile(comma_re, flags=re.I)


# def remove_comma_format(matchobj):

expr = '1,234,567'
expr_2 = 'sin(' + expr + ')'
expr_3 = 'sin(' + expr + '+' + expr + ')'


expr_a = '0' * expr.count(',') + expr.replace(',', '')

print(COMMA_REG.search(expr).group(1))
print(COMMA_REG.findall(expr_2))
print(COMMA_REG.findall(expr_3))
