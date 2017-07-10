import re
import os
from pprint import pprint

def_re = re.compile(r'def ([^\(]+)')


def find_funcs_2(file_name):
    funcs = [match_obj.group(1) for match_obj in
             [def_re.match(line) for line in open(file_name)]
             if match_obj is not None]

    return funcs


files = [file for file in os.listdir() if file.endswith('py')]

# print(files[2])


# pprint(find_funcs_2(files[2]))


def list_defs(file):
    text = [line for line in open(file) if line[0] != '#'and
            re.search('\w', line) is not None]
    defs = {}
    def_text = []
    name = ''
    test = False

    for line in text:
        if line[:3] == 'def':
            if test:
                defs[name] = def_text
                def_text = []
            name = def_re.match(line).group(1)
            test = True
        elif test and not line[0].isalpha():
            def_text += [line]
        elif name != '':
            defs[name] = def_text
            def_text = []
            name = ''
            test = False

    return defs


def func_depend(file):
    funcs_with_text = list_defs(file)
    func_names = list(funcs_with_text.keys())
    func_list = sorted(func_names, key=len, reverse=True)
    depend_dict = {}

    for func in func_list:
        def_text = ' '.join(funcs_with_text[func][1:])
        dependendts = []
        for test_func in func_list:
            def_text, n = re.subn(test_func, '', def_text)
            if n > 0:
                dependendts += [test_func]
        if len(dependendts) > 0:
            depend_dict[func] = dependendts
        else:
            depend_dict[func] = None

    return depend_dict


# pprint(func_depend(find_funcs_2(files[2]), 4))

# funcs_list = list(list_defs(files[2]).keys())


pprint(func_depend(files[2]))

# comp_reg_list2 += [r'([^a-zA-z][ij])', r'([ij][^a-zA-z])',
#                    r'([^a-zA-z][ij][^a-zA-z])', r'(i+)', r'(j+)'
#                    ]

# comp_reg2 = '|'.join(comp_reg_list2)

# comp_re2 = re.compile(comp_reg2, flags=re.I)