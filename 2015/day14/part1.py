

def parse_line(line):
    tokens = line.split()
    return (tokens[0], int(tokens[3]), int(tokens[6]), int(tokens[13])) #name, speed, fly time, rest

def calc_dist(deer, travel_time):
    total_distance = 0
    cycle_time = (deer[2] + deer[3])
    full_cycles = travel_time // cycle_time
    reminder = travel_time - full_cycles * cycle_time

    if reminder >= deer[2]:
        total_distance = (full_cycles + 1) * deer[2] * deer[1]
    else:
        total_distance = (full_cycles * deer[2] + reminder) * deer[1]

    return (deer[0], total_distance)

input = open("input.txt")

deers = []
for line in input:
    deers.append(parse_line(line))

distance_travelled = []
for deer in deers:
    distance_travelled.append(calc_dist(deer, 2503))

fastest = ("", 0)
for deer in distance_travelled:
    if deer[1] > fastest[1]:
        fastest = deer

for deer in distance_travelled:
    print(deer[0], deer[1])

print(fastest)
