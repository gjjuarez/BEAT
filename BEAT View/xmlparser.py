from xmljson import parker as pk
import xml.etree.ElementTree as et
import json
import data_manager


def parse_xml(path):
    print('got to xml parser')
    plugin_tree = et.parse(path)
    plugin_root = plugin_tree.getroot()
    plugin_dict = json.loads(json.dumps(pk.data(plugin_root)))

    plugin = plugin_dict['name']
    desc = plugin_dict['description']
    print("saving data_manager in plugin" + plugin)
    data_manager.save_plugin(plugin, desc)

    print(type(plugin_dict['pointsOfInterest']['variable']))
    print(type(plugin_dict['pointsOfInterest']['function']))

    '''
    VARIABLES
    '''
    if isinstance(plugin_dict['pointsOfInterest']['variable'], dict):
        n = plugin_dict['pointsOfInterest']['variable']['VariableName']
        t = plugin_dict['pointsOfInterest']['variable']['VariableType']
        print('saving vars')
        data_manager.add_variable_to_plugin(plugin, n, t)
    else:
        for f in plugin_dict['pointsOfInterest']['variable']:
            n = f['VariableName']
            t = f['VariableType']
            print('saving vars')
            data_manager.add_variable_to_plugin(plugin, n, t)

    '''
    DLL
    '''
    if isinstance(plugin_dict['pointsOfInterest']['dll'], dict):
        n = plugin_dict['pointsOfInterest']['dll']['Library']
        print('saving dlls')
        data_manager.add_dll_to_plugin(plugin, n)
    else:
        for f in plugin_dict['pointsOfInterest']['dll']:
            n = f['Library']
            print('saving dlls')
            data_manager.add_dll_to_plugin(plugin, n)

    '''
    FUNCTIONS
    '''
    if isinstance(plugin_dict['pointsOfInterest']['function'], dict):
        name = plugin_dict['pointsOfInterest']['function']['FunctionName']
        parameter_ordertype = plugin_dict['pointsOfInterest']['function']['ParameterOrderAndType']
        return_type = plugin_dict['pointsOfInterest']['function']['ReturnType']
        print('saving functions')
        data_manager.add_function_to_plugin(plugin, name, parameter_ordertype, return_type)
    else:
        for f in plugin_dict['pointsOfInterest']['function']:
            name = f['FunctionName']
            parameter_ordertype = f['ParameterOrderAndType']
            return_type = f['ReturnType']
            print('saving functions')
            data_manager.add_function_to_plugin(plugin, name, parameter_ordertype, return_type)

    '''
    STRING
    '''
    if isinstance(plugin_dict['pointsOfInterest']['string'], dict):
        n = plugin_dict['pointsOfInterest']['string']['StringName']
        print('saving strings')
        data_manager.add_string_to_plugin(plugin, n)
    else:
        for f in plugin_dict['pointsOfInterest']['string']:
            n = f['StringName']
            print('saving strings')
            data_manager.add_string_to_plugin(plugin, n)
