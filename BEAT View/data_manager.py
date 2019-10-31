#! /usr/bin/env python3

# database_operations.py version 1.1
import pymongo
from bson import ObjectId

# Data will be stored in the following format on the mongo Database
# database = project selected
# collection = the POI selected (String, struct, etc.)
# document = data related to the POI (type, size, etc.)

# connect to database on a local machine
connection = pymongo.MongoClient('localhost',27017)

# create database
current_database = 'BEAT_Database' # change string ('temp') here to make a new database for each project***
database = connection[current_database]

# create a collection for each point of interest
POI_collection = database['POIs']# change string ('placeholder') here to make a new collection for each point of interest***
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

# used to change the type of data entered into the database via the if/else statements below
poi_type = "variable" # change "variable" to variable, string, library, function, packet, or struct depding on the type
                      # of data to be entered into the database *note struct not yet implemented*

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

def POI_type_selector():
    #take in something then if else to select the proper method
    #POI_name = something
    #POI_call_address = something
    #POI_data_type =

    #selects which method to run to store POI values
    if POI_data_type == "variable": #variable
        POI_variable()
    elif POI_data_type == "string":
        POI_string()
    elif POI_data_type == "library":
        POI_library()
    elif POI_data_type == "function":
        POI_function()
    elif POI_data_type == "protocol":
        POI_protocol()
    elif POI_data_type == "struct":
        POI_struct()

# methods that handle the POI values to be stored
def POI_variable():
    document = POI_collection.insert_many([{
                'Variable Name': POI_name,
                'Variable Value': POI_value,
                'Variable Type': POI_data_type,
                'Variable Size': POI_size,
                'Bianry Section': POI_binary_section,
                'Call From Address': POI_call_address}])

def POI_string():
    document = POI_collection.insert_many([{
                'String Name': POI_name,
                'String Value': POI_value,
                'String Type': POI_data_type,
                'String Size': POI_size,
                'Call From Address': POI_call_address,
                'Destination Address': POI_destination_address,
                'Section': POI_binary_section}])

def POI_library():
    document = POI_collection.insert_many([{
                'Library Name': POI_name,
                'Parameter Order': POI_parameter_order,
                'Parameter Type': POI_parameter_type,
                'Parameter Value': POI_parameter_value,
                'Return Type': POI_return_type,
                'Return Value': POI_return_value,
                'Call From Address': POI_order_to_functions}])

def POI_function():
    document = POI_collection.insert_many([{
                'Function Name': POI_name,
                'Function Value': POI_value,
                'Return Type': POI_return_type,
                'Return Value': POI_return_value,
                'Call From Address': POI_call_address,
                'Destination Address': POI_destination_address,
                'Binary Section': POI_binary_section}])

def POI_protocol():
    document = POI_collection.insert_many([{
                'Protocol Name': POI_name,
                'Call From Address': POI_call_address,
                'Structure': POI_structure,
                'Section Size': POI_section_Size,
                'Section Value': POI_section_value,
                'Binary Section': POI_binary_section}])

def POI_struct():
    document = POI_collection.insert_many([{
                'Struct Name': POI_name,
                'Call From Address': POI_call_address,
                'Structure': POI_structure,
                'Member Order': POI_member_order,
                'Member Type': POI_member_type,
                'Member Value': POI_member_value,
                'Binary Section': POI_binary_section}])