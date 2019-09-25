#! /usr/bin/env python3

import r2pipe

rlocal = r2pipe.open("bubblesort", flags=['-d'])  # Open ping in Radare2 in debug mode
rlocal.cmd("aa")  # analyze all functions
number_import = rlocal.cmd("ii~[0]")
number_import = number_import.split()
addresses = rlocal.cmd("ii~[1]")
addresses = addresses.split()
binds = rlocal.cmd("ii~[2]")
binds = binds.split()
types = rlocal.cmd("ii~[3]")
types = types.split()
names = rlocal.cmd("ii~[4]")
names = names.split()

for impor, addr, bind, type, name in zip(number_import, addresses, binds, types, names):
    # rlocal.cmd("db " + addr)
    print(impor, addr, bind, type, name)
print("Done")
inp = input("$ ")
while inp != "exit":
    rlocal.cmd(inp)
    inp = input("$ ")
