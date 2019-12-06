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

current_plugin_name = ""

def set_current_plugin(name):
    global current_plugin_name
    current_plugin_name = name


def get_pois_from_plugin_and_type(plugin, type):
    print("in get_poits_from_plugin_and__type")
    pois = []
    print("Looking for POI from plugin:", plugin, "of type:",type)
    for c in plugin_collection.find():
        if c['name'] == plugin:
            return list(c[type])

def get_pois_from_type(type):
    pois = []
    plugin = current_plugin_name
    for c in plugin_collection.find():
        try:
            if c['name'] == plugin:
                return list(c[type])
        except:
            return None

def get_plugin_names():
    plugins = []
    for c in plugin_collection.find():
        plugins.append(str(c["name"]))
    return plugins

def save_plugin(name, desc):
    print("in save plugin")
    plugin_dict = {"name": name,
                   "desc": desc}
    plugin_collection.insert_one(plugin_dict)

def get_plugin_from_name(to_find):
    name = ""
    desc = ""
    for c in plugin_collection.find():
        print(c["name"])
        try :
            if(c["name"] == to_find):
                name = c["name"]
                desc = c["desc"]
                return name, desc
        except KeyError:
            print("Key error")

# deletes a plugin document from the database based on the name of the plugin given as a string
def delete_plugin_given_name(name):
    try:
        plugin_collection.delete_one({'name': name})
    except:
        print("Drop collection error")

# deletes a function document from the database based on the name of the point of interest given as a string
def delete_function_poi_by_name(poi_name):
    try:
        function_collection.delete_one({'name': poi_name})
    except:
        print("Delete POI function error")

# deletes a string document from the database based on the name of the point of interest given as a string
def delete_string_poi_by_name(poi_name):
    try:
        string_collection.delete_one({'name': poi_name})
    except:
        print("Delete POI string error")

# deletes a variable document from the database based on the name of the point of interest given as a string
def delete_variable_poi_by_name(poi_name):
    try:
        variable_collection.delete_one({'name': poi_name})
    except:
        print("Delete POI variable error")


def add_string_to_plugin(name, string_name):
    string = {'String Value': string_name
            }
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

def add_function_to_plugin(name, function_name, parmeter_order_and_type, return_value):
    function = {'Function Name': function_name,
               'Parameter Type and Order': parmeter_order_and_type,
               'Return Type': return_value,
               }
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"function": function}
    },upsert=True
    )

def add_variable_to_plugin(name, variable_name,variable_type):
    variable = {'Variable Name': variable_name,
                'Variable Type': variable_type,
                }
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"variable": variable}
    },upsert=True
    )

def add_dll_to_plugin(name, libaray_name):
    dll = {'Library': libaray_name
           }
    plugin_collection.find_one_and_update(
    {'name' : name},
    {"$push":
        {"dll": dll}
    },upsert=True
    )

def delete_poi_given_plugin_poitype_and_poi(plugin, type, poi):
    print("in get_poits_from_plugin_and__type")
    pois = []
    print("Looking for POI from plugin:", plugin, "of type:",type)
    print("------------------------------------", type)
    if type == 'DLL':
        print("lllllllllllllllllllllllllllllllllllllllllllllllllllll", poi)
        plugin_collection.update(
            {'name': plugin},
            {'$pull':
                 {'dll': {'Library': poi}}
             }
        )
    elif type == 'Function':
        print("lllllllllllllllllllllllllllllllllllllllllllllllllllll", poi)
        plugin_collection.update(
            {'name': plugin},
            {'$pull':
                 {'function': {'Function Name': poi}}
             }
        )
    elif type == 'String':
        print("lllllllllllllllllllllllllllllllllllllllllllllllllllll", poi)
        plugin_collection.update(
            {'name': plugin},
            {'$pull':
                 {'string': {'String Value': poi}}
             }
        )
    elif type == 'Variables':
        print("lllllllllllllllllllllllllllllllllllllllllllllllllllll", poi)
        plugin_collection.update(
            {'name': plugin},
            {'$pull':
                 {'variable': {'Variable Name': poi}}
             }
        )


'''
#################################################################################
Project functions
#################################################################################
'''

variable_collection = None
string_collection = None
function_collection = None  #libraries (imports) included in this collection
global_var_collection = None

#Creates the database base on the project_name (string) and the collections for the different points of interst types (variable, global variable, function, and string)
#they do not already exist.
def initialize_POI_collections(project_name):
    global variable_collection
    global string_collection
    global function_collection
    global global_var_collection
    global database

    varName = project_name + "Variables"
    stringName = project_name + "Strings"
    functionName = project_name + "Functions"
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

    if globalVarName not in database.list_collection_names():
        database.create_collection(globalVarName)
    global_var_collection = database[globalVarName]

#Pulls all the projects saved to the database
def get_project_names():
    projects = []
    for c in project_collection.find():
        projects.append(str(c["name"]))
    return projects

#returns all the variable POIs within a given collection in a list format
def get_variable_POIs():
    data = variable_collection.find()
    return list(data)

#returns all the string POIs within a given collection in a list format
def get_string_POIs():
    data = string_collection.find()
    return list(data)

#returns all the function POIs within a given collection in a list format
def get_Function_POIs():
    data = function_collection.find()
    return list(data)

#saves a project document with a name, description, file path, and binary info
def save_project(name, desc, path, binary_info):
    project_dict = {"name": name,
                    "desc": desc,
                    "path": path,
                    "bin_info": binary_info}
    project_collection.insert_one(project_dict)

#saves a variable document with the type of analysis run on it, the function name, name of the point of interest,
# value of the point of intest, point of interest data type, comments based on the specific point of interest, and
# the name of the analysis the result is tied to. *Note Comment and Analysis Name are initially left blank as they are
# populated later with add_comment and add_analysis_name methods*.
def save_variables(analysis_run, function_name, POI_name, POI_value, POI_data_type, address):
    global variable_collection
    document = {'Analysis Run': analysis_run,
                'Function Name': function_name,  # to reference parent, avoid conflicting names
                'Variable Name': POI_name,
                'Variable Value': POI_value,
                'Variable Type': POI_data_type,
                'Address': address,
                'Comment': "",
                'Analysis Name': ""}
    variable_collection.replace_one({'Function Name': function_name,
                                     'Variable Name': POI_name,
                                     'Analysis Run': analysis_run}, document, upsert=True)

#saves a global variable document with the type of analysis run on it, the size of the point of interest, name of the point of interest,
# value of the point of interest, address of the point of interest, comments based on the specific point of interest, and
# the name of the analysis the result is tied to. *Note Comment and Analysis Name are initially left blank as they are
# populated later with add_comment and add_analysis_name methods*.
def save_global_variable(analysis_run, POI_name, POI_size, address, POI_value="", comment=""):
    global global_var_collection
    document = {'Analysis Run': analysis_run,
                'Variable Name': POI_name,
                'Variable Value': POI_value,
                'Variable Size': POI_size,
                'Address': address,
                'Comment': comment,
                'Analysis Name': ""}
    global_var_collection.replace_one({'Variable Name': POI_name}, document, upsert=True)

#returns all the global variables found in the database
def get_global_variables():
    global global_var_collection
    variables = []
    for var in global_var_collection.find():
        variables.append(var)
    return variables

#returns all the variables found in the database
def get_variables():
    global variable_collection
    variables = []
    for var in variable_collection.find():
        variables.append(var)
    return variables

#finds a variable based on the name (string)
def get_variable_from_name(find_variable):
        name = ""
        for c in variable_collection.find():
            try:
                if (c["Variable Name"] == find_variable):
                    name = c["Variable Name"]
                    return name
            except KeyError:
                print("Key error")

#finds a local variables from a function based on the functions name (string)
def get_local_variables_from_function(func_name):
    localVars = []
    query = {"Function Name": func_name}
    for c in variable_collection.find(query):
        localVars.append(c)
    return localVars

#saves a string document with the type of analysis run on it, the value of the point of interest, section the point of
# interest is in, address of the point of interest, comments based on the specific point of interest, and
# the name of the analysis the result is tied to. *Note Comment and Analysis Name are initially left blank as they are
# populated later with add_comment and add_analysis_name methods*.
def save_strings(analysis_run, POI_value, section, address, comment=''):
    global string_collection
    document = {'Analysis Run': analysis_run,
                'String Value': POI_value,
                'Section': section,
                'Address': address,
                'Comment': comment,
                'Analysis Name': ""}
    string_collection.replace_one({'String Value': POI_value}, document, upsert=True)

#gets all the strings in the database
def get_strings():
    global string_collection
    strings = []
    for strg in string_collection.find():
        strings.append(strg)
    return strings

def get_all_plugin_strings():
    global current_plugin_name
    for c in plugin_collection.find():
        try:
            if (c["name"] == current_plugin_name):
                strings = []
                for s in c["strings"]:
                    strings.append(c["strings"])
                return strings
        except KeyError:
            print("Key error")

#finds a string based on the name given (string)
def get_string_from_name(find_string):
    name = ""
    for c in string_collection.find():
        try:
            if (c["String Value"] == find_string):
                name = c["String Value"]
                return name
        except KeyError:
            print("Key error")

#saves a function document with the type of analysis run on it, the name of the point of interest, return type of the point of interest,
# return value of the point of interest, destination address of the point of interest, address of the point of interest,
# parameter order of function, type parameters of the function, the section in binary the funtcion is in, value of the parameters,
# where the function is being called from, if the function has a breakpoint, comments based on the specific point of interest,
# and the name of the analysis the result is tied to. *Note Comment and Analysis Name are initially left blank as they are
# populated later with add_comment and add_analysis_name methods*.
def save_functions(analysis_run, POI_name, POI_return_type, POI_return_value, POI_address,
                   POI_parameter_order, POI_parameter_type, dest_address, hasBreakpoint, call_from=None,
                   POI_parameter_values=None, binary_section="", comment=""):
    if call_from is None:
        call_from = []
    if POI_parameter_values is None:
        POI_parameter_values = []
    global function_collection
    document = {'Analysis Run': analysis_run,
                'Function Name': POI_name,
                'Return Type': POI_return_type,
                'Return Value': POI_return_value,
                'Destination Address': dest_address,
                'Address': POI_address,
                'Parameter Order': POI_parameter_order,
                'Parameter Type': POI_parameter_type,
                'Binary Section': binary_section,
                'Parameter Value': POI_parameter_values,
                'Call From': call_from,  # either a function name or address
                'Comment': comment,
                'Breakpoint': hasBreakpoint,  # boolean value
                'Analysis Name': ""
                }
    function_collection.replace_one({"Function Name": POI_name, 'Analysis Run': analysis_run}, document, upsert=True)

#finds a function based on the function name given (string)
def get_function_from_name(find_function):
    name = ""
    for c in function_collection.find():
        try:
            if (c["Function Name"] == find_function):
                name = c["Function Name"]
                return name
        except KeyError:
            print("Key error")

#gets all the functions from the database
def get_functions():
    global function_collection
    functions = []
    for func in function_collection.find():
        functions.append(func)
    return functions

#updates the current project by deleting the old one and relpaceing the values of name, description, file path, and binary info
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

#find a project based on the name given (string)
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

#delete an entire project by dropping all collections based on the name of the project (string)
def delete_project_given_name(name):
    try:
        project_collection.delete_one({'name': name})
        current_collection.drop()

        function_collection.drop()
        string_collection.drop()
        variable_collection.drop()
    except:
        print("Drop collection error")

#delete only the function collection
def delete_function_collection():
    try:
        function_collection.drop()
    except:
        print("Drop function collection error")

#delete only the string collection
def delete_string_collection():
    try:
        string_collection.drop()
    except:
        print("Drop string collection error")

#delete only the variable collection
def delete_variable_collection():
    try:
        variable_collection.drop()
    except:
        print("Drop variable collection error")

#adds a comment by name for the point of interest type
def add_comment(POI_name, poi_type, comment):

    if poi_type == "function":
        global function_collection
        function_collection.update_one({"Function Name": POI_name}, {"$set": {"Comment": comment}})
    if poi_type == "struct":
        global struct_collection
        struct_collection.update_one({"Struct Name": POI_name}, {"$set": {"Comment": comment}})
    if poi_type == "variable":
        global variable_collection
        variable_collection.update_one({"Variable Name": POI_name}, {"$set": {"Comment": comment}})
    if poi_type == "protocol":
        global protocol_collection
        protocol_collection.update_one({"Protocol Name": POI_name}, {"$set": {"Comment": comment}})
    if poi_type == "string":
        global string_collection
        string_collection.update_one({"String Value": POI_name}, {"$set": {"Comment": comment}})


# This function is brute forced. At the moment I coul not find a function that would let me
# know the type of POI selected, only its name
def get_comment_from_name(POI_name):
    comment = ""
    functions = get_functions()
    for func in functions:
        try:
            print(str(func["Function Name"]))
            if (func["Function Name"] == POI_name):
                comment = str(func["Comment"])
                return comment, "function"
        except KeyError:
            print("Key error")
            print("in function")

    variables = get_variables()
    for var in variables:
        try:
            print(str(var["Variable Name"]))
            if (var["Variable Name"] == POI_name):
                comment = str(var["Comment"])
                return comment, "variable"
        except KeyError:
            print("Key error")
            print("in var")

    strings = get_strings()
    for s in strings:
        try:
            if (s["String Value"] == POI_name):
                comment = str(s["Comment"])
                return comment, "string"
        except KeyError:
            print("Key error")
            print("in string")

    return "", "function"

#finds all POIs without an analysis assigned to them and gives them the analysis_name
def add_analysis_name(analysis_name):
    name =""
    global variable_collection
    global function_collection
    global string_collection

    for c in variable_collection.find():
        variable_collection.update_one({'Analysis Name': name} ,{ "$set":{'Analysis Name': analysis_name}})
    for d in function_collection.find():
        function_collection.update_one({'Analysis Name': name}, {"$set": {'Analysis Name': analysis_name}})
    for e in string_collection.find():
        string_collection.update_one({'Analysis Name': name}, {"$set": {'Analysis Name': analysis_name}})

#gets the all POIs based on the analysis_name given (if given an empty string will return all POIs not assigned to an analysis)
def find_analysis(analysis_name):
        global variable_collection
        global function_collection
        global string_collection

        for c in variable_collection.find():
            variable = variable_collection.find({'Analysis Name': analysis_name})
        for d in variable_collection.find():
            function = function_collection.find({'Analysis Name': analysis_name})
        for e in variable_collection.find():
            string = string_collection.find({'Analysis Name': analysis_name})

        return variable, function, string

#sets all POIs with the defined analysis name to a blank string to be either renamed or removed from the analysis
def delete_analysis_by_name(analysis_name):
    name =""
    global variable_collection
    global function_collection
    global string_collection

    for c in variable_collection.find():
        variable_collection.update_one({'Analysis Name': analysis_name} ,{ "$set":{'Analysis Name': name}})
    for d in variable_collection.find():
        function_collection.update_one({'Analysis Name': analysis_name}, {"$set": {'Analysis Name': name}})
    for e in variable_collection.find():
        string_collection.update_one({'Analysis Name': analysis_name}, {"$set": {'Analysis Name': name}})

# close the connection to the database
def end():
    connection.close()

# test code##############################################################################################
#initialize_POI_collections("project 1")

#save_variables("static", "integer 1", 254, "integer", 256, "some random section in binary", "here lies a binary address")

#save_variables("static", "integer 2", 254, "integer", 256, "some random section in binary", "here lies a binary address")
#save_variables("dynamic", "integer 1", 254, "integer", 256, "some random section in binary", "here lies a binary address")
