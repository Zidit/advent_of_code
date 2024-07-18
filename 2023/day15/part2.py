import math
import time
import re

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [x for x in data[0].split(",")]
#print(data)

def hash(data:str):
    current_value = 0
    for c in data:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value



hashmap = {i:{} for i in range(256)}

for d in data:
    m = re.match("(\w*)(=|-)(.*)", d).groups()
    #print(m.groups())
    h = hash(m[0])

    if m[1] == "=":
        hashmap[h][m[0]] = int(m[2])
    else:
        if m[0] in hashmap[h]:
            del hashmap[h][m[0]]

    #print(h)

print(hashmap)

total = 0
for k, v in hashmap.items():
    for s, l in enumerate(v.values()):
        focus = (k + 1) * (s + 1) *  l
        total += focus
        #print(focus)


print(total)