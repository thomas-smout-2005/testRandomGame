import random


"""
list = []
list.append(3)
list.append(4)
list.append(4)
print(list)

how_many = list.count(3)
print(how_many)
"""

"""
throw = []

def dice_roll():
    dice = random.randint(1, 6)
    return dice

for _ in range(5):
    throw.append(dice_roll())

print(throw)
print(throw[0])

print(f"Dice : [a.{throw[0]}] [b.{throw[1]}] [c.{throw[2]}] [d.{throw[3]}] [e.{throw[4]}]")
user_input = input("Which dice would you like to keep? (e.g., 2 4 5) or press Enter to roll again: ")
"""


def dice_roll():
    dice = random.randint(1, 6)
    return dice

kept_dice = [0, 0, 0, 0, 0]
for x in range(5):
    if kept_dice[x-1] == 0:
        kept_dice[x-1] = dice_roll()

print(kept_dice)