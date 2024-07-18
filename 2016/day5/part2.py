#!/usr/bin/python
import re
import md5

input = "uqwqemis"

def find_next(index):

    while True:
        hash = md5.new(input + str(index)).hexdigest()
        #print (hash[:2])
        index += 1
        if hash[:5] == "00000":
            return index,hash


next_index = 0
code = "xxxxxxxx"

while True:
    next_index, hash = find_next(next_index)
    print(hash, next_index)

    pos = int(hash[5], 16)
    char = hash[6]

    if pos >= 0 and pos <  8:
        if code[pos] == "x":
            #code[pos] = char
            code = code[:pos] + char + code[pos+1:]
    print (code)

    if "x" not in code:
        break

print (code)

# 986 too high
