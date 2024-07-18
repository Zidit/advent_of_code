
import math

weapons = ((8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0))
armors  = ((0,0,0),(13,0,1),(31,0,2),(53,0,3),(75,0,4),(102,0,5))
rings   = ((0,0,0),(0,0,0),(25,1,0),(50,2,0),(100,3,0),(20,0,1),(40,0,2),(80,0,3))

def get_winner(p_hp, p_dmg, p_armor, b_hp, b_dmg, b_armor):
    player_dies_turn = math.ceil(p_hp / max(b_dmg - p_armor, 1))
    boss_dies_turn = math.ceil(b_hp / max(p_dmg - b_armor, 1))

    #print (player_dies_turn, boss_dies_turn)

    if player_dies_turn >= boss_dies_turn:
        return "player"
    else:
        return "boss"


min_cost = 1000

for weapon in weapons:
    for armor in armors:
        for i,ring1 in enumerate(rings):
            for ring2 in rings[:i] + rings[i + 1:]:
                items = tuple(map(sum, zip(weapon, armor, ring1, ring2)))
                if get_winner(100,items[1], items[2], 109,8,2) == "player":
                    min_cost = min(min_cost, items[0])

print (min_cost)
