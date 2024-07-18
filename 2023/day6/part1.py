import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

time = data.pop(0).split(":")[1].strip().split()
times = [int(v) for v in time]

distance = data.pop(0).split(":")[1].strip().split()
distances = [float(v) + 0.0001 for v in distance]

print(times)
print(distances)

def calc_hold_time(time, dist):
    hold_time1 = (time - math.sqrt(time**2 - 4*dist))/ 2 
    hold_time2 = (time + math.sqrt(time**2 - 4*dist))/ 2 

    return hold_time1, hold_time2

total = 1

for t, d in zip(times, distances):
    a,b = calc_hold_time(t,d)
    print(a,b)
    a = math.ceil(a)
    b = math.floor(b)
    valid_times = b - a +1
    print(a, b, valid_times)
    print()
    total *= valid_times

print(total)