import random

# Constants
NUM_DICE = 5
MAX_ROLLS = 3
CATEGORIES = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "Three of a Kind", "Four of a Kind", "Full House",
    "Small Straight", "Large Straight", "Yahtzee", "Chance"
]

def roll_dice(held):
    """Rolls dice that are not held."""
    return [random.randint(1, 6) if not held[i] else held[i] for i in range(NUM_DICE)]

def display_dice(dice):
    """Displays the dice values."""
    print("Dice:", " ".join(f"[{i+1}:{val}]" for i, val in enumerate(dice)))

def score_category(category, dice):
    """Calculates score for a given category."""
    counts = {i: dice.count(i) for i in range(1, 7)}
    sorted_dice = sorted(dice)

    if category == "Ones": return counts[1] * 1
    if category == "Twos": return counts[2] * 2
    if category == "Threes": return counts[3] * 3
    if category == "Fours": return counts[4] * 4
    if category == "Fives": return counts[5] * 5
    if category == "Sixes": return counts[6] * 6
    if category == "Three of a Kind" and max(counts.values()) >= 3: return sum(dice)
    if category == "Four of a Kind" and max(counts.values()) >= 4: return sum(dice)
    if category == "Full House" and sorted(counts.values())[-2:] == [2, 3]: return 25
    if category == "Small Straight" and any(set(seq).issubset(dice) for seq in ([1,2,3,4],[2,3,4,5],[3,4,5,6])): return 30
    if category == "Large Straight" and sorted_dice in ([1,2,3,4,5],[2,3,4,5,6]): return 40
    if category == "Yahtzee" and max(counts.values()) == 5: return 50
    if category == "Chance": return sum(dice)
    return 0

def choose_category(used_categories):
    """Prompts user to choose an unused category."""
    while True:
        print("\nAvailable categories:")
        for i, cat in enumerate(CATEGORIES):
            if cat not in used_categories:
                print(f"{i+1}. {cat}")
        try:
            choice = int(input("Choose category number: "))
            if 1 <= choice <= len(CATEGORIES) and CATEGORIES[choice-1] not in used_categories:
                return CATEGORIES[choice-1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def yahtzee_game():
    """Main game loop."""
    used_categories = set()
    total_score = 0

    for turn in range(len(CATEGORIES)):
        print(f"\n--- Turn {turn+1} ---")
        dice = [0] * NUM_DICE
        held = [0] * NUM_DICE

        for roll in range(MAX_ROLLS):
            dice = roll_dice(held)
            display_dice(dice)

            if roll < MAX_ROLLS - 1:
                hold_input = input("Enter dice numbers to hold (e.g., 1 3 5) or press Enter to roll all: ").strip()
                held = [dice[i] if str(i+1) in hold_input.split() else 0 for i in range(NUM_DICE)]

        category = choose_category(used_categories)
        used_categories.add(category)
        score = score_category(category, dice)
        total_score += score
        print(f"Scored {score} points in {category}. Total score: {total_score}")

    print(f"\nGame Over! Final Score: {total_score}")

if __name__ == "__main__":
    yahtzee_game()
