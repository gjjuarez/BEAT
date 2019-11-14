import data_manager

def filter_strings(plugin, strings):
    strings_poi = data_manager.get_strings_from_name(plugin)
    newS = []
    for s in strings:
        if s in strings_poi:
            newS.append(s)
    return newS

def filter_vars(plugin, vars):
    vars_poi = data_manager.get_strings_from_name(plugin)
    newV = []
    for v in vars:
        if v in vars_poi:
            newV.append(v)
    return newV