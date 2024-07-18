import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

for i, line in enumerate(data):
    if "S" in line:
        y = i
        x = line.index("S")
        cur = (x,y)

def get_pipe(pos):
    if pos[0] < 0 or pos[1] < 0:
        return "x"
    return data[pos[1]][pos[0]]

def move_pos(pos, x, y):
    return (pos[0] + x, pos[1] + y)

prev = cur
print(cur, get_pipe(cur))

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

cur, dir = find_pipe_connected_to_start(cur)


pipe_cfg = {
    "-": {"east": "east", "west": "west"},
    "|": {"north": "north", "south": "south"},
    "L": {"south": "east", "west": "north"},
    "J": {"south": "west", "east": "north"},
    "7": {"north": "west", "east": "south"},
    "F": {"north": "east", "west": "south"},
}

pipe_len = 0
while True:
    pipe_len += 1
    pipe = get_pipe(cur)
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
    
print(pipe_len/2)
