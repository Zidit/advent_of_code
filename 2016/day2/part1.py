#!/usr/bin/python

current_number = 5

def get_number(line):
    global current_number

    for char in line:
        if char == "U":
            if(current_number > 3 ):
                current_number -= 3
        elif char == "D":
            if(current_number < 7 ):
                current_number += 3
        elif char == "L":
            if((current_number != 1) and (current_number != 4) and (current_number != 7)):
                current_number -= 1
        elif char == "R":
            if((current_number != 3) and (current_number != 6) and (current_number != 9)):
                current_number += 1

    print (current_number)
    return current_number

def process(input):

    ret = 0

    for line in input:
        ret = ret * 10
        ret += get_number(line)

    return ret

with open("input.txt") as input:
    ret = process(input)
    print (ret)
