
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

lowest_loc = None

for seed in seeds:
    number = seed
    for m in maps:
        print(number,  end="")
        for line in m:
            src_start = line[1]
            src_end = line[1] + line[2]
            if src_start <= number < src_end:
                #print("(", src_start + line[0], ")", end="")
                number = number - src_start + line[0]
                break

        print(" -> ", end="")

            
    print(number)

    if lowest_loc is None:
        lowest_loc = number
    else:
        lowest_loc = min(lowest_loc, number)

print()
print(lowest_loc)