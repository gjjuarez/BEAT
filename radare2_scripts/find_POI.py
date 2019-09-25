#! /usr/bin/env python3

import r2pipe
import re

rlocal = r2pipe.open("/bin/ping", flags=['-d'])  # Open ping in Radare2 in debug mode
rlocal.cmd("aaa")  # analyze file

addresses = rlocal.cmd("afl~[0]")  # get all the addresses of functions
addresses = addresses.split()
for addr in addresses:
    rlocal.cmd("db " + addr)  # set breakpoint at every address
    print(addr)
for bp in rlocal.cmdj("dbj"):
    print(bp)
print("----------------Done with breakpoints----------------")
if input("$ Continue? (y/n)") == "n":
    exit()

for func in rlocal.cmdj("aflj"):
    print(func)
print("----------------Done with functions----------------")
if input("$ Continue? (y/n)") == "n":
    exit()

rlocal.cmd("s main")
for var in rlocal.cmd("afvd").split("\n"):
    print(var)
print("----------------Done with variables in main----------------")
if input("$ Continue? (y/n)") == "n":
    exit()

for string in rlocal.cmd("iz").split("\n"):
    print(string)
print("----------------Done with strings----------------")
if input("$ Continue? (y/n)") == "n":
    exit()

for imp in rlocal.cmdj("iij"):
    print(imp)
print("----------------Done with imports----------------")
print("All done. Continue debugging using radare2 commands. Type exit to quit.")

inp = input("$ ")
while inp != "exit":
    rlocal.cmd(inp)
    inp = input("$ ")
