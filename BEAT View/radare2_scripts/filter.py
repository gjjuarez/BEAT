import sys
sys.path.append("..")  # for data_manager
import data_manager

def filter_string(value, section, address):
    strings_poi = data_manager.get_pois_from_type("string")
    if strings_poi is None:
        return True
    for s in strings_poi:
        if s["String Name"] in value\
                or s["Section"] in section\
                or s["Address"] == address:
            return True
    return False

def filter_var(name, value, vartype, size, address):
    vars_poi = data_manager.get_pois_from_type("variable")
    if vars_poi is None:
        return True
    for v in vars_poi:
        if v["Variable Name"] in name\
                or v["Variable Value"] in value\
                or v["Call From Address"] == address\
                or v["Variable Type"] in vartype\
                or v["Variable Size"] == size:
            return True
    return False

def filter_function(name, ret_type, ret_value, address, dest_address, call_from="", param_order=[], param_values=[]):
    functions = data_manager.get_pois_from_type("function")
    if functions is None:
        return True
    for func in functions:
        if func["Function Name"] in name\
                or func["Return Type"] in ret_type\
                or func["Return Value"] == ret_value\
                or func["Address"] == address\
                or func["Call From"] in call_from\
                or func["Destination Address"] == dest_address:
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
        valueInOrder = False
        # check if plugin param values match given parameters
        for func_type, plugin_type in param_values, func["Parameter Values"]:
            # values need to match exactly
            # Ex: 8 shouldn't match 81
            if func_type != plugin_type:
                valueInOrder = False
                break
        if valueInOrder:
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
