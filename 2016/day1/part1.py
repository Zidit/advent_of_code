#!/usr/bin/python
import re

input = open("input.txt", "r")

direction = 0
dist_north = 0
dist_east = 0

tokens = input.read().split(", ")
for token in tokens:
    if token[0] == 'R':
        direction += 1
        if direction == 4:
            direction = 0

    if token[0] == 'L':
        direction -= 1
        if direction == -1:
            direction = 3

    walk = int(token[1:])

    if direction == 0:
        dist_north += walk
    if direction == 1:
        dist_east += walk
    if direction == 2:
        dist_north -= walk
    if direction == 3:
        dist_east -= walk

print ("N: " , dist_north, " E: ", dist_east)
print (abs(dist_east) + abs(dist_north))

# Result: 241
