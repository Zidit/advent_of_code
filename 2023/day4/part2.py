import re

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

total = 0
cards = {1:1}

for line in data:
    card, line = line.split(":")
    win_nums, nums = line.split("|")

    card = int(card.split()[1])
    win_nums = set([int(i) for i in win_nums.split()])
    nums = set([int(i) for i in nums.split()])

    common = win_nums.intersection(nums)
    #print(card, win_nums, nums, common)
    if card not in cards:
        cards[card] = 1

    for i in range(card + 1, card + 1 + len(common)):
        if i not in cards:
            cards[i] = 1
        cards[i] += cards[card]

    #print(cards)

#print(cards)
total = sum(cards.values())
print(total)