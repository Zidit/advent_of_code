
planets = {}

with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        parent, planet = line.strip().split(")")
        planets.update([(planet,(parent, None))])



def get_parent_count(planet):
    if planet == "COM":
        return 0

    planet_info = planets[planet]
    if planet_info[1] is None:
        parents = get_parent_count(planet_info[0]) + 1
        planets.update([(planet, (planet_info[0], parents))] )
        return parents
    else:
        return planet_info[1]

direct_orbits = len(planets) 

orbits = 0
for planet in planets:
    orbits += get_parent_count(planet)

#print(planets)
#print(f"{direct_orbits=}")
print(f"Total = {orbits}")