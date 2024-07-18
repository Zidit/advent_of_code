

def parse_line(line):
    tokens = line.split()
    return (tokens[0], int(tokens[3]), int(tokens[6]), int(tokens[13])) #name, speed, fly time, rest

def simulate_deer(deer):
    if deer[2] is False: # Deer mooving
        deer[1] += deer[0][1]
        deer[3] += 1
        if deer[3] >= deer[0][2]:
            deer[2] = True
            deer[3] = 0
    else:               # Deer resting
        deer[3] += 1
        if deer[3] >= deer[0][3]:
            deer[2] = False
            deer[3] = 0


input = open("input.txt")

longest_dist = 0
deers = []
for line in input:
    deers.append([parse_line(line), 0, False, 0, 0]) # deer, ditance, resring, time in current state, points

for time in range(2503):
    for deer in deers:
        simulate_deer(deer)
    for deer in deers:
        longest_dist = max(longest_dist, deer[1])

    for deer in deers:
        if deer[1] == longest_dist:
            deer[4] += 1


most_points = ("",0)

for deer in deers:
    if deer[4] >= most_points[1]:
        most_points = (deer[0][0], deer[4])

print(most_points)
