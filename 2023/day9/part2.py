import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

total = 0
for line in data:
    nums = [int(v) for v in line.split()]
    first_num = [nums[0]]
    while nums.count(0) != len(nums):
        nums = [b - a for a, b in zip(nums[:-1], nums[1:])]
        first_num.append(nums[0])

    #print(first_num)
    pred = 0
    first_num = first_num[:-1]
    for num in first_num[::-1]:
        pred = num - pred

    #print(pred)
    total += pred

print(total)
