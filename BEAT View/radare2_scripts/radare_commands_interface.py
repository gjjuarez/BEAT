#! /usr/bin/env python3

import r2pipe
import re
rlocal = None



def run_static_analysis():
    global rlocal
    rlocal = r2pipe.open("/bin/ping")
    #rlocal = r2pipe.open("/bin/ping")  # Open ping in Radare2 in debug mode
    try:
        rlocal.cmd("aaa")  # analyze file
    except:
        print("Error running static analysis")
    extract_all()


def extract_strings():
    global rlocal
    try:
        for string in rlocal.cmd("iz").split("\n"):
            print(string)
    except:
        print("Error extracting strings")

def extract_vars_from_functions(filename):
    varFileName = "variables.txt"
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

def extract_all():
    print("")
    global rlocal
    try:
        rlocal.cmd("afl > functions.txt")
        rlocal.cmd("iz > strings.txt")
        rlocal.cmd("ii > imports.txt")
        # rlocal.cmd("s main")
        extract_vars_from_functions("functions.txt")
        # rlocal.cmd("afvd > variables.txt")
    except:
        print("Error extracting all POI")


def display_POI_in_points_of_interest():
    print("Test")

if __name__ == "__main__":
    run_static_analysis()