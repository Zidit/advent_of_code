input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

ranges = [v.strip().split("-") for v in data]
ranges = [(int(a), int(b)) for a,b in ranges]
ranges.sort(key=lambda x: x[0])

print(len(ranges))

def combine_ranges(ranges):

    while True:
        for i in range(len(ranges) - 1):
            if ranges[i][1] + 1 >= ranges[i+1][0]:
                print(ranges[i], ranges[i+1])
                ranges[i] = (ranges[i][0], max(ranges[i+1][1], ranges[i][1]))
                del ranges[i+1]
                break
        else:
            break

    return ranges


ranges = combine_ranges(ranges)
print(len(ranges))

total = 0
for a,b in ranges:
    total += b - a +1

print(4294967295 + 1 - total)
