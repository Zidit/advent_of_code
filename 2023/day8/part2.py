import math

input_file = "example2.txt"
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

positions = [x for x in paths.keys() if x[2] == "A"]
print(positions)

counts = []



for route in positions:
    count = 0
    pos = route
    #print(route)
    while True:
        for turn in turns:
            count += 1
            if turn == "L":
                pos = paths[pos][0]
            else:
                pos = paths[pos][1]
            #print(pos)

        #print("---")
        if pos[2] == "Z":
            counts.append(count)
            break

print(counts)

def factors(n):    # (cf. https://stackoverflow.com/a/15703327/849891)
    j = 2
    while n > 1:
        for i in range(j, int(math.sqrt(n+0.05)) + 1):
            if n % i == 0:
                n //= i ; j = i
                yield i
                break
        else:
            if n > 1:
                yield n; break
            
facs = set()
for i in counts:
    fac = list(factors(i))
    print(fac)
    for f in fac:
        facs.add(f)

print(facs)
total = 1
for f in facs:
    total *= f

print(total)


