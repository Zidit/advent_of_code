import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

total = 0
for line in data:
    nums = [int(v) for v in line.split()]
    #last_num = [nums[-1]]
    pred = 0 
    while nums.count(0) != len(nums):
        pred += nums[-1]
        nums = [b - a for a, b in zip(nums[:-1], nums[1:])]
        
        #last_num.append(nums[-1])
    #print(pred)
    total += pred

print(total)
