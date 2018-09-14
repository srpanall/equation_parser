import tokenizer as toke
import unittest


class TokenizerTests(unittest.TestCase):

    def test_id_paren(self):
        """Replaces the contents of all sets of parentheses with underscores
        and returns a string.
        """
        expr = '( )'
        self.assertEqual(toke.id_paren(expr), '(_)')


# def id_funct(expr):
#     """Replaces all named mathematical functions and their arguments with `
#     and returns a string.
#     """


# def token_prep(expr):
#     """Prepares expression for Tokenizer by replacing parentheses and
#     contents as well as functions and their arguments with symbols and
#     returns a string.
#     """


# # Tokenizing


# def tokenize(code):
#     """Returns a list of named tuples containing the type of chunk, its
#     content, as well as the start and end point in the function and it's
#     position in the string"""


# # Parsing


# def chunk_expr(expr):
#     """Parses the expression and returns a list of numbers, binary operators,
#     functions with arguments, and parenthesis with contents.
#     """

# # Chunk processing


# def op_chunk(*tupe):
#     """Returns the binary operator in the chunk as a string."""


# def num_chunk(*tupe):
#     """Returnse the value of the string as a Fraction object."""


# def func_chunk(expr, tupe):
#     """Returns a list of the form [mathematical function, argument]"""


# def paren_chunk(expr, tupe):
#     """Recursively chunks the contents of nested parentheses and returns a
#     list.
#     """


# def pi_chunk(*tupe):


def main():
    unittest.main()


if __name__ == '__main__':
    main()
