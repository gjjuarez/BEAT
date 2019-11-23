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
        elif s["Address"] == address:
            return True
    return False

def filter_var(name, value, vartype, size, address):
    vars_poi = data_manager.get_pois_from_plugin_and_type("variable")
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