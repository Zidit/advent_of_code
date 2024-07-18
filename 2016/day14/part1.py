
import re
import hashlib

def hash(salt:str, index:int):
    test = salt + str(index)
    result = hashlib.md5(test.encode()).digest()
    return result.hex()


def search_keys(salt:str):
    candidates = []
    keys_found = 0

    hex = "0123456789abcdef"
    exp3_hex = "{3}|".join([c for c in hex]) + "{3}"
    exp5_hex = "{5}|".join([c for c in hex]) + "{5}"
    dig3 = re.compile(exp3_hex)
    dig5 = re.compile(exp5_hex)

    for i in range(50000):

        key = hash(salt, i)

        if v := dig5.findall(key):
            c = v[:1][0][0]
            #print(c, i)
            for candidate in candidates:
                if candidate[0] == c and i - candidate[1] < 1000:
                    keys_found += 1
                    print("Key", keys_found, "found at:", candidate[1])
                    if keys_found == 64:
                        return candidate[1]

        if v := dig3.findall(key):
            candidates.append((v[:1][0][0], i))

#print(search_keys("abc"))
print(search_keys("ahsbgdzn"))