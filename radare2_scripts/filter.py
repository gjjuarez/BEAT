import sys
sys.path.append("..")  # for data_manager
import data_manager

def filter_string(value):
    strings_poi = data_manager.get_pois_from_type("string")
    if strings_poi is None:
        return True
    for s in strings_poi:
        if s["String Name"] in value:
            return True
    return False

def filter_var(name, vartype):
    vars_poi = data_manager.get_pois_from_type("variable")
    if vars_poi is None:
        return True
    for v in vars_poi:
        if v["Variable Name"] in name\
                or v["Variable Type"] in vartype:
            return True
    return False

def filter_function(name, ret_type, param_order=[]):
    functions = data_manager.get_pois_from_type("function")
    if functions is None:
        return True
    for func in functions:
        if func["Function Name"] in name\
                or func["Return Type"] in ret_type:
            return True
        inOrder = True
        # check if plugin parameters match gien parameters
        for func_param, plugin_param in param_order, func["Parameter Order"]:
            # types don't need to match exactly
            # Ex: int can be int32_t or int16_t
            if func_param not in plugin_param:
                inOrder = False
                break
        if inOrder:
            return True

    return False

def filter_dll(name):
    dll_poi = data_manager.get_pois_from_type("dll")
    if dll_poi is None:
        return True
    for d in dll_poi:
        if d["Library"] in name:
            return True
    return False
