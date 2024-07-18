

def line_to_points(line):
    points = []
    x = 0
    y = 0
    points.append((x,y))

    for step in line.split(","):
        d = step[0]
        l = int(step[1:])
        if d == "U":
            y += l
        if d == "D":
            y -= l
        if d == "L":
            x -= l
        if d == "R":
            x += l

        points.append((x,y))

    return points

def is_between(a, b, p):
    if a < p and b > p:
        return True
    elif a > p and b < p:
        return True
    else:
        return False

def intersection(l0a, l0b, l1a, l1b):
    if is_between(l0a[0], l0b[0], l1a[0]) and is_between(l0a[0], l0b[0], l1b[0]):
        if is_between(l1a[1], l1b[1], l0a[1]) and is_between(l1a[1], l1b[1], l0b[1]):
            return (l1a[0], l0a[1])

    if is_between(l1a[0], l1b[0], l0a[0]) and is_between(l1a[0], l1b[0], l0b[0]):
        if is_between(l0a[1], l0b[1], l1a[1]) and is_between(l0a[1], l0b[1], l1b[1]):
            return (l0a[0], l1a[1])

    return None

with open("input.txt", "r", encoding="utf-8") as f:
    points1 = line_to_points(f.readline())
    points2 = line_to_points(f.readline())

#points1 = line_to_points("R75,D30,R83,U83,L12,D49,R71,U7,L72")
#points2 = line_to_points("U62,R66,U55,R34,D71,R55,D58,R83")
#points1 = line_to_points("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
#points2 = line_to_points("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")

print(points1)
print(points2)

shortest = 10000000000000000000

for l1 in range(len(points1) - 1):
    for l2 in range(len(points2) - 1):
        i = intersection(points1[l1], points1[l1+1], points2[l2], points2[l2+1])
        if i:
            print(points1[l1], points1[l1+1], points2[l2], points2[l2+1])
            l = abs(i[0]) + abs(i[1])
            if l > 0:
                shortest = min(shortest, l)
            print(l)

print()
print(shortest)
