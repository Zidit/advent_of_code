#!/usr/bin/python
import re
import collections

def process(input):

    chars = ["", "", "", "", "", "", "", ""]

    for line in input:
        for i in range(8):
            chars[i] += line[i]

    print (chars)

    code = ""

    for i in range(8):
        count = collections.Counter(chars[i]).most_common(1)
        code += count[0][0]

    return code

with open("input.txt") as input:
    ret = process(input)
    print (ret)

# 986 too high
