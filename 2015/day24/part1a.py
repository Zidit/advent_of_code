
packages = []



def get_QE(container):
    product = 1
    for cont in container:
        product *= cont

    return product

def perm(list_org, list1 = [], list2 = []):
    if len(list_org) == 0:
        yield list1, list2
    else:
        yield from perm (list_org[1:], list1, list2 + [list_org[0]])
        yield from perm (list_org[1:], list1 + [list_org[0]], list2)


def test3(list, total):
    for a,b in perm(list):
        if sum(a) == sum(b):
            return True

    return False



def test2(packages):

    total = sum(packages) / 3
    min_QE = 10000000000000
    min_back = 100

    for a, b in perm(packages):
        if len(a) <= min_back and sum(a) == total:
            if len(a) < min_back:
                if test3(b, total):
                    min_back = len(a)
                    min_QE = get_QE(a)

            elif get_QE(a) < min_QE:
                if test3(b, total):
                    min_QE = get_QE(a)


    return min_back, min_QE



with open("input.txt") as file:
    for line in file:
        packages.append(int(line))

#for a,b in perm([1,2,3,4,5]):
    #print(a,b)

print(test2(packages))
