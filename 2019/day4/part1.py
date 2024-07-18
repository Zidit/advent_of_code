
import time

def comp_array(a, b):
    if len(a) != len(b):
        raise Exception

    for c, d in zip(a,b):
        if c < d:
            return True

    return False

def inc_array(a, val = 1):
    a[-1] += val
    
    if a[-1] == 10:
        n = inc_array(a[0:-1])
        a = n + [n[-1]]

    return a

def pass_gen(start = 0, end = 0):
    n = [int(i) for i in str(start)]
    e = [int(i) for i in str(end)]

    j = 0
    for i,k in enumerate(n):
        j = max(k,j)
        n[i] = j

    while comp_array(n, e):
        yield n
        n = inc_array(n)

def test_pass(pwd):
    for p1, p2 in zip(pwd[:-1], pwd[1:]):
        if p1 == p2:
            return True
    return False

match = 0
for i in pass_gen(147981,691423):
    if test_pass(i):
        match += 1

print(match)
