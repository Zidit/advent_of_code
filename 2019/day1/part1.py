
data = []
with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        data.append(line)

total = 0
for line in data:
    fuel = int(line) // 3 - 2
    total += fuel
    
print(total)