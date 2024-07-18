import math
import sys 

#sys.setrecursionlimit(1000000)

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [list(line.strip()) for line in data]

is_pipe = [[False for _ in range(len(data[0]))] for _ in range(len(data))]

for i, line in enumerate(data):
    if "S" in line:
        y = i
        x = line.index("S")
        start = (x,y)

def get_pipe(pos):
    if pos[0] < 0 or pos[1] < 0:
        return "x"
    return data[pos[1]][pos[0]]

def move_pos(pos, x, y):
    return (pos[0] + x, pos[1] + y)

print(start, get_pipe(start))

pipe_cfg = {
    "-": {"east": "east", "west": "west"},
    "|": {"north": "north", "south": "south"},
    "L": {"south": "east", "west": "north"},
    "J": {"south": "west", "east": "north"},
    "7": {"north": "west", "east": "south"},
    "F": {"north": "east", "west": "south"},
}

def find_pipe_connected_to_start(pos):
    temp = move_pos(pos, 1, 0)
    if get_pipe(temp) in "-J7":
        return temp, "east"

    temp = move_pos(pos, -1, 0)
    if get_pipe(temp) in "-FL":
        return temp, "west"

    temp = move_pos(pos, 0, 1)
    if get_pipe(temp) in "|JL":
        return temp, "north"

    temp = move_pos(pos, 0, -1)
    if get_pipe(temp) in "|F7":
        return temp, "south"

def get_start_pipe_shape(pos):
    outs = []

    temp = move_pos(pos, 1, 0)
    if get_pipe(temp) in "-J7":
        outs.append("east")

    temp = move_pos(pos, -1, 0)
    if get_pipe(temp) in "-FL":
        outs.append("west")

    temp = move_pos(pos, 0, 1)
    if get_pipe(temp) in "|JL":
        outs.append("north")

    temp = move_pos(pos, 0, -1)
    if get_pipe(temp) in "|F7":
        outs.append("south")

    #print(outs)
    for k, v in pipe_cfg.items():
        if v.get(outs[0], "") == outs[1]:
            return k
        elif v.get(outs[1], "") == outs[0]:
            return k


shape = get_start_pipe_shape(start)
cur, dir = find_pipe_connected_to_start(start)
print(shape)

while True:
    pipe = get_pipe(cur)
    #data[cur[1]][cur[0]] = "x"
    is_pipe[cur[1]][cur[0]] = True

    #print(cur, dir, pipe)

    if pipe == "S":
        break

    dir = pipe_cfg[pipe][dir]
    #print(dir)

    if dir == "east": cur = move_pos(cur, 1, 0)
    elif dir == "west": cur = move_pos(cur, -1, 0)
    elif dir == "north": cur = move_pos(cur, 0, -1)
    elif dir == "south": cur = move_pos(cur, 0, 1)
    else:
        raise Exception

data[start[1]][start[0]] = shape



#for y, line in enumerate(data):
#    for x, point in enumerate(line):
#        if is_pipe[y][x] == True:
#            data[y][x] = "x"


for y, line in enumerate(data):
    outside = True
    hori = None
    status = ""
    for x, point in enumerate(line):
        if is_pipe[y][x] == True:
            if point in "|":
                outside = not outside
            elif point in "FL":
                hori = point
            elif point in "7":
                if hori == "L":
                    outside = not outside
                elif hori != "F":
                    print("".join(line))
                    print(status)
                    print("".join(line[x-5: x+5]))
                    print(y, x, point, hori)
                    raise Exception()
                hori = None
            elif point in "J":
                if hori == "F":
                    outside = not outside
                elif hori != "L":
                    print(y, x, point, hori)
                    raise Exception()
                hori = None              
        elif outside:
            data[y][x] = " "
        else:
            data[y][x] = "x"

        status += "o" if outside else "i" 


print("done")
#print(len(data), len(data[0]))

with open("out.txt", "w") as file:
    data = ["".join(line) + "\n" for line in data]
    file.writelines(data)

total = 0
for line in data:
    total += line.count("x")

print(total)