#! /usr/bin/env python3

import r2pipe
import sys
from . import filter
sys.path.append("..")  # for data_manager
import data_manager

rlocal = None
def run_cmd(cmd):
    print("running cmd", cmd)
    global rlocal
    return rlocal.cmd(cmd)

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

            # skip parameters
            if attr[0] != "var":
                continue
            varName = attr[1]
            varAddr = attr[3]
            varValue = attr[5]
            varType = ""
            for varTemp in variableTypes:
                if varName in varTemp:
                    varType = varTemp.split()[1]
            if filter.filter_var(varName, varType):
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
    currentAddr = rlocal.cmd("s")
    # print(newVars)
    for v in newVars:
        attributes = v.split()
        address = attributes[2]
        size = attributes[5]
        name = attributes[6]
        value = "-1"
        try:
            rlocal.cmd("s " + str(address))
            value = rlocal.cmd("pch~0x[0]:0").strip("\n")  # get the value
        except:
            print("Problem getting value of global variable")

        if filter.filter_var(name, ""):
            data_manager.save_global_variable("static", name, size, address, value)

    rlocal.cmd("s " + currentAddr)  # revert to previous address


def extract_functions():
    global rlocal
    print("Entered extract functions!")
    funcs = rlocal.cmd("afl").split("\n")
    currentAddr = rlocal.cmd("s")
    # go through every function and add to database
    for func in funcs:
        if func == "":
            # print("Empty line")
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
        # print(returnType)
        # print(funcHeader)
        # make sure function has a return type
        if returnType == funcName or funcName not in funcHeader:
            returnType = None

        regValue = rlocal.cmd("pdf~eax").split("\n")
        regValue = regValue[0:len(regValue) - 1]
        # check if return exists in eax register
        if len(regValue) > 0:
            # print("List")
            # print(regValue)
            cols = regValue[len(regValue)-1].split()
            lastCol = len(cols)-1
            # if return value is determined at runtime use register value, should be 0x00 before running
            if "[" in cols[lastCol]:
                returnValue = rlocal.cmd("aer eax").split("\n")[0]
            elif "eax" in cols[lastCol] or "mov" not in regValue[len(regValue)-1]:
                returnValue = None
            else:
                returnValue = cols[lastCol]
        else:
            regValue = rlocal.cmd("pdf~rax,").split("\n")
            regValue = regValue[0:len(regValue)-1]
            # print("List")
            # print(regValue)
            if len(regValue) == 0:
                returnValue = None
            # if return value is determined at runtime use register value, should be 0x00 before running
            elif "[" in regValue:
                returnValue = rlocal.cmd("aer rax").split("\n")[1]
            else:
                cols = regValue[len(regValue)-1].split()
                lastCol = len(cols) - 1
                lastValue = len(regValue) - 1
                # print(regValue)
                # make sure rax is used as return value
                if "rax" in cols[lastCol]:
                    returnValue = None
                elif ";" in regValue[lastValue]:
                    cols = regValue[lastValue].split(";")
                    returnValue = cols[len(cols)-1]
                elif "lea" not in regValue[lastValue]:
                    returnValue = None
                else:
                    returnValue = cols[lastCol]

        #print("Return value: ")
        #print(returnValue)

        # print("Return value: " + returnValue)
        # (aer eax) or (aer rax) - to check return register value during dynamic

        # get return address of function
        returnAddresses = rlocal.cmd("pdf~ret").split("\n")

        returnAddr = None
        # make sure return address exists
        if len(returnAddresses) > 1:
            returnAddrLine = returnAddresses[len(returnAddresses) - 2].split()
            for item in returnAddrLine:
                if "0x" in item:
                    returnAddr = item
                    break

        # get all xrefs TO the current function
        # include caller names, addresses, and reference types
        callFromList = rlocal.cmd("axt @" + funcName + ";~[0-2]").split("\n")
        # last item in list is always empty string, ignore it
        callFromList = callFromList[0:len(callFromList)-1]

        # check if there are no calls
        callFrom = []
        for call in callFromList:
            # calls are in format: main 0x5602c691e160 [CALL]
            cols = call.split()
            callFrom.append(cols[0] + " " + cols[1])

        # get parameter values if parameters exist
        # print(funcName)
        # print(params)
        paramVal = []
        if len(params) > 0:
            values = rlocal.cmd("afvd~arg").split("\n")
            # print(values)

            for val in values:
                # print(val)
                if val == "":
                    continue
                val = val.split()

                # get value of param
                # use px [numBytes] @[rsi/rdi/rax] to get value during dynamic
                hexVal = val[len(val)-1]

                # check if value is given for param in radare2 or empty
                if "=" == hexVal:  # no value exists, radare2 can't get a value
                    paramVal.append("n/a")
                    continue
                elif "0x" not in hexVal:  # value is at different index
                    hexVal = val[4]  # should be value in hex
                paramVal.append(hexVal)
                # print("Parameter Value: " + hexVal)

        # get section in binary
        # in format of:
        # Nm Paddr       Size Vaddr           Memsz Perms    Checksum    Name
        # 00 0x00001050   417 0x556ae87f9050   417  -r-x      0x1234    .text
        # Checksum is usually empty
        section = rlocal.cmd("iS.~:2").strip("\n")
        if len(section) < 1:
            sectionName = "n/a"
        else:
            sectionArray = section.split()
            sectionName = sectionArray[len(sectionArray)-1]
        # print(sectionName)

        data_manager.save_functions("static", funcName, returnType, returnValue, funcAddr,
                                    params, paramType, returnAddr, callFrom, paramVal, sectionName)
    rlocal.cmd("s " + currentAddr)

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
        # filter out strings
        if filter.filter_string(strValue):
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

def dynamicAnalysis():
    functions = data_manager.get_functions()
    # infile = r2pipe.open(filePath, ['-d', '-e', 'dbg.profile=profile.rr2']) #open file, will do only once
    global rlocal
    #rlocal= r2pipe.open("/home/krunkcoco/PycharmProjects/Team01_BEAT/BEAT View/radare2_scripts/hello", flags=['-d'])
    # infile.cmd('e dbg.profile=robot.rr2')  # this line should configure things properly should input be required
    #rlocal.cmd("aaa") # entire analysis is needed for full functionality
    progress = [] # empty list to attach things too
    #rlocal.cmd("ood")
    for func in functions: # iterate over list of functions
        curntFunc = func['Function Name']
        progress.append("Function Name:")
        progress.append(curntFunc)
        rlocal.cmd("s " + curntFunc)
        # rlocal.cmd("ood")   # open in debug mode
        breakpointString = "db " + str(curntFunc)
        rlocal.cmd(breakpointString) # first set the breakpoint
        rlocal.cmd("dc")    # continue to run until breakpoint is hit, there may be some input required which still not sure where to pass it
        progress.append("Hit breakpoint @ " + curntFunc)
        argsnvar = rlocal.cmd("afvd")   # get args and local vars at this point
        progress.append("----------Initial Values of Args and Variables----------")
        progress.append(argsnvar)   # put args on list
        # rlocal.cmd("dcr")   # continue execution until return call
        returnvals = rlocal.cmd("afvd")#values at the end
        progress.append("----------Final Values of Args and Variables----------")
        progress.append(returnvals)     # end values
        stack = rlocal.cmd("x@rsp")     # peek in the stack, some other values may be elswhere will have to modify
        # progress.append("----------STACK----------")
        # progress.append(stack)  # add stack to list
        rax = rlocal.cmd("dr rax")#return value
        progress.append("----------RETURN VALUE----------")
        progress.append(rax)    # put in list
        progress.append("--------------------------------")
        # at this point process is done so the breakpoint needs to be removed for next thing
        # rlocal.cmd("db-*")  # remove all breakpoints
    return progress

if __name__ == "__main__":
    #pass
    import sys
    if(sys.argv[1] == 'static'):
        print("running static....")
        run_static_analysis()
    if(sys.argv[1] == 'dynamic'):
        run_dynamic_analysis()
