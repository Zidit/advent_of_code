
input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

seeds = data.pop(0).split(":")[1].strip().split()
seeds = [int(v) for v in seeds]

data.pop(0)

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
        src_start = line[0]
        src_end = line[0] + line[2]
        offset = line[1] - line[0]
        #print(src_start, src_end, offset)

        map_comb_line[src_start] = offset
        if src_end not in map_comb_line:
            map_comb_line[src_end] = 0

    map_comb_line = dict(sorted(map_comb_line.items()))
    #print(map_comb_line)

    maps_comb.append([(k,v) for k, v in map_comb_line.items()])

for line in maps_comb:
    print(line)

def run():
    seed_ranges = [(s,s+e) for s,e in zip(seeds[::2], seeds[1::2])]
    for location in range(10_000_000):
        number = location
        for m in maps_comb[::-1]:
            offset = 0
            for k, v in m:
                if k > number:
                    break
                offset = v
            number += offset

        for seed in seed_ranges:
            if seed[0] <= number < seed[1]:
                print(number, location)      
                return

        if location % (10_000_000/100) == 0:
            print(".", end="", flush=True)

run()



