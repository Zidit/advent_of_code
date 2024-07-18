#!/usr/bin/python
import re

def is_valid_triangle(sides):
    print (sides)
    if int(sides[0]) + int(sides[1]) <= int(sides[2]):
        return False
    elif int(sides[0]) + int(sides[2]) <= int(sides[1]):
        return False
    elif int(sides[1]) + int(sides[2]) <= int(sides[0]):
        return False
    else:
        return True

def colums_to_rows(three_lines):
    print (three_lines)
    l0 = three_lines[0].split()
    l1 = three_lines[1].split()
    l2 = three_lines[2].split()

    num_of_valids = 0

    if is_valid_triangle([l0[0], l1[0], l2[0]]):
        num_of_valids += 1
    if is_valid_triangle([l0[1], l1[1], l2[1]]):
        num_of_valids += 1
    if is_valid_triangle([l0[2], l1[2], l2[2]]):
        num_of_valids += 1

    return num_of_valids



def process(input):

    ret = 0

    while True:

        three_lines = []

        for i in range(3):
            line = input.readline()
            if line == '':
                break
            else:
                three_lines.append(line)

        if three_lines == []:
            break

        ret +=colums_to_rows(three_lines)

    return ret

with open("input.txt") as input:
    ret = process(input)
    print (ret)
