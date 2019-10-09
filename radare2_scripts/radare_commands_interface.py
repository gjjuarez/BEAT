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
        print("")


def extract_strings():
    global rlocal
    try:
        for string in rlocal.cmd("iz").split("\n"):
            print(string)
    except:
        print("")


def extract_all():
    print("")
    global rlocal
    try:
        rlocal.cmd("afl > functions.txt")
        rlocal.cmd("iz > strings.txt")
        rlocal.cmd("ii > imports.txt")



        #for string in rlocal.cmd("iz").split("\n"):
            #print(string)

        #for imp in rlocal.cmdj("iij"):
            #print(imp)

        #rlocal.cmd("s main")
        #for var in rlocal.cmd("afvd").split("\n"):
            #print(var)
    except:
        print("THey dont pay me enough")
