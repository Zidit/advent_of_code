
input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

seeds = data.pop(0).split(":")[1].strip().split()
seeds = [int(v) for v in seeds]

data.pop(0)
#print(data)

maps = []
while data:
    try:
        end = data.index("\n")
        map_data = data[:end]
        data = data[end + 1:]
    except ValueError:
        map_data = data
        data = None
    
    map_lines = [[int(v) for v in l.split()] for l in map_data[1:]]
    maps.append(map_lines)

#print(maps)
maps_comb = []

for m in maps:
    map_comb_line = {0:0}
    #print(m)
    for line in m:  
        src_start = line[1]
        src_end = line[1] + line[2]
        offset = line[0] - line[1]
        #print(src_start, src_end, offset)

        map_comb_line[src_start] = offset
        if src_end not in map_comb_line:
            map_comb_line[src_end] = 0

    map_comb_line = dict(sorted(map_comb_line.items()))
    #print(map_comb_line)

    maps_comb.append([(k,v) for k, v in map_comb_line.items()])

#print(maps_comb)

lowest_loc = None

for seed in seeds:
    number = seed
    for m in maps_comb:
        offset = 0
        for k, v in m:
            if k > number:
                break
            offset = v
        number += offset
            
    #print(number)

    try:
        lowest_loc = min(lowest_loc, number)
    except Exception:
        lowest_loc = number

print()
print(lowest_loc)
