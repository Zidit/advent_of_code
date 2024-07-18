#!/usr/bin/python

import sys

registers = {'a':0, 'b':0, 'c':0, 'd':0}

def run_cmd(line):
    global registers
    tokens = line.split()
#    print (line)

    if tokens[0] == "cpy":
        if tokens[1].isnumeric():
            registers[tokens[2]] = int(tokens[1])
        else:
            registers[tokens[2]] = registers[tokens[1]]
        return 1

    elif tokens[0] == "inc":
        registers[tokens[1]] += 1
        return 1

    elif tokens[0] == "dec":
        registers[tokens[1]] -= 1
        return 1

    elif tokens[0] == "jnz":
        if tokens[1].isnumeric():
            if int(tokens[1]) != 0:
                return int(tokens[2])
        elif registers[tokens[1]] != 0:
            return int(tokens[2])
        else:
            return 1

    else:
        print ("error" + line)

def process(input):

    code = []

    for line in input:
        code.append(line.strip())

    pc = 0
    while pc < len(code):
        pc += run_cmd(code[pc])
        #print(registers)
        #print(pc)
        #print("")

    return registers["a"]


with open("input.txt") as input:
    ret = process(input)
    print (ret)
