import json

total = 0

def p_int(num):
    global total
    total += int(num)
    return int(num)

def p_float(num):
    global total
    total += float(num)
    return float(num)


data = json.load(open("input.txt"), parse_float = p_float, parse_int = p_int)


print(data)
print(total)
