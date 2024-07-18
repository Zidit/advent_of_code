
data = []
with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        data.append(line)

def mod_fuel(mass):
    return max(mass // 3 - 2, 0)

total = 0
for line in data:
    module_fuel = 0

    fuel = mod_fuel(int(line))
    module_fuel += fuel
    while fuel:
        fuel = mod_fuel(fuel)
        module_fuel += fuel

    total += module_fuel
    
print(total)