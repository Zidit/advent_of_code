
import re
import hashlib

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()


disks = []
for line in data:
    m = re.fullmatch("Disc #(\d*) has (\d*) positions; at time=(\d*), it is at position (\d*).", line.strip())
    disks.append([int(m.groups()[1]), int(m.groups()[3])])

disks.append([11,0])
print(disks)

for i, disk in enumerate(disks):
    disk[1] = (disk[1] + i) % disk[0]

print(disks)

for i in range(200000000):
    for disk in disks:
        state = (disk[1] + i) % disk[0]
        if state != 0:
            break
    else:
        print(i - 1)
        break