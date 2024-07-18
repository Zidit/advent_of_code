
planets = {}

with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        parent, planet = line.strip().split(")")
        planets.update([(planet,(parent, None))])



def get_parent_count(planet, target= "COM"):
    if planet == target:
        return 0

    planet_info = planets[planet]
    if planet_info[1] is None:
        parents = get_parent_count(planet_info[0], target) + 1
        planets.update([(planet, (planet_info[0], parents))] )
        return parents
    else:
        return planet_info[1]

def get_parents(planet, target= "COM"):
    if planet == target:
        return [target]

    return [planets[planet][0]] + get_parents(planets[planet][0], target)   

direct_orbits = len(planets) 

orbits = 0
for planet in planets:
    orbits += get_parent_count(planet)

#print(planets)
#print(f"{direct_orbits=}")
print(f"Total = {orbits}")
parents_you = get_parents("YOU")
parents_san = get_parents("SAN")
parents_san.reverse()
parents_you.reverse()
#print(f"{parents_you}")
#print(f"{parents_san}")



short_you = []
[short_you.append(x) for x in parents_you if x not in parents_san]
short_san = []
[short_san.append(x) for x in parents_san if x not in parents_you]

print(short_san)
print(short_you)

print(len(short_you) + len(short_san))

