#!/usr/bin/python
import re
import collections
import operator

def decode(name, ID):
    decoded = ""

    for char in name:
        if char == " ":
            decoded += " "
            continue
        asc_num = (ord(char) - 97 + ID) % 26
        decoded += chr(asc_num + 97)

    return decoded

def break_line(line):
    tokens = line.split("-")

    name = ""

    for token in tokens[:-1]:
        name += token
        name += " "

    ID = int(tokens[-1].split("[")[0])
    check = tokens[-1].split("[")[1].split("]")[0]

    return (name, ID, check)

def is_valid(room):

    count = collections.Counter(room[0]).most_common()
    count = filter(lambda x: x[0] != " ", count)
    count = sorted(count, key=lambda row: row[0], reverse=False)
    count = sorted(count, key=lambda row: row[1], reverse=True)

    for i, char in enumerate(room[2]):
        if char != count[i][0]:
            return False

    return True

def process(input):

    ret = 0

    for line in input:
        room = break_line(line)
        if is_valid(room):
            name = decode(room[0], room[1])
            if "northpole" in name:
                return name, room[1]




with open("input.txt") as input:
    ret = process(input)
    print (ret)

# 986 too high
