import math
import time
import sys
sys.setrecursionlimit(10000)
#resource.setrlimit(10000)

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [l.strip() for l in data]
map_height = len(data)
map_width = len(data[0])

energized = [["" for c in row] for row in data]


def print_map(map:list[str]):
    for l in map:
        print("".join(l))
    print()


#print_map(data)
#print_map(energized)

beam = (0,0,"R")

def move_beam(x,y,d):
    if d == "R": return x + 1, y
    if d == "L": return x - 1, y
    if d == "U": return x, y - 1
    if d == "D": return x, y + 1

def run_beam(x:int, y:int, d:str):

    while True:
        if x < 0 or x >= map_width:
            return
        
        if y < 0 or y >= map_height:
            return
        
        if d in energized[y][x]:
            return
        
        energized[y][x] += d
        spot = data[y][x]

        if spot == ".":
            x,y = move_beam(x,y,d)
        
        elif spot == "/":
            if d == "R": d = "U"
            elif d == "L": d = "D"
            elif d == "U": d = "R"
            elif d == "D": d = "L"
            x,y = move_beam(x,y,d)
        
        elif spot == "\\":
            if d == "R": d = "D"
            elif d == "L": d = "U"
            elif d == "U": d = "L"
            elif d == "D": d = "R"
            x,y = move_beam(x,y,d)

        elif spot == "|":
            if d == "U" or d == "D":
                x,y = move_beam(x,y,d)
            else:
                run_beam(*move_beam(x,y,"U"),"U")
                run_beam(*move_beam(x,y,"D"),"D")

        elif spot == "-":
            if d == "L" or d == "R":
                x,y = move_beam(x,y,d)
            else:
                run_beam(*move_beam(x,y,"R"),"R")
                run_beam(*move_beam(x,y,"L"),"L")

        else:
            raise Exception(spot)


run_beam(0,0,"R")

#print_map(energized)
energized = [["#" if x else "." for x in y] for y in energized]
#print_map(energized)

energized_spots = 0
for line in energized:
    energized_spots += "".join(line).count("#")

print(energized_spots)