#!/usr/bin/python

import sys


def decode(string, depth):


    length = 0
    pos = 0

    print(depth)

    while 1:

        start = string.find("(", pos)
        if start == -1:
            break
        stop = string.find(")", start)

        length += start - pos

        tokens = string[start + 1 : stop].split("x")
        length += decode(string[stop + 1: stop + 1 + int(tokens[0])], depth + 1) * int(tokens[1])

        pos = stop + 1 + int(tokens[0])

    length += len(string[pos :].strip())

    return length


def process(input):

    for line in input:
        length = decode(line, 0)

    return length


with open("input.txt") as input:
    ret = process(input)
    print (ret)


#11451628996 too high
