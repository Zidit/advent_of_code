

def get_index(row, colum):
    x = row + colum - 1
    t = (x * (x - 1) / 2) + colum
    return t

def get_mod(i):
    #return (20151125 * (252533 ** (i - 1))) % 33554393
    return (20151125 * (252533 ** (i - 1))) % 33554393


for row in range(1,7):
    r = []
    for colum in range(1,7):
        r.append(get_mod(get_index(row, colum)))
    print(r)

print(get_mod(get_index(2978, 3083)))
