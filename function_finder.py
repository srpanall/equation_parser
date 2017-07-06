import re
import os
from pprint import pprint

func_reg = re.compile(r'def ([^\(]+)')


def find_function(file_name):
    func_list_out = []
    with open(file_name, 'r') as f:
        for line in f:
            name_obj = func_reg.match(line)
            if name_obj is not None:
                func_list_out += [name_obj.group()]

    return func_list_out


files = [[file, find_function(file)] for file in os.listdir()
         if file.endswith('py')]

pprint(files)
