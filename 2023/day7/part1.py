import math

input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()


hands = []

for line in data:
    hand, value = line.split()
    value = int(value)
    hand = [card for card in hand]

    hand_int = []
    for card in hand:
        if card == "T":
            card = 10
        elif card == "J":
            card = 11
        elif card == "Q":
            card = 12
        elif card == "K":
            card = 13
        elif card == "A":
            card = 14
        else:
            card = int(card)
        hand_int.append(card)

    hands.append((hand_int, value))

#print(hands)

def rank_hand(hand:list[int]) -> int:
    card_counts = {i:hand.count(i) for i in hand}
    card_counts = sorted(list(card_counts.values()), reverse=True)
    #print(hand, card_counts)

    hand_value = 0
    if card_counts[0] == 5:
        hand_value = 7
    elif card_counts[0] == 4:
        hand_value = 6
    elif card_counts[0] == 3 and card_counts[1] == 2:
        hand_value = 5
    elif card_counts[0] == 3:
        hand_value = 4
    elif card_counts[0] == 2 and card_counts[1] == 2:
        hand_value = 3
    elif card_counts[0] == 2:
        hand_value = 2
    else:
        hand_value = 1        

    total = hand_value
    for card in hand:
        total *= 100
        total += card
    
    return total

ranked_hands = [(rank_hand(hand[0]), hand[1]) for hand in hands]
ranked_hands.sort(key=lambda x: x[0])
print(ranked_hands)

total = 0
for i, hand in enumerate(ranked_hands):
    total += (i + 1) * hand[1]

print(total)

