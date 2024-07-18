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
code = ""

for i in range(8):
    next_index, hash = find_next(next_index)
    print(hash, next_index)
    code += hash[5]

print (code)

# 986 too high
