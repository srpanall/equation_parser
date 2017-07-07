import re
import os
from pprint import pprint

func_reg = re.compile(r'def ([^\(]+)')


def find_funcs_2(file_name):
    funcs = [match_obj.group(1) for match_obj in
             [func_reg.match(line) for line in open(file_name)]
             if match_obj is not None]

    return funcs


files = [file for file in os.listdir() if file.endswith('py')]

# print(files[2])

# pprint(find_funcs_2(files[2]))


def func_depend(func_names, file_text):
    func_list = sorted(func_names, key=len, reverse=True)
    func_reg = '|'.join(func_list)
    func_re = re.compile(func_reg)


    return func_list


pprint(func_depend(find_funcs_2(files[2]), 4))


# comp_reg_list2 += [r'([^a-zA-z][ij])', r'([ij][^a-zA-z])',
#                    r'([^a-zA-z][ij][^a-zA-z])', r'(i+)', r'(j+)'
#                    ]

# comp_reg2 = '|'.join(comp_reg_list2)

# comp_re2 = re.compile(comp_reg2, flags=re.I)