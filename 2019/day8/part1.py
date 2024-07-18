with open("input.txt", "r", encoding="utf-8") as f:
    d = f.readline()

colums = 25
rows = 6
pixels_in_layer = colums * rows


def split_array(array, size):
    ret = []

    for i in range(len(array) // size):
        ret.append(array[i * size: (i + 1) * size])

    return ret

def count_chars(array, char):
    count = 0
    for c in array:
        if c == char:
            count += 1

    return count


layers = split_array(d, pixels_in_layer)

fewest_zeros = 10000000
best_layer = 0

for i,l in enumerate(layers):
    count = count_chars(l, "0")
    if fewest_zeros > count:
        fewest_zeros = count
        best_layer = i

print(best_layer)
print(count_chars(layers[best_layer], "1") * count_chars(layers[best_layer], "2") )