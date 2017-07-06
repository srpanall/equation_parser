import re
import os
from pprint import pprint

folder_path = r"C:\Users\gex02845\Desktop\Programing\New folder"

old_file = 'complex.py'
new_file = 'complex_for_parser.py'


def list_defs(file):
    # path = os.path.join(folder_path, file + '.py')

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
            name = re.match('def ([^\(]+)', line).group(1)
            test = True
        elif test and not line[0].isalpha():
            def_text += [line]
        elif name != '':
            defs[name] = def_text
            def_text = []
            name = ''
            test = False
        else:
            continue

    return defs


def compare_functions(old, new):
    old_defs = list_defs(old)
    new_defs = list_defs(new)

    common_func = list(sorted(set(old_defs.keys()) & set(new_defs.keys())))

    just_old = [func for func in old_defs.keys() if func not in common_func]
    just_new = [func for func in new_defs.keys() if func not in common_func]

    print(old)
    pprint(just_old)
    print()
    print(new)
    pprint(just_new)
    print()

    diff_func = {}

    for func in common_func:
        if old_defs[func] != new_defs[func]:
            diff_func[func] = [old_defs[func], new_defs[func]]

    return diff_func


test = compare_functions(old_file, new_file)

pprint(test)
