import hashlib

input = "bgvyzdsv"

for x in range(100000000):
    hash = hashlib.md5(input.encode() + str(x).encode() ).hexdigest()
    if (int(hash[0:5], 16) == 0):
        print(hash)
        print(x)
        exit()
