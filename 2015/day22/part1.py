
import dataclasses
import copy

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

boss_hp = int(data[0].split(":")[1].strip())
boss_dmg = int(data[1].split(":")[1].strip())

@dataclasses.dataclass
class Boss:
    hp:int
    dmg:int
    poison:int=0

@dataclasses.dataclass
class Player:
    hp:int
    armor:int
    mana:int
    armor_turns:int = 0
    recharge_turns:int = 0
    total_mana_usage:int = 0


def run_effects(player:Player, boss:Boss):


    def print(*varg, **kvarg):
        pass

    if boss.poison:
        boss.poison -= 1
        boss.hp -= 3
        print("Poison timer", boss.poison)
       

    if player.armor_turns:
        player.armor_turns -= 1
        print("Shield timer", player.armor_turns)
    if player.armor_turns == 0:
        player.armor = 0

    if player.recharge_turns:
        player.recharge_turns -= 1
        player.mana += 101
        print("Recharge timer", player.recharge_turns)

def turn(player_org:Player, boss_org:Boss, spell:int):

    def print(*varg, **kvarg):
        pass

    player = copy.copy(player_org)
    boss = copy.copy(boss_org)
    #Player turn
    print("-- Player turn --")
    print(player)
    print(boss)
    run_effects(player, boss)

    if spell == 0:
        player.mana -= 53
        if player.mana < 0: return player, boss, False
        boss.hp -= 4
        player.total_mana_usage += 53
        print("Cast Missile")

    elif spell == 1:
        player.mana -= 73
        if player.mana < 0: return player, boss, False 
        boss.hp -= 2
        player.hp += 2
        player.total_mana_usage += 73
        print("Cast Drain")

    elif spell == 2:
        player.mana -= 113
        if player.mana < 0: return player, boss, False
        if player.armor_turns: return player, boss, False
        player.armor += 7
        player.armor_turns = 6
        player.total_mana_usage += 113
        print("Cast Armor")

    elif spell == 3:
        player.mana -= 173
        if player.mana < 0: return player, boss, False 
        if boss.poison: return player, boss, False
        boss.poison = 6
        player.total_mana_usage += 173
        print("Cast Poison")

    elif spell == 4:
        player.mana -= 229
        if player.mana < 0: return player, boss, False 
        if player.recharge_turns: return player, boss, False
        player.recharge_turns = 5
        player.total_mana_usage += 229
        print("Cast Recharge")

    #Boss turn
    print()
    print("-- Boss turn --")
    print(player)
    print(boss)
    run_effects(player, boss)

    if boss.hp <= 0:
        return player, boss, True

    player.hp -= max(1, boss.dmg - player.armor)

    if player.hp <= 0:
        return player, boss, False
    
    return player, boss, None



def check_state(player:Player, boss:Boss):
    if player.mana < 0:
        return False

    if boss.hp <= 0:
        return True

    if player.hp <= 0:
        return False


min_usage = 1000000000
def simulate(player:Player, boss:Boss, turn_num:int=0):
    global min_usage

    if player.total_mana_usage > min_usage:
        return

    for spell in range(5):
        #print("Turn:" , turn_num, "Spell:", spell)
        player_next, boss_next, status = turn(player, boss, spell)
        if status == True:
            if player_next.total_mana_usage < min_usage:
                print("Turn:", turn_num)
                print(player_next)
                print(boss_next)
                print()

            min_usage = min(player_next.total_mana_usage, min_usage)
        elif status == False:
            pass
        else:
            simulate(player_next, boss_next, turn_num+1)

    return min_usage


player = Player(50, 0, 500)
boss = Boss(boss_hp, boss_dmg)

#player = Player(10, 0, 250)
#boss = Boss(14, 8)


#print(player)
#print(boss)
print()

if False:
    test_spels = [4, 2, 1, 3, 0]
    for i, spell in enumerate(test_spels):
        print("Turn:" , i)

        player, boss, status = turn(player, boss, spell)

        print(status)
        print()


ret = simulate(player, boss)

print("End")
print(player)
print(boss)


print(min_usage)
