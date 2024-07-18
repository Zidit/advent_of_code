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

def p_object(obj):
    if "red" in obj.values():
        #print("red")
        return 0
    return obj

data = json.load(open("input.txt"), object_hook = p_object)

data2 = json.loads(json.dumps(data), parse_float = p_float, parse_int = p_int)

print(data)
print(total)
