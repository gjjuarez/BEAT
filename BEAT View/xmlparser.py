from xmljson import parker as pk
import xml.etree.ElementTree as et
import json
from pathlib import Path
#from src.Functionality.database import *
import data_manager

def parse_xml(path):
    print('got to xml parser')
    pluginTree = et.parse(path)
    pluginRoot = pluginTree.getroot()
    pluginDict = json.loads(json.dumps(pk.data(pluginRoot)))

    plugin = pluginDict['name']
    desc = pluginDict['description']
    print("saving data_manager in plugin" + plugin)
    data_manager.save_plugin(plugin, desc)
    #print(f)
    print("aaaaaaaaaaaaaaaaaaaaaaaaa",pluginDict['pointsOfInterest']['variable']['VariableName'])

    print(type(pluginDict['pointsOfInterest']['variable']))
    print(type(pluginDict['pointsOfInterest']['function']))
    ### VARIABLES ###
    if isinstance(pluginDict['pointsOfInterest']['variable'], dict):
        f = pluginDict['pointsOfInterest']['variable']
        n = pluginDict['pointsOfInterest']['variable']['VariableName']
        v = pluginDict['pointsOfInterest']['variable']['VariableValue']
        t = pluginDict['pointsOfInterest']['variable']['VariableType']
        s = pluginDict['pointsOfInterest']['variable']['VariableSize']
        c = pluginDict['pointsOfInterest']['variable']['CallFromAddress']
        print('saving vars')
        data_manager.add_variable_to_plugin(plugin, n, v, t, s, c)
    else:
        for f in pluginDict['pointsOfInterest']['variable']:
            n = f['VariableName']
            v = f['VariableValue']
            t = f['VariableType']
            s = f['VariableSize']
            c = f['CallFromAddress']
            print('saving vars')
            data_manager.add_variable_to_plugin(plugin, n, v, t, s, c)
    ### DLL ###
    if isinstance(pluginDict['pointsOfInterest']['dll'], dict):
        f = pluginDict['pointsOfInterest']['dll']
        n = pluginDict['pointsOfInterest']['dll']['Library']
        print('saving dlls')
        data_manager.add_dll_to_plugin(plugin,n)
    else:
        for f in pluginDict['pointsOfInterest']['dll']:
            n = f['Library']
            print('saving dlls')
            data_manager.add_dll_to_plugin(plugin,n)

### FUNCTIONS ###
    if isinstance(pluginDict['pointsOfInterest']['function'], dict):
        f = pluginDict['pointsOfInterest']['function']
        name = pluginDict['pointsOfInterest']['function']['FunctionName']
        parameter_ordertype = pluginDict['pointsOfInterest']['function']['ParameterOrderAndType']
        value = pluginDict['pointsOfInterest']['function']['ParameterValue']
        reutnr = pluginDict['pointsOfInterest']['function']['ReturnValue']
        binary_section = pluginDict['pointsOfInterest']['function']['BinarySection']
        calladd = pluginDict['pointsOfInterest']['function']['CallFromAddress']
        destadd = pluginDict['pointsOfInterest']['function']["DestinationAddress"]
        pythontranslatedcode = pluginDict['pointsOfInterest']['function']['PythonTranslationCode']
        print('saving functions')
        data_manager.add_function_to_plugin(plugin, name, parameter_ordertype, value, reutnr. binary_section, calladd, destadd, pythontranslatedcode)
    else:
        for f in pluginDict['pointsOfInterest']['function']:
            name = f['FunctionName']
            parameter_ordertype =f['ParameterOrderAndType']
            value = f['ParameterValue']
            reutnr = f['ReturnValue']
            binary_section = f['BinarySection']
            calladd = f['CallFromAddress']
            destadd = f["DestinationAddress"]
            pythontranslatedcode = f['PythonTranslationCode']
            print('saving functions')
            data_manager.add_function_to_plugin(plugin, name, parameter_ordertype, value, reutnr, binary_section, calladd, destadd, pythontranslatedcode)

    ### STRING ###
    if isinstance(pluginDict['pointsOfInterest']['string'], dict):
        f = pluginDict['pointsOfInterest']['string']
        n = pluginDict['pointsOfInterest']['string']['StringName']
        t = pluginDict['pointsOfInterest']['string']['StringType']
        s = pluginDict['pointsOfInterest']['string']['StringSize']
        c = pluginDict['pointsOfInterest']['string']['CallFromAddress']
        a = pluginDict['pointsOfInterest']['string']['Address']
        se = pluginDict['pointsOfInterest']['string']['Section']
        print('saving strings')
        data_manager.add_string_to_plugin(plugin, n, t, s, c, a, s )
    else:
        for f in pluginDict['pointsOfInterest']['string']:
            n = f['StringName']
            t = f['StringType']
            s = f['StringSize']
            c = f['CallFromAddress']
            a = f['Address']
            se = f['Section']
            print('saving strings')
            data_manager.add_string_to_plugin(plugin, n, t, s, c, a, s )

    ### STRUCT ###
    if isinstance(pluginDict['pointsOfInterest']['struct'], dict):
        f = pluginDict['pointsOfInterest']['struct']
        n = pluginDict['pointsOfInterest']['struct']['StructName']
        print('saving structs')
        data_manager.add_struct_to_plugin(plugin,n)
    else:
        for f in pluginDict['pointsOfInterest']['StructName']:
            n = f['struct']
            print('saving structs')
            data_manager.add_struct_to_plugin(plugin,n)

    ### PACKET
    if isinstance(pluginDict['pointsOfInterest']['packet'], dict):
        f = pluginDict['pointsOfInterest']['packet']
        pn = pluginDict['pointsOfInterest']['packet']['ProtocolName']
        fn = pluginDict['pointsOfInterest']['packet']['FieldName']
        ft = pluginDict['pointsOfInterest']['packet']['FieldType']
        print('saving packet')
        data_manager.add_packet_to_plugin(plugin,pn,fn,ft)
    else:
        for f in pluginDict['pointsOfInterest']['packet']:
            pn = f['ProtocolName']
            fn = f['FieldName']
            ft = f['FieldType']
            print('saving packet')
            data_manager.add_packet_to_plugin(plugin,pn,fn,ft)
