#!/usr/bin/python
import re
import collections

test = ["ioxxoj[asdfgh]zxcvbn"]

def tokenize(line):
    line = line.replace("[", " ")
    line = line.replace("]", " ")

    return line.split()

def test_ABA(token, hypernet):
    for i in range(len(token) - 2):
        if token[i] == token[i + 2] and token[i] != token[i + 1]:
            print (token[i : i + 3])
            bab = token[i + 1] + token[i] + token[i + 1]
            for net in hypernet:
                if net.find(bab) != -1:
                    return True

    return False

def test_SSL(IP):
    print (IP)
    for supernet in IP[::2]:
        print("IP", supernet)
        if test_ABA(supernet, IP[1::2]):
            return True

    return False

def process(input):

    SSL_support = 0
    total_lines = 0

    for line in input:
        total_lines += 1
        IP = tokenize(line)
        if test_SSL(IP):
            SSL_support += 1

    return SSL_support, total_lines

with open("input.txt") as input:
    ret = process(input)
    print (ret)

# 31 too low
