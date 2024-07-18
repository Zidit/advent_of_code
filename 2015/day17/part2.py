

containers = []
eggnot = 150

containers_neede = 100
combinations = 0

def test(containers, stored = 0, containers_used = 0):
    global combinations
    global containers_neede

    if stored == eggnot:
        if containers_used < containers_neede:
            combinations = 1
            containers_neede = containers_used
        elif containers_used == containers_neede:
            combinations += 1

    if stored > eggnot:
        return

    for i, container in enumerate(containers):
        test(containers[i + 1:], stored + container, containers_used + 1)

    return



with open("input.txt") as file:
    for line in file:
        containers.append(int(line))

test(containers)

print (combinations)
