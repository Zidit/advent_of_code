#!/usr/bin/python

import sys

lcd = [[0 for x in range(50)] for y in range(6)]

def print_lcd():
    for x in lcd:
        for y in x:
            if y == 1:
                sys.stdout.write('#')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n\r')
    print ("")

def draw_rect(x, y):
    for a in range(x):
        for b in range(y):
            lcd[b][a] = 1

def rotate_row(row, steps):
    new_row = lcd[row][-steps:]
    new_row +=  lcd[row][0:-steps]
    lcd[row] = new_row

def rotate_column(column, steps):
    for step in range(steps):
        last = lcd[-1][column]
        for i in range(len(lcd) - 2, -1, -1):
            lcd[i + 1][column] = lcd[i][column]
        lcd[0][column] = last

def run_line(line):
    tokens = line.split()

    if tokens[0] == "rect":
        cord = tokens[1].split("x")
        draw_rect(int(cord[0]), int(cord[1]))

    elif tokens[1] == "row":
        rotate_row(int(tokens[2].split("=")[1]), int(tokens[4]))

    elif tokens[1] == "column":
        rotate_column(int(tokens[2].split("=")[1]), int(tokens[4]))

    else:
        print ("unknown command")

def process(input):

    total_lines = 0
    for line in input:
        run_line(line)

    print_lcd()

    leds_on = 0
    for x in lcd:
        for y in x:
            if y == 1:
                leds_on += 1

    return leds_on


with open("input.txt") as input:
    ret = process(input)
    print (ret)
