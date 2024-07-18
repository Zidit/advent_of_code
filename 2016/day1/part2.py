#!/usr/bin/python
import re

def prosess(input):
    direction = 0
    positions = [(0, 0)]
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

        step = ()

        if direction == 0:
            step = (1, 0)
        #    positions.append((last_pos[0] + walk, last_pos[1]))

        if direction == 1:
            step = (0, 1)
        #    positions.append((last_pos[0], last_pos[1] + walk))

        if direction == 2:
            step = (-1, 0)
        #    positions.append((last_pos[0] - walk, last_pos[1]))

        if direction == 3:
            step = (0, -1)
        #    positions.append((last_pos[0], last_pos[1] - walk))

        for i in range(0, walk):
            new_pos = (positions[-1][0] + step[0], positions[-1][1] + step[1])
            if new_pos in positions:
                return new_pos
            else:
                positions.append(new_pos)



input = open("input.txt", "r")
result = prosess(input)
print (result)

print (abs(result[0]) + abs(result[1]))

# 246 too high
