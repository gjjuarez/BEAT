#! /usr/bin/env python3

import r2pipe
import re
rlocal = None



def run_static_analysis():
    global rlocal
    try:
        rlocal = r2pipe.open("/home/osboxes/Documents/Team01_BEAT/BEAT View/radare2_scripts/hello", flags=['-d'])  # open radare2 in debug mode
        rlocal.cmd("aaa")  # analyze file
        rlocal.cmd("s main")
    except:
        rlocal.cmd("exit")
        print("Error running static analysis")

def extract_vars_from_functions(filename):
    varFileName = "variables.txt"
    currentAddr = rlocal.cmd("s")  # dont lose original position
    try:
        with open(varFileName, 'w') as vf:
            vf.write("[Variables]\n")
        with open(filename) as f:
            with open(varFileName, 'a') as varf:
                for func in f.read().split("\n"):
                    print(func.split()[0])
                    rlocal.cmd("s " + func.split()[0])  # move to each functions offset
                    varf.write(rlocal.cmd("afvd"))
    except IOError:
        print("Error extracting variables")
    rlocal.cmd("s " + currentAddr)

def extract_all():
    print("")
    global rlocal
    try:
        extract_functions()
        extract_strings()
        extract_imports()
        extract_vars_from_functions("functions.txt")
    except:
        print("Error extracting all POI")

def extract_functions():
    global rlocal
    try:
        rlocal.cmd("afl > functions.txt")
    except:
        print("Error extracting functions")

def extract_strings():
    global rlocal
    try:
        rlocal.cmd("iz > strings.txt")
    except:
        print("Error extracting string")

def extract_imports():
    global rlocal
    try:
        rlocal.cmd("ii > imports.txt")
    except:
        print("Error extracting string")

def run_dynamic_and_update():
    try:
        rlocal.cmd("dc")
        extract_strings()
        extract_vars_from_functions("functions.txt")
    except:
        print("Error running dynamic")

def set_breakpoint_at_function(func_name):
    try:
        rlocal.cmd("db " + func_name)
        print("Breakpoint successfully set at: " + func_name)
    except:
        print("Error setting breakpoint at: " + func_name)

def remove_breakpoint_at_function(func_name):
    try:
        rlocal.cmd("db- " + func_name)
        print("Breakpoint successfully removed at: " + func_name)
    except:
        print("Error removing breakpoint at: " + func_name)

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