#!/usr/bin/python

key_pad = ((0,0,5,0,0), (0,10,6,2,0), (13,11,7,3,1), (0,12,8,4,0), (0,0,9,0,0))
pad_pos = (0,2)

def valid_pos(pos):
    global key_pos
    print (pos)

    if pos[0] < 0 or pos[0] > 4:
        return False
    if pos[1] < 0 or pos[1] > 4:
        return False

    if key_pad[pos[0]][pos[1]] != 0:
        return True
    else:
        return False

def get_number(line):
    global pad_pos
    global pad_pos

    for char in line:
        new_pos = ()
        if char == "U":
            new_pos = (pad_pos[0], pad_pos[1] + 1)
        elif char == "D":
            new_pos = (pad_pos[0], pad_pos[1] - 1)
        elif char == "L":
            new_pos = (pad_pos[0] - 1, pad_pos[1])
        elif char == "R":
            new_pos = (pad_pos[0] + 1, pad_pos[1])

        if new_pos != ():
            if valid_pos(new_pos):
                pad_pos = new_pos

    print (key_pad[pad_pos[0]][pad_pos[1]])
    return key_pad[pad_pos[0]][pad_pos[1]]

def process(input):

    ret = ""

    for line in input:
        ret += format(get_number(line), 'x')

    return ret

with open("input.txt") as input:
    ret = process(input)
    print (ret)
