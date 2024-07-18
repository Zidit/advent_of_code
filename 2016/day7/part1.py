#!/usr/bin/python
import re
import collections

test = ["ioxxoj[asdfgh]zxcvbn"]

def tokenize(line):
    line = line.replace("[", " ")
    line = line.replace("]", " ")

    return line.split()

def test_ABBA(token):
    for i in range(len(token) - 3):
        #print(token[i : i + 2], token[i + 2 : i + 4][::-1])
        if token[i : i + 2] == token[i + 2 : i + 4][::-1]:
            if token[i] != token[i + 1]:
                print(token[i : i + 2], token[i + 2 : i + 4][::-1])
                return True

    return False

def test_TLS(IP):
    print (IP)
    for hyper in IP[1::2]:
        print("hyper", hyper)
        if test_ABBA(hyper):
            return False

    for ip in IP[::2]:
        print("IP", ip)
        if test_ABBA(ip):
            return True

    return False

def process(input):

    TLS_support = 0
    total_lines = 0

    for line in input:
        total_lines += 1
        IP = tokenize(line)
        if test_TLS(IP):
            TLS_support += 1

    return TLS_support, total_lines

with open("input.txt") as input:
    ret = process(input)
    print (ret)

# 93 too low
#108 too high
