


def get_next_row(row:str):
    new_row = ""
    row = "." + row + "."

    for i in range(len(row) - 2):
        tmp = row[i:i+3]
        if tmp == "^^." or tmp == ".^^" or tmp == "^.." or tmp == "..^":
            new_row += "^"
        else:
            new_row += "."
    return new_row

def get_map(first:str, rows:int):
    out = [first]

    for _ in range(rows - 1):
        out.append(get_next_row(out[-1]))

    return out


def print_map(map:list[str]):
    for l in map:
        print(l)
    print()

#print_map(get_map("..^^.", 3))
#map = get_map(".^^.^.^^^^", 10)

map = get_map(".^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^.", 40)

safe = 0
for l in map:
    safe += l.count(".")
print(safe)

