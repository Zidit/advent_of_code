

presents_most = 0
presents = [0]*1000000000

i = 1

while True:

    k = i
    a = 0
    for a in range (1,51):
        presents[k * a] += 11 * i
        presents_most = max(presents_most, presents[k])
        if presents_most > 36000000:
            print(k*a,presents_most)
            exit()


    i += 1
    print(presents_most)
