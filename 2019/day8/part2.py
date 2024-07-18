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

def print_image(data, rows, colums):
    for r in range(rows):
        for c in range(colums):
            print(data[r * colums + c], end='')

        print("")


layers = split_array(d, pixels_in_layer)

image = []

for pixel in range(pixels_in_layer):
    for l in layers:
        if l[pixel] == "0":
            image.append(" ")
            break
        if l[pixel] == "1":
            image.append("#")
            break

print_image(image, rows, colums)