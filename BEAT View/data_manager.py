#! /usr/bin/env python3

# database_operations.py version 1.2
import pymongo
from bson import ObjectId

# Data will be stored in the following format on the mongo Database
# database = project selected
# collection = the POI selected (String, struct, etc.)
# document = data related to the POI (type, size, etc.)

# connect to database on a local machine
connection = pymongo.MongoClient('localhost', 27017)

# create database
current_database = 'BEAT_Database'  # change string ('temp') here to make a new database for each project***
database = connection[current_database]

project_collection = database['project']
current_collection = database['current']
plugin_collection = database['plugin']

'''
#################################################################################
Plugin functions
#################################################################################
'''
def get_plugin_names():
    plugins = []
    for c in plugin_collection.find():
        plugins.append(str(c["name"]))
    return plugins

def save_plugin(name, desc):
    plugin_dict = {"name": name,
                   "desc": desc}
    plugin_collection.insert_one(plugin_dict)

def get_plugin_from_name(to_find):
    name = ""
    desc = ""
    for c in plugin_collection.find():
        try :
            if(c["name"] == to_find):
                name = c["name"]
                desc = c["desc"]
                return name, desc
        except KeyError:
            print("Key error")
def delete_plugin_given_name(name):
    plugin_collection.delete_one({'name': name})

def add_string_to_plugin(name, string):
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"string": string}
    },upsert=True
    )
    from pprint import pprint

    cursor = plugin_collection.find({})
    for document in cursor: 
        pprint(document)
    #plugin_collection.findOneAndUpdate({name}.insert_one({string: 'whatever'}))
def add_function_to_plugin(name, string):
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"string": string}
    },upsert=True
    )
def add_variable_to_plugin(name, variable):
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"variable": variable}
    },upsert=True
    )

def add_dll_to_plugin(name, dll):
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"dll": dll}
    },upsert=True
    )
def add_packet_to_plugin(name, packet):
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"packet": packet}
    },upsert=True
    )
def add_struct_to_plugin(name, struct):
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"struct": struct}
    },upsert=True
    )

'''
#################################################################################
Project functions
#################################################################################
'''

variable_collection = None
string_collection = None
function_collection = None  #libraries (imports) included in this collection
protocol_collection = None
struct_collection = None
global_var_collection = None

def initialize_POI_collections(project_name):
    global variable_collection
    global string_collection
    global function_collection
    global protocol_collection
    global struct_collection
    global global_var_collection
    global database

    varName = project_name + "Variables"
    stringName = project_name + "Strings"
    functionName = project_name + "Functions"
    protocolName = project_name + "Protocols"
    structName = project_name + "Structs"
    globalVarName = project_name + "GlobalVars"

    if varName not in database.list_collection_names():
        database.create_collection(varName)
    variable_collection = database[varName]

    if stringName not in database.list_collection_names():
        database.create_collection(stringName)
    string_collection = database[stringName]

    if functionName not in database.list_collection_names():
        database.create_collection(functionName)
    function_collection = database[functionName]

    if protocolName not in database.list_collection_names():
        database.create_collection(protocolName)
    protocol_collection = database[protocolName]

    if structName not in database.list_collection_names():
        database.create_collection(structName)
    struct_collection = database[structName]

    if globalVarName not in database.list_collection_names():
        database.create_collection(globalVarName)
    global_var_collection = database[globalVarName]

def get_project_names():
    projects = []
    for c in project_collection.find():
        projects.append(str(c["name"]))
    return projects

#returns all the POIs within a given collection in a list format
def get_variable_POIs():
    data = variable_collection.find()
    return list(data)

def get_string_POIs():
    data = string_collection.find()
    return list(data)

def get_Function_POIs():
    data = function_collection.find()
    return list(data)

def get_protocol_POIs():
    data = protocol_collection.find()
    return list(data)

def get_struct_POIs():
    data = struct_collection.find()
    return list(data)

def save_project(name, desc, path, binary_info):
    project_dict = {"name": name,
                    "desc": desc,
                    "path": path,
                    "bin_info": binary_info}
    project_collection.insert_one(project_dict)

def save_variables(analysis_run, function_name, POI_name, POI_value, POI_data_type, address):
    global variable_collection
    document = {'Analysis Run': analysis_run,
                'Function Name': function_name,  # to reference parent, avoid conflicting names
                'Variable Name': POI_name,
                'Variable Value': POI_value,
                'Variable Type': POI_data_type,
                'Address': address}
    variable_collection.replace_one({'Function Name': function_name,
                                     'Variable Name': POI_name}, document, upsert=True)

def save_global_variable(analysis_run, POI_name, POI_size, address, comment=""):
    global global_var_collection
    document = {'Analysis Run': analysis_run,
                'Variable Name': POI_name,
                'Variable Size': POI_size,
                'Address': address,
                'Comment': comment}
    global_var_collection.replace_one({'Variable Name': POI_name}, document, upsert=True)

def get_variables():
    global variable_collection
    variables = []
    for var in variable_collection.find():
        variables.append(var)
    return variables

def get_variable_from_name(find_variable):
        name = ""
        for c in variable_collection.find():
            try:
                if (c["Variable Name"] == find_variable):
                    name = c["Variable Name"]
                    return name
            except KeyError:
                print("Key error")

def save_strings(analysis_run, POI_value, section, address, comment=''):
    global string_collection
    document = {'Analysis Run': analysis_run,
                'String Value': POI_value,
                'Section': section,
                'Address': address,
                'Comment': comment}
    string_collection.replace_one({'String Value': POI_value}, document, upsert=True)

def get_strings():
    global string_collection
    strings = []
    for strg in string_collection.find():
        strings.append(strg)
    return strings

def get_string_from_name(find_string):
    name = ""
    for c in string_collection.find():
        try:
            if (c["String Name"] == find_string):
                name = c["String Name"]
                return name
        except KeyError:
            print("Key error")

def save_functions(analysis_run, POI_name, POI_return_type, POI_return_value, POI_binary_section, POI_parameter_order, POI_parameter_type):
    global function_collection
    document = {'Analysis Run': analysis_run,
                'Function Name': POI_name,
                # 'Function Value': POI_value,
                'Return Type': POI_return_type,
                'Return Value': POI_return_value,
                # 'Destination Address': POI_destination_address,
                'Binary Section': POI_binary_section,
                # 'Library Name': POI_name,
                'Parameter Order': POI_parameter_order,
                'Parameter Type': POI_parameter_type,
                # 'Parameter Value': POI_parameter_value,
                # 'Call From Address': POI_order_to_functions
                }
    function_collection.replace_one({"Function Name": POI_name}, document, upsert=True)

def get_function_from_name(find_function):
    name = ""
    for c in function_collection.find():
        try:
            if (c["Function Name"] == find_function):
                name = c["Function Name"]
                return name
        except KeyError:
            print("Key error")

def save_protocols(analysis_run, POI_name, POI_structure, POI_section_size, POI_section_value,
                      POI_binary_section, POI_call_address, comment=''):
    global project_collection
    document = {'Protocol Name': POI_name,
                'Call From Address': POI_call_address,
                'Structure': POI_structure,
                'Section Size': POI_section_size,
                'Section Value': POI_section_value,
                'Binary Section': POI_binary_section,
                'Comment': comment}
    function_collection.replace_one({"Protocol Name": POI_name}, document, upsert=True)

def get_protocol_from_name(find_protocol):
    name = ""
    for c in protocol_collection.find():
        try:
            if (c["Protocol Name"] == find_protocol):
                name = c["Protocol Name"]
                return name
        except KeyError:
            print("Key error")

def save_structs(analysis_run, POI_name, POI_structure, POI_member_order, POI_member_type, POI_member_value,
                    POI_binary_section, POI_call_address, comment=''):
    global struct_collection
    document = {'Struct Name': POI_name,
                'Call From Address': POI_call_address,
                'Structure': POI_structure,
                'Member Order': POI_member_order,
                'Member Type': POI_member_type,
                'Member Value': POI_member_value,
                'Binary Section': POI_binary_section,
                'Comment': comment}
    function_collection.replace_one({"Struct Name": POI_name}, document, upsert=True)

def get_struct_from_name(find_struct):
    name = ""
    for c in struct_collection.find():
        try:
            if (c["Struct Name"] == find_struct):
                name = c["Struct Name"]
                return name
        except KeyError:
            print("Key error")

def get_functions():
    global function_collection
    functions = []
    for func in function_collection.find():
        functions.append(func)
    return functions

def update_current_project(name, desc, path, binary_info):
    current_collection.drop()
    curr_dict = {"name": name,
                 "desc": desc,
                 "path": path,
                 "bin_info": binary_info}
    current_collection.insert_one(curr_dict)

# Get current projects info
# If there is no project, returns three null strings
def getCurrentProjectInfo():
    name = ""
    path = ""
    desc = ""
    bin_info = {}
    for x in current_collection.find():
        try:
            path = x["path"]
            desc = x["desc"]
            name = x["name"]
            bin_info = x["bin_info"]
        except KeyError:
            print("Key error")
    return name, desc, path, bin_info

def get_project_from_name(to_find):
    name = ""
    desc = ""
    path = ""
    bin_info = {}
    for c in project_collection.find():
        try :
            if(c["name"] == to_find):
                name = c["name"]
                desc = c["desc"]
                path = c["path"]
                bin_info = c["bin_info"]
                return name, desc, path, bin_info
        except KeyError:
            print("Key error")

def delete_project_given_name(name):
    try:
        project_collection.delete_one({'name': name})
        current_collection.drop()

        function_collection.drop()
        string_collection.drop()
        variable_collection.drop()
        protocol_collection.drop()
        struct_collection.drop()
    except:
        print("Drop collection error")


# deprecated code (left for now as examples)
def insert_data(data): #data needs to be in json format
   document = collection.insert_one(data)
   return document.inserted_id

def update_or_create(document_id,data):
    #avoids duplicates by by creating a new document if the same id does not exist
    document = collection.update_one({'_id': ObjectId(document_id)},{"$set": data},upsert=True)
    return document.acknowledged

def update_existing(document_id,data):
    document = collection.update_one({'_id': ObjectId(document_id)}, {"$set": data})
    return document.acknowledged

def remove_data(document_id):
    document = collection.delete_one({'_id': ObjectId(document_id)})
    return document.acknowledged #returns true if deleted

# select a single piece of data to return from a collection(point of interest)
def get_single_data(document_id):
    data = collection.find_one({'_id': ObjectId(document_id)})
    return data

def end():
    # close the connection to the database
    connection.close()

# test code##############################################################################################
#initialize_POI_collections("project 1")

#save_variables("static", "integer 1", 254, "integer", 256, "some random section in binary", "here lies a binary address")

#save_variables("static", "integer 2", 254, "integer", 256, "some random section in binary", "here lies a binary address")
#save_variables("dynamic", "integer 1", 254, "integer", 256, "some random section in binary", "here lies a binary address")
