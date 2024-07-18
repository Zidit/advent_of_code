import math
import functools
import time
import re

input_file = "example.txt"
#input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [line.strip().split(" ") for line in data]
data = [(line[0], [int(i) for i in line[1].split(",")]) for line in data]
#data = [((line[0] + "?") * 5, line[1] * 5) for line in data]

#print(data)


def is_valid(line:str, check:str):
    #check = [int(i) for i in check.split(",")]
    damaged = [len(v) for v in line.split(".") if len(v)]
    return damaged == check

def line_iter(line:str):
    if "?" in line:
        yield from line_iter(line.replace("?", ".", 1))
        yield from line_iter(line.replace("?", "#", 1))
    else:
        yield line



def test_line(line:str, res:list[int], stage=0):
    #print(f"Test {stage}: ", line, res)

    current_springs = 0
    matches = 0
    split_point = 0

    for i, c in enumerate(line):
        if c == "#":
            current_springs += 1
        elif c == ".":
            if current_springs == 0:
                continue
            if len(res) == 0 or res.pop(0) != current_springs:
                return 0
            current_springs = 0
            split_point = i
        else:
            matches += test_line(line[split_point:].replace("?", "#", 1), res, stage+1)
            matches += test_line(line[split_point:].replace("?", ".", 1), res, stage+1)

    return matches

    if len(res) == 0:
        #print(1)
        #
        return 0 if "#" in line else 1
        return 1

    i = 0
    matches = 0
    while (m := res[0].search(line[i:])) and "#" not in line[:m.start()] :
        #print(m)
        #print (" - ", line[i + m.end():])
        matches += test_line(line[i + m.end():], res[1:], stage+1)

        #if "#" in m[0]:
            #break
        if m[0][0] == "#":
            break


        i += m.start() + 1

        #if "#" in m[0]:
        #    i += m.start() + m[0].index("#")
        #    print(i)
        #else:
        #    i += m.start() + 1
        #while line[i] == "#":

        #    i += 1

    #print(matches)
    return matches


total = 0


start = time.perf_counter()

for line, check in data:
    valids = test_line(line, check)
    print(valids)

    valid_old = 0
    for iter in line_iter(line):
        if is_valid(iter, check):
            valid_old += 1

    if valids != valid_old:
        print(line, check, valids, valid_old)
        break
    #    print()
    total += valids


print("Time: ", time.perf_counter() - start)

print(total)