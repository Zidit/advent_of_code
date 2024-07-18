
import re

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()


data = [v.strip() for v in data]
#print(data)

password = "abcde"
password = "abcdefgh"

def rot_right(s:str, pos:int):
    for _ in range(pos):
        c = s[-1]
        s = c + s[:-1]
    return s

def rot_left(s:str, pos:int):
    for _ in range(pos):
        c = s[0]
        s = s[1:] + c
    return s

for line in data:
    password_old = password
    #print(password, line)
    if m:= re.match(r"swap position (\d) with position (\d)", line):
        x, y = [int(x) for x in m.groups()]
        xc = password[x]
        yc = password[y]
        password = password[:x] + yc + password[x + 1:]
        password = password[:y] + xc + password[y + 1:]

    elif m:= re.match(r"swap letter (.) with letter (.)", line):
        x, y = m.groups()
        password = password.replace(x, ".")
        password = password.replace(y, x)
        password = password.replace(".", y)

    elif m:= re.match(r"rotate (left|right) (\d) step", line):
        d = m.groups()[0]
        c = int(m.groups()[1])
        if d == "right":
            password = rot_right(password, c)
        if d == "left":
            password = rot_left(password, c)

    elif m:= re.match(r"rotate based on position of letter (.)", line):
        pos = password.find(m.groups()[0])
        if pos >= 4:
            pos += 1
        pos += 1
        password = rot_right(password, pos)
        
    elif m:= re.match(r"reverse positions (\d) through (\d)", line):
        x, y = [int(x) for x in m.groups()]
        rev = password[x:y + 1][::-1]
        password = password[:x] + rev + password[y + 1:]

    elif m:= re.match(r"move position (\d) to position (\d)", line):
        x, y = [int(x) for x in m.groups()]
        c = password[x]
        password = password[:x] + password[x + 1:]
        password = password[:y] + c + password[y:]

    else:
        raise Exception(f"Unknown command {line}")

    print(password_old, "->", password, " ", line)

    
print(password)
