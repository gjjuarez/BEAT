import sys
sys.path.append("..")  # for data_manager
import data_manager

def filter_string(value, section, address):
    strings_poi = data_manager.get_pois_from_plugin_and_type("string")
    for s in strings_poi:
        if s["String Name"] in value:
            return True
        elif s["Section"] in section:
            return True
        elif s["Address"] in address:
            return True
    return False

def filter_vars(plugin, vars):
    vars_poi = data_manager.get_strings_from_name(plugin)
    newV = []
    for v in vars:
        if v in vars_poi:
            newV.append(v)
    return newV