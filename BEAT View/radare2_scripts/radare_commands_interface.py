#! /usr/bin/env python3

import r2pipe
import sys
sys.path.append("..")  # for data_manager
import data_manager

rlocal = None

def parse_binary(path):
    global rlocal
    rlocal = r2pipe.open(path)
    binary_info = rlocal.cmd("if")
    print(binary_info)
    binary_info = binary_info.split("\n")[:-1]
    x = dict(s.split(' ', 1) for s in binary_info)
    for k, v in x.items():
        x[k] = v.lstrip()
    rlocal.quit()
    return x

def run_static_analysis():
    global rlocal
    name, desc, path, bin_info = data_manager.getCurrentProjectInfo()
    rlocal = r2pipe.open(path, flags=['-d'])  # open in debug mode, necessary for breakpoints
    try:
        rlocal.cmd("aaa")  # analyze file
        rlocal.cmd("s main")
    except:
        pass  # fail quietly, almost always gives error when reading
    extract_all()

def run_dynamic_analysis():
    global rlocal
    try:
        #rlocal = r2pipe.open("/home/osboxes/Documents/Team01_BEAT/BEAT View/radare2_scripts/hello", flags=['-d'])  # open radare2 in debug mode
        rlocal.cmd("aaa")
    except:
        pass  # fail quietly, almost always gives error when reading
    extract_all()
    run_dynamic_and_update()

def extract_vars_from_functions():
    global rlocal
    currentAddr = rlocal.cmd("s")  # dont lose original position
    functions = data_manager.get_functions()
    for func in functions:
        funcName = func["Function Name"]
        rlocal.cmd("s " + funcName)
        variables = rlocal.cmd("afvd").split("\n")
        variableTypes = rlocal.cmd("afv").split("\n")
        for var in variables:
            attr = var.split()
            if len(attr) < 1:
                continue

            if attr[0] != "var":
                continue
            varName = attr[1]
            varAddr = attr[3]
            varValue = attr[5]
            varType = ""
            for varTemp in variableTypes:
                if varName in varTemp:
                    varType = varTemp.split()[1]
            data_manager.save_variables("static", funcName, varName, varValue, varType, varAddr)

    rlocal.cmd("s " + currentAddr)

def extract_all():
    # TODO: filter the search somehow
    extract_functions()
    extract_strings()
    # extract_imports()
    extract_vars_from_functions()
    extract_global_vars()

def extract_global_vars():
    global rlocal
    globalString = "GLOBAL"
    # print("Extracting global vars")
    glvars = rlocal.cmd("is~OBJ").split("\n")
    newVars = list()
    # print(glvars)
    # find objects that are global
    for item in glvars:
        # print("Current item: " + item)
        if item == "":  # remove empty items
            continue
        # remove any items that are not global
        elif globalString in item.split()[3]:
            newVars.append(item)

    # print(newVars)
    for v in newVars:
        attributes = v.split()
        address = attributes[2]
        size = attributes[5]
        name = attributes[6]
        data_manager.save_global_variable("static", name, size, address)


def extract_functions():
    global rlocal
    print("Entered extract functions!")
    funcs = rlocal.cmd("afl").split("\n")
    # go through every function and add to database
    for func in funcs:
        if func == "":
            print("Empty line")
            continue
        # print("Function: " + func)
        attr = func.split()
        # print(attr)

        funcName = attr[len(attr) - 1]
        rlocal.cmd("s " + funcName)
        funcHeader = rlocal.cmd("pdf~" + funcName + ":1").split()
        paramList = rlocal.cmd("afvr").split("\n")
        params = []
        paramType = []
        for p in paramList:
            if p == "":
                continue
            # add name of param
            params.append(p.split()[2])
            # add types of params
            paramType.append(p.split()[1])
        funcAddr = attr[0]
        returnType = funcHeader[1]
        # make sure function has a return type
        if returnType == funcName:
            returnType = None
        returnValue = None  # don't know the value of return until running dynamic
        data_manager.save_functions("static", funcName, returnType, returnValue, funcAddr, params, paramType)
        # funcDict = {"name": funcName, "address": funcAddr}
        # print(funcDict)
        # functioncol.insert_one(funcDict)

def extract_strings():
    global rlocal
    strings = rlocal.cmd("iz").split("\n")
    for strg in strings[2:]:
        if strg == "":
            print("Empty string")
            continue
        attr = strg.split()

        # save entire string value
        strValue = ""
        for value in attr[7:]:
            strValue = strValue + " " + value

        strSection = attr[5]
        strAddr = attr[2]
        data_manager.save_strings("static", strValue, strSection, strAddr)

def extract_imports():
    global rlocal
    try:
        rlocal.cmd("ii > imports.txt")
    except:
        print("Error extracting string")

def run_dynamic_and_update():
    rlocal.cmd("dc")
    extract_strings()
    extract_functions()
    extract_vars_from_functions()

def set_breakpoint_at_function(func_name):
    try:
        rlocal.cmd("db " + func_name)
        print("Function breakpoint successfully set at: " + func_name)
    except:
        print("Error setting breakpoint at function address: " + func_name)

def remove_breakpoint_at_function(func_name):
    try:
        rlocal.cmd("db- " + func_name)
        print("Function breakpoint successfully removed at: " + func_name)
    except:
        print("Error removing breakpoint at function address: " + func_name)

def set_breakpoint_at_strings(string_addr):
    try:
        rlocal.cmd("db " + string_addr)
        print("String breakpoint successfully set at: " + string_addr)
    except:
        print("Error setting breakpoint at string address: " + string_addr)

def set_breakpoint_for_var_inside_function(var_address):
    try:
        rlocal.cmd("db " + var_address)
        print("Var breakpoint successfully set at: " + var_address)
    except:
        print("Error setting breakpoint at var address: " + var_address)

def get_all_breakpoints():
    global rlocal
    bp = []
    try:
        bpInfo = rlocal.cmd("db")
        for bpLine in bpInfo.split("\n"):
            bpName = bpLine.split()[10]  # get the name of breakpoint
            bpName = str(bpName[6:len(bpName)-1])  # remove name= from name
            bp.append(bpName)
            print("Debug breakpoint name: " + bpName)
    except:
        print("Error getting all breakpoints")
    return bp

def display_POI_in_points_of_interest():
    print("Test")

if __name__ == "__main__":
    #pass
    import sys
    if(sys.argv[1] == 'static'):
        print("running static....")
        run_static_analysis()
    if(sys.argv[1] == 'dynamic'):
        run_dynamic_analysis()

