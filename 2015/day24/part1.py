
packages = []


def valid_answer(containers):

    #print (sum(containers[0]),sum(containers[1]),sum(containers[2]))
    if sum(containers[0]) == sum(containers[1]):
        if sum(containers[1]) == sum(containers[2]):
            return True

    return False

def get_QE(container):
    product = 1
    for cont in container:
        product *= cont

    return product

def split(list):
    for position in range(len(list) - 1):
        yield list[:position + 1], list[position + 1:]

def dual_perm(list_org, list1 = [], list2 = []):
    if len(list_org) == 0:
        yield list1, list2

    for i, list in enumerate(list_org):
        yield from dual_perm (list_org[:i] + list_org[i + 1:], list1 + [list], list2)
        yield from dual_perm (list_org[:i] + list_org[i + 1:], list1, list2 + [list])

def perm(list_org, list1 = [], list2 = []):
    if len(list_org) == 0:
        yield list1, list2
    else:
        yield from perm (list_org[1:], list1, list2 + [list_org[0]])
        yield from perm (list_org[1:], list1 + [list_org[0]], list2)



def test(packages):

    min_QE = 100000
    min_back = 10000

    for a, b in perm(packages):
        if sum(a) * 2 == sum (b) and len(a) <= min_back:
            for c,d in perm(b):
                if sum(c) == sum(d):
                    print (a, c, d)
                    if len(a) < min_back:
                        min_back = len(a)
                        min_QE = get_QE(a)
                    elif len(a) == min_back:
                        min_QE = min(min_QE, get_QE(a))
                    break

    return min_back, min_QE

def test2(packages):

    total = sum(packages)
    min_QE = 10000000000000
    min_back = 100

    for a, b in perm(packages):
        if len(a) <= min_back:
            if sum(a) * 3 == total:
                if len(a) < min_back:
                    for c,d in perm(b):
                        if sum(c) == sum(d):
                            min_back = len(a)
                            min_QE = get_QE(a)
                            break
                elif get_QE(a) < min_QE:
                    for c,d in perm(b):
                        if sum(c) == sum(d):
                            min_QE = get_QE(a)
                            break

    return min_back, min_QE



with open("input.txt") as file:
    for line in file:
        packages.append(int(line))

#for a,b in perm([1,2,3,4,5]):
    #print(a,b)

print(test2(packages))
