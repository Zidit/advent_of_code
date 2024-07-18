import math
import time

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()


data = [line.split(" ") for line in data]
data = [(line[0], [int(i) for i in line[1].strip().split(",")]) for line in data]


#print(data)

def line_iter(line:str):
    if "?" in line:
        yield from line_iter(line.replace("?", ".", 1))
        yield from line_iter(line.replace("?", "#", 1))
    else:
        yield line

def is_valid(line:str, check:list[int]):
    damaged = line.split(".")
    damaged = [len(v) for v in damaged if len(v)]
    return damaged == check

start = time.perf_counter()

total = 0
for line in data:
    #print(line, "  ", end="")
    valids = 0
    for iter in line_iter(line[0]):
        if is_valid(iter, line[1]):
            valids += 1
    #print(valids)
    total += valids

print("Time: ", time.perf_counter() - start)

print(total)