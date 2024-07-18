
dists = {}
cities_all = []
shortest = 1000

input = open("input.txt", "r")

def get_sortest_dist(start, destinations, current_len):
    global shortest

    if(len(destinations) == 1):
        shortest = min(dists[(start, destinations[0])] + current_len, shortest)

    else:
        for i,k in enumerate(destinations):
            if (start == None):
                get_sortest_dist(destinations[i], destinations[:i] + destinations[i + 1:], 0)
            else:
                get_sortest_dist(destinations[i], destinations[:i] + destinations[i + 1:], dists[(start, destinations[i])] + current_len)



for line in input:
    route, dist = line.split(" = ")
    A, B = route.split(" to ")
    dists[(A,B)] = int(dist)
    dists[(B,A)] = int(dist)
    cities_all.append(A)
    cities_all.append(B)

cities = list(set(cities_all))

get_sortest_dist(None, cities, 0)
print(shortest)
