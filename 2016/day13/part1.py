#!/usr/bin/python

import sys
import math

room = [["" for x in range(80)] for y in range(80)]

def print_room():
    for x in room:
        for y in x:
            sys.stdout.write(y)
        sys.stdout.write('\n\r')
    print ("")

def is_wall(x,y):
    if x < 0 or y < 0:
        return True

    if x > 80 or y > 80:
        return True

    number = (x + y)**2 + 3*x + y + 1350 #x*x + 3*x + 2*x*y + y + y*y + input
    bit_str = bin(number)
    bits = bit_str.count('1')
    if bits % 2 == 1:
        return True
    else:
        return False

def dist(start, stop):
    return math.sqrt((stop[0] - start[0])**2 + (stop[1] - start[1])**2)

def valid_node(x,y, open_list, closed_list):
    if is_wall(x,y):
        return False
    for l in open_list:
        if l[2] == (x,y):
            return False
    for l in closed_list:
        if l[2] == (x,y):
            return False

    return True

def new_node(pos, prev, dest):
    global room

    h = dist(prev, dest)
    g = prev[1] + 1
    f = g + h

    room[pos[0]][pos[1]] = "0"
    return [f, g, pos]

def shortes_path(start, stop):
    open_list = [[dist(start, stop), 0, start]]
    closed_list = []

    while len(open_list) != 0:
        open_list = sorted(open_list, key=lambda tup: tup[0])

        current = open_list[0]
        open_list = open_list[1:]
        closed_list.append(current)

        if valid_node(current[2][0] - 1, current[2][1], open_list, closed_list):
            open_list.append(new_node((current[2][0] - 1, current[2][1]), current, stop))
        if valid_node(current[2][0], current[2][1] - 1, open_list, closed_list):
            open_list.append(new_node((current[2][0], current[2][1] - 1), current, stop))
        if valid_node(current[2][0] + 1, current[2][1], open_list, closed_list):
            open_list.append(new_node((current[2][0] + 1, current[2][1]), current, stop))
        if valid_node(current[2][0], current[2][1] + 1, open_list, closed_list):
            open_list.append(new_node((current[2][0], current[2][1] + 1), current, stop))

    for l in closed_list:
        if l[2] == stop:
            return l[1]


def process(input):

    global room
    for i, x in enumerate(room):
        for j, y in enumerate(x):
            if is_wall(i,j):
                room[i][j] = "#"
            else:
                room[i][j] = "."


    ret = shortes_path((1,1),(31,39))
    room[31][39] = "x"
    print_room()
    return ret


ret = process(1)
print (ret)
