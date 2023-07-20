import os
import json

jsonfiles = []
for i in os.walk("out"):
    for j in i[2]:
        if j.endswith(".binE.json"):
            jsonfiles.append(i[0] + "\\" + j)

for jsonfile in jsonfiles:
    data = {}
    with open(jsonfile, "r") as o:
        data = json.load(o)
    
    ptr_length = 4 * len(data["strings"])

    for i in range(len(data["strings"])):
        if (type(data["strings"][i]) is not str):
            data["strings"][i] = data["strings"][i][0]
        data["strings"][i] = data["strings"][i] + "[end]"
    
    pointers = []
    ptr_val = len(data["header"]) + ptr_length
    for string in data["strings"]:
        pointers.append(ptr_val)
        ptr_val += len(bytes(string, encoding="utf-8"))
    
    raw = bytes(data["header"])
    for ptr in pointers:
        raw += int.to_bytes(ptr, 4, "little")
    for string in data["strings"]:
        raw += bytes(string, encoding="utf-8")
    
    with open(jsonfile[:-5], "wb") as o:
        o.write(raw)