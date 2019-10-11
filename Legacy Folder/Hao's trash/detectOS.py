import platform

current_OS = platform.system()

if current_OS == "Windows":
    print("Satya")
elif current_OS == "Linux":
    print("Unix bish")
else: 
	print("This tool is not supported by your current Operating system." + "\n" + "Try using BEAT on Windows or Linux.")