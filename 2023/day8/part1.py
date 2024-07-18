import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

turns = data.pop(0).strip()
data.pop(0)

paths = {}
for line in data:
    pos, opts = line.split("=")
    pos = pos.strip()
    
    opts = opts.strip().strip("()")
    opts = opts.split(",")
    opts = [o.strip() for o in opts]
    opts = tuple(opts)

    paths[pos] = opts

print(paths)
print(turns)

count = 0
pos = "AAA"

while True:
    for turn in turns:
        count += 1
        if turn == "L":
            pos = paths[pos][0]
        else:
            pos = paths[pos][1]

        #print(pos)

    #print("---")
    if pos == "ZZZ":
        break


print(count)
