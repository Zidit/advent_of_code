
import dataclasses
import time
import math
from cProfile import Profile
from pstats import SortKey, Stats
import os
from operator import itemgetter

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip().split() for l in data]

def get_point(data) -> tuple[int,int]:
    pos = (0,0)
    for line in data:
        l = int(line[2][2:7], 16)
        d = int(line[2][-2])
        if d == 3: pos = (pos[0], pos[1] + l)
        elif d == 1: pos = (pos[0], pos[1] - l)
        elif d == 2: pos = (pos[0] - l, pos[1])
        elif d == 0: pos = (pos[0] + l, pos[1])
        else:
            raise Exception(line)

        yield pos


total_x = 0
total_y = 0
perimeter = 0

point = list(get_point(data[::-1]))
for a, b in zip(point, point[1:] + point[:1]):
    total_x += a[0]*b[1]
    total_y += a[1]*b[0]
    perimeter += abs(a[0] - b[0]) + abs(a[1] - b[1])

print(total_x, total_y, perimeter)
print((total_x - total_y) // 2 + perimeter // 2 + 1)
