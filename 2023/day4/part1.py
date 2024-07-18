import re

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

total = 0

for line in data:
    card, line = line.split(":")
    win_nums, nums = line.split("|")

    card = int(card.split()[1])
    win_nums = set([int(i) for i in win_nums.split()])
    nums = set([int(i) for i in nums.split()])

    common = win_nums.intersection(nums)
    #print(card, win_nums, nums, common)

    if len(common):
        #print(2**(len(common) - 1))
        total += 2**(len(common) - 1)

print(total)