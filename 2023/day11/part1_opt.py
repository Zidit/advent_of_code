import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

data = [list(line.strip()) for line in data]



extra_col = []
for c in range(len(data[0])):
    col = [data[r][c] for r in range(len(data))]
    #print(col)
    if len(set(col)) == 1:
        extra_col.append(c)
print("col", extra_col)

""" for c in extra_col[::-1]:
    for r in range(len(data)):
        data[r].insert(c, ".")

extra_col = []
for c in range(len(data[0])):
    col = [data[r][c] for r in range(len(data))]
    if len(set(col)) == 1:
        extra_col.append(c)
print(extra_col) """


extra_rows = []
for i, row in enumerate(data):
    if len(set(row)) == 1:
        extra_rows.append(i)

print("row", extra_rows)        

""" for i in extra_rows[::-1]:
    data.insert(i, "." * len(row))

extra_rows = []
for i, row in enumerate(data):
    if len(set(row)) == 1:
        extra_rows.append(i)
print(extra_rows) """

for line in data:
    print("".join(line))

galaxies = []
for r, row in enumerate(data):
    for c, pos in enumerate(row):
        if pos == "#":
            galaxies.append((r,c))

#print(galaxies)

length = 0
for i, galaxy in enumerate(galaxies):
    for galaxy_sec in galaxies[i+1:]:
        a = galaxy[0]
        b = galaxy_sec[0]
        if a > b:
            a, b = (b, a)
        #print("r", a,b)
        exp_row = [x for x in extra_rows if a < x < b]

        a = galaxy[1]
        b = galaxy_sec[1]
        if a > b:
            a, b = (b, a)
        #print("c", a,b)
        exp_col = [x for x in extra_col if a < x < b]

        #print(galaxy, galaxy_sec, exp_row, exp_col)

        dist_hor = abs(galaxy[1] - galaxy_sec[1]) + len(exp_row)
        dist_col = abs(galaxy[0] - galaxy_sec[0]) + len(exp_col)

        dist = dist_hor + dist_col
        length += dist
        #print(galaxy, galaxy_sec, dist)

print(length)
    