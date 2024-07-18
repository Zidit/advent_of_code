#!/usr/bin/python

import sys


def decode(string):
    decoded_string = ""

    pos = 0

    while 1:
        print(pos)
        start = string.find("(", pos)
        if start == -1:
            break
        stop = string.find(")", start)

        decoded_string += string[pos : start]
        tokens = string[start + 1 : stop].split("x")

        for i in range(int(tokens[1])):
            decoded_string += string[stop + 1: stop + 1 + int(tokens[0])]

        print (string[stop + 1: stop + 1 + int(tokens[0])])

        pos = stop + 1 + int(tokens[0])

    decoded_string += string[pos :]

    return decoded_string


def process(input):

    for line in input:
        decoded = decode(line)



    decoded = decoded.replace(" ", "")
    decoded = decoded.replace("\r", "")
    decoded = decoded.replace("\n", "")
    print (decoded)
    return len(decoded)


with open("input.txt") as input:
    ret = process(input)
    print (ret)

    #print(decode("X(8x2)(3x3)ABCY"))
    #print(decode("A(2x2)BCD(2x2)EFG"))

#115574 too high
#11214 too low
