import math

# Ore == 31
test_reactions0 = """
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

# Ore == 165
test_reactions1 = """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

# Ore == 13312
test_reactions2 = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

# Ore == 180697
test_reactions3 = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""

# Ore == 2210736
test_reactions4 = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""

def parse_reaction_list(reactions_list):
    reactions = {}
    for line in reactions_list:
        if len(line) == 0:
            continue
        parts = line.split("=>")
        r_in = [p.strip().split(" ") for p in parts[0].split(",")]
        r_in = [(int(i[0]), i[1]) for i in r_in]
        r_out = parts[1].strip().split(" ")

        r_line = {r_out[1]: (int(r_out[0]), r_in)}
        reactions.update(r_line)
        #print(r_in, r_out)

    return reactions

def count_ore_requirment(reactions, required):

    stock = {}     
    ore = 0

    while len(required):
        next_item, count = list(required.items())[0]
        del required[next_item]

        stocked = stock.setdefault(next_item, 0)
        
        if count <= stocked:
            stock[next_item] = stocked - count
            continue
        else:
            count -= stocked

        reaction = reactions[next_item]
        reactions_count = math.ceil(count / reaction[0])
        stock[next_item] = reactions_count * reaction[0] - count

        for component in reaction[1]:
            ammount, name = component
            ammount *= reactions_count

            if name == "ORE":
                ore += ammount
            else:
                current = required.setdefault(name, 0)
                required.update({name: ammount + current})

        print(required)

    return ore


with open("input.txt", "r", encoding="utf-8") as f:
    input_reactions = f.read()

print(input_reactions)
reactions = parse_reaction_list(input_reactions.split("\n"))
#reactions = parse_reaction_list(test_reactions4.split("\n"))
print(reactions)

print(count_ore_requirment(reactions, {"FUEL": 1}))