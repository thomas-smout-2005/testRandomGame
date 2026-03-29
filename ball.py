catagories = ["Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", "Three of a Kind", "Four of a Kind", "Full House", "Small Straight", "Long Straight", "YAHTEE", "Chance"]

def chose_catagory():
    # While catagories has anything in it, game/loop continues
    while catagories:
        # For loop, loops through all items in list catagories and outputs them
        for i in range(len(catagories)):
            # Printing formatting
            print(f"{i+1}. {catagories[i]}")
        # Asking user what they want to choose
        choice = int(input("What catagory do you want to put this in? (e.g., 4) : "))
        # Remove catagory from list
        catagories.pop(choice - 1)
    print("Game Over")



chose_catagory()