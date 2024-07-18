

import hashlib

salt = "qtetzkpl"
salt = "hijkl"
salt = "ihgpwlah"

def hash_str(data:str):
    return hashlib.md5(data.encode()).digest().hex()


def get_open_doors(hash:str):
    valids = ""
    open_let = "bcdef"
    if hash[0] in open_let:
        valids += "U"
    if hash[1] in open_let:
        valids += "D"
    if hash[2] in open_let:
        valids += "L"
    if hash[3] in open_let:
        valids += "R"

    return valids

def get_valid_directions(pos:tuple[int, int]):
    valids = ""

    if pos[1] > 0:
        valids += "U"
    if pos[1] < 3:
        valids += "D"
    if pos[0] > 0:
        valids += "L"
    if pos[0] < 3:
        valids += "R"

    return valids

def move_pos(pos:tuple[int, int], dir:str):
    if dir == "U":
        return (pos[0], pos[1] - 1)
    if dir == "D":
        return (pos[0], pos[1] + 1)

    if dir == "L":
        return (pos[0] - 1, pos[1])
    if dir == "R":
        return (pos[0] + 1, pos[1])



def step(salt:str, path:str="", pos:tuple[int, int]=(0,0), best=100000):
    if pos == (3,3):
        print("Path:", path)
        return path

    if len(path) >= best:
        return

    hash = hash_str(salt+path)
    doors = get_open_doors(hash)
    valid_dir = get_valid_directions(pos)
    dirs = set(valid_dir) & set(doors)
    #print(hash, doors, valid_dir, dirs)

    best_str = None
    for d in dirs:
        ret = step(salt, path+d, move_pos(pos, d), best)
        if ret:
            best = min(best, len(ret))
            best_str = ret

    return best_str




#print(step("ihgpwlah"))
#print(step("kglvqrro"))
#print(step("ulqzkmiv"))

print(step("qtetzkpl"))

