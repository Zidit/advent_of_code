import re

grid = [[0 for x in range(1000)] for x in range(1000)]

def process_line(line):

    cords = [int(s) for s in re.findall('\\d+', line)]

    if line.find("turn on") != -1:
        for x in range(cords[0], cords[2] + 1):
            for y in range(cords[1], cords[3]+ 1):
                grid[x][y] += 1

    if line.find("turn off") != -1:
        for x in range(cords[0], cords[2] + 1):
            for y in range(cords[1], cords[3] + 1):
                if(grid[x][y] > 0): grid[x][y] -= 1

    if line.find("toggle") != -1:
        for x in range(cords[0], cords[2] + 1):
            for y in range(cords[1], cords[3] + 1):
                grid[x][y] += 2





input = open("input.txt", "r")
#input = ["turn on 0,0 through 2,2", "toggle 0,0 through 999,0"]#, "turn on 0,0 through 999,999", ]

for line in input:
    process_line(line)

output = 0
for row in grid:
    for cell in row:
        output += cell

print(output)
