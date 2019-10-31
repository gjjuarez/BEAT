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

def initialize_POI_collections(project_name):
    global variable_collection
    global string_collection
    global function_collection
    global protocol_collection
    global struct_collection
    global database

    varName = project_name + "Variables"
    stringName = project_name + "Strings"
    functionName = project_name + "Functions"
    protocolName = project_name + "Protocols"
    structName = project_name + "Structs"

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

def get_project_names():
    projects = []
    for c in project_collection.find():
        projects.append(str(c["name"]))
    return projects

def save_project(name, desc, path, binary_info):
    project_dict = {"name": name,
                    "desc": desc,
                    "path": path,
                    "bin_info": binary_info}
    project_collection.insert_one(project_dict)

def save_variables(analysis_run, POI_name, POI_value, POI_data_type,
                   POI_size, POI_binary_section, POI_call_address):
    global variable_collection
    document = {'Variable Name': POI_name,
                'Variable Value': POI_value,
                'Variable Type': POI_data_type,
                'Variable Size': POI_size,
                'Binary Section': POI_binary_section,
                'Call From Address': POI_call_address}
    variable_collection.insert_one({'Analysis run': analysis_run, "POI Values": document})

def save_strings(analysis_run, POI_name, POI_value, POI_data_type, POI_size, POI_binary_section,
                    POI_call_address, POI_destination_address):
    global string_collection
    document = {'String Name': POI_name,
                'String Value': POI_value,
                'String Type': POI_data_type,
                'String Size': POI_size,
                'Call From Address': POI_call_address,
                'Destination Address': POI_destination_address,
                'Section': POI_binary_section}
    string_collection.insert_one({'Analysis run': analysis_run, "POI Values": document})

def save_functions(analysis_run, POI_name, POI_return_type, POI_return_value, POI_binary_section, POI_parameter_order, POI_parameter_type):
    global function_collection
    document = {'Analysis run': analysis_run,
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

def save_protocols(analysis_run, POI_name, POI_structure, POI_section_size, POI_section_value,
                      POI_binary_section, POI_call_address):
    global project_collection
    document = {'Protocol Name': POI_name,
                'Call From Address': POI_call_address,
                'Structure': POI_structure,
                'Section Size': POI_section_size,
                'Section Value': POI_section_value,
                'Binary Section': POI_binary_section}
    protocol_collection.insert_one({'Analysis run': analysis_run, "POI Values": document})

def save_structs(analysis_run, POI_name, POI_structure, POI_member_order, POI_member_type, POI_member_value,
                    POI_binary_section, POI_call_address):
    global struct_collection
    document = {'Struct Name': POI_name,
                'Call From Address': POI_call_address,
                'Structure': POI_structure,
                'Member Order': POI_member_order,
                'Member Type': POI_member_type,
                'Member Value': POI_member_value,
                'Binary Section': POI_binary_section}
    struct_collection.insert_one({'Analysis run': analysis_run, "POI Values": document})

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
    project_collection.delete_one({'name': name})
    current_collection.drop()

# begin methods for adding, updating/creating, getting, and removal of data from collections
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

# return everything from a collection(points of interest) in a list format
def get_multiple_data():
    data = collection.find()
    return list(data)


def end():
    # close the connection to the database
    connection.close()

# start of main

# useful notes on database operations:
# data = {"_id": "Project 01","Name", "HP"} #how to define a user defined id *can't use the same id twice!*
# id = insert_data(data) #this will return the id auto generated by mongoDB

# edit the following variables with what was found in the static or dynamic analysis
# values that can be stored by the mongo Database are string, integer, boolean, double, Min/Max keys, arrays, timestamp,
# Object, Null, Symbol, Date, ObjectId, Binary data, javascript code and regular expressions
POI_object_ID = ""
POI_name = "POI_Temp"
POI_data_type = ""
POI_call_address = ""

POI_value = 0
POI_size = 0
POI_destination_address = ""
POI_parameter_type = ""
POI_parameter_order = ""
POI_parameter_value = ""
POI_member_type = ""
POI_member_order = ""
POI_member_value = ""
POI_return_type = ""
POI_return_value = ""
POI_binary_section = ""
POI_section_Size = 0
POI_section_value = ""
POI_structure = ""
POI_order_to_functions = ""

# test code##############################################################################################
#initialize_POI_collections("project 1")

#save_variables("static", "integer 1", 254, "integer", 256, "some random section in binary", "here lies a binary address")

#save_variables("static", "integer 2", 254, "integer", 256, "some random section in binary", "here lies a binary address")
#save_variables("dynamic", "integer 1", 254, "integer", 256, "some random section in binary", "here lies a binary address")