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


# Function generates one random number from 1 to 6 to simulate a dice
def dice_roll():
    dice = random.randint(1, 6)
    return dice


# Function checks each position in the kept_dice list, to see if  value equal 0. If so, that means that number is a blank and needs to be rolled
def player_roll(kept_dice, current_dice):
    # Checks each position in kept_dice
    for x in range(5):
        # If position is equal to zero, then a dice roll needs to be proformed
        if kept_dice[x-1] == 0:
            # Dice roll is put into current dice so player can later chose what to keep
            current_dice[x-1] = dice_roll()
    print(current_dice)
    kept_dice = choose_keep(current_dice)
    return kept_dice


# Function asks user what rolls they want to keep
def choose_keep(current_dice):
    # User input of what they want
    keep = input("Keep:").strip()
    # Split the user input so we can read each choice
    final = keep.split()
    # Reset any dice rolls that aren't being kept back to zero, so they can be rolled on the next loop
    kept_dice = [0, 0, 0, 0, 0]
    # For loop to only last the length of the user's input
    for y in range(len(final)):
        # Position in the list starts at 0, not 1, so all positions need to be moved one less
        position = int(final[y]) - 1
        # kept_dice will be taken to next turn, whist current_dice just shows what was rolled this turn
        kept_dice[position] = current_dice[position]
    return kept_dice


# Main function where everything starts and ends
def main():
    # Starting list before any dice are rolled
    kept_dice = [0, 0, 0, 0, 0]
    current_dice = [0, 0, 0, 0, 0]
    print("--- Turn 1 ---")
    kept_dice = player_roll(kept_dice, current_dice)
    print("List currently shows ", kept_dice)
    print("--- Turn 2 ---")
    kept_dice = player_roll(kept_dice, current_dice)
    print("List currently shows ", kept_dice)


main()

