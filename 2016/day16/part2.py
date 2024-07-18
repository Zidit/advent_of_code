

def dragon_curve(a:str):
    b = a.replace("0", "2").replace("1", "0").replace("2", "1")
    return a + "0" + b[::-1]

def get_curve(data:str, length:int):
    while len(data) < length:
        data = dragon_curve(data)

    return data[:length]

def get_check_sum(data:str):
    while len(data) % 2 == 0:
        new_data = []
        for a,b in zip(data[:-1:2], data[1::2]):
            new_data.append("1" if a == b else "0")

        data = "".join(new_data)

    return data

curve = get_curve("01000100010010111", 35651584)
print("curve")
#print(curve)
check_sum = get_check_sum(curve)
print(check_sum)