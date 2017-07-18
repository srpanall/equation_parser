import re
import os
from pprint import pprint

def_re = re.compile(r'def ([^\(]+)')

files = [file for file in os.listdir() if file.endswith('py')]


def list_defs(file):
    """Given a python file returns a dictionary function: definition"""
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
    """Given a dictioanry containing functions and their definitions
    returns a dictionary of functions and their first order dependents
    in the form function: dependent functions
    """
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


def all_depend(file):
    """Given a python file returns a dictionary of the form
    function: all dependents.

    If the function is recursive, the first entry in the value is 'self'.
    """
    depend_dict = func_depend(file)
    def_list = [key for key, value in depend_dict.items() if value is not None]
    d_out = {key: value for key, value in depend_dict.items() if value is None}

    for func in def_list:
        func_set = set(depend_dict[func])
        test = False
        d_out_val = []
        temp_funcs = {func_name for func_name in func_set}

        while not test:
            set_len = len(temp_funcs)
            for dep_func in func_set:
                if depend_dict[dep_func] is not None:
                    temp_funcs = temp_funcs | set(depend_dict[dep_func])
            test = set_len == len(temp_funcs)

        d_out_val = sorted(list(temp_funcs))

        if func in d_out_val:
            d_out_val = ['self'] + d_out_val
            d_out_val.remove(func)
        d_out[func] = d_out_val

    return d_out


def funcs_using(func_dict):
    """Takes a dictionary of functions and their dependents and returns a
    dictionary functions: functions using key.
    """
    func_w_dep = [key for key, value in func_dict.items() if value is not None]

    list_depend = [set(func_dict[key]) for key in func_w_dep]
    set_depend = list_depend[0]
    for set_vals in list_depend[1:]:
        set_depend |= set_vals

    if 'self' in set_depend:
        set_depend.remove('self')

    dep_func = sorted(list(set_depend))

    dep_out = {func: [caller for caller in func_w_dep if
               func in func_dict[caller]] for func in dep_func}

    return dep_out


pprint(funcs_using(all_depend(files[3])))
