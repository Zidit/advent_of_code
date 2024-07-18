

containers = []
eggnot = 150


def test(containers, stored = 0):

    if stored == eggnot:
        return 1
    if stored > eggnot:
        return 0

    comb = 0
    for i, container in enumerate(containers):
        comb += test(containers[i + 1:], stored + container)

    return comb

with open("input.txt") as file:
    for line in file:
        containers.append(int(line))

print(test(containers))
