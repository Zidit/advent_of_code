#!/usr/bin/python
import re

def is_valid_triangle(line):
    sides = line.split()
    print (sides)
    if int(sides[0]) + int(sides[1]) <= int(sides[2]):
        return False
    elif int(sides[0]) + int(sides[2]) <= int(sides[1]):
        return False
    elif int(sides[1]) + int(sides[2]) <= int(sides[0]):
        return False
    else:
        return True


def process(input):

    ret = 0

    for line in input:
        if is_valid_triangle(line):
            ret += 1

    return ret

with open("input.txt") as input:
    ret = process(input)
    print (ret)

# 986 too high
