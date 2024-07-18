

presents_most = 0
presents = [0]*1000000

i = 1

while True:

    k = i
    while (k < 1000000):
        presents[k] += 10 * i
        presents_most = max(presents_most, presents[k])
        if presents_most > 36000000:
            print(k,presents_most)
            exit()
        k += i

    i += 1
    print(presents_most)
