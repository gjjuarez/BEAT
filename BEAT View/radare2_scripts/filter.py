import sys
sys.path.append("..")  # for data_manager
import data_manager

def filter_string(value, section, address):
    strings_poi = data_manager.get_pois_from_plugin_and_type("string")
    if strings_poi is None:
        return True
    for s in strings_poi:
        if s["String Name"] in value:
            return True
        elif s["Section"] in section:
            return True
        elif s["Address"] == address:
            return True
    return False

def filter_var(name, value, vartype, size, address):
    vars_poi = data_manager.get_pois_from_plugin_and_type("variable")
    if vars_poi is None:
        return True
    for v in vars_poi:
        if v["Variable Name"] in name:
            return True
        elif v["Variable Value"] in value:
            return True
        elif v["Call From Address"] == address:
            return True
        elif v["Variable Type"] in vartype:
            return True
        elif v["Variable Size"] == size:
            return True
    return False

def filter_function(name, param_order=[], param_values=[], ret_value="0", call_from="", destination=""):
    functions = data_manager.get_pois_from_plugin_and_type("function")
    if functions is None:
        return True
    for func in functions:
        if func["Function Name"] in name:
            return True
    return False
