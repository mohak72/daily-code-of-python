"""
Rock Paper Scissors Game
Classic game against the computer
"""

import random


CHOICES = {
    '1': 'Rock',
    '2': 'Paper',
    '3': 'Scissors'
}

EMOJIS = {
    '1': '\U0001F5FF',  # Rock
    '2': '\U0001F4C4',  # Paper
    '3': '\u2702\uFE0F'   # Scissors
}


def get_user_choice() -> str:
    """Get validated user choice"""
    print("\nChoose your weapon:")
    for key, value in CHOICES.items():
        emoji = EMOJIS.get(key, '')
        print(f"{key}. {emoji} {value}")

    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in CHOICES:
            return choice
        print("Invalid choice! Please enter 1, 2, or 3.")


def determine_winner(user: str, computer: str) -> str:
    """Determine the winner"""
    if user == computer:
        return "draw"

    win_conditions = {
        '1': '3',  # Rock beats Scissors
        '2': '1',  # Paper beats Rock
        '3': '2'   # Scissors beats Paper
    }

    if win_conditions[user] == computer:
        return "user"
    return "computer"


def play_round() -> dict:
    """Play one round"""
    user_choice = get_user_choice()
    computer_choice = random.choice(list(CHOICES.keys()))

    print(f"\nYou chose: {EMOJIS[user_choice]} {CHOICES[user_choice]}")
    print(f"Computer chose: {EMOJIS[computer_choice]} {CHOICES[computer_choice]}")

    result = determine_winner(user_choice, computer_choice)

    return {'result': result, 'user': user_choice, 'computer': computer_choice}


def main():
    """Main game loop"""
    print("\n" + "="*40)
    print("  ROCK PAPER SCISSORS")
    print("="*40)

    score = {'user': 0, 'computer': 0, 'draw': 0}

    while True:
        round_result = play_round()
        result = round_result['result']

        if result == "user":
            print("\nYou win this round!")
            score['user'] += 1
        elif result == "computer":
            print("\nComputer wins this round!")
            score['computer'] += 1
        else:
            print("\nIt's a draw!")
            score['draw'] += 1

        print(f"\nScore - You: {score['user']} | Computer: {score['computer']} | Draws: {score['draw']}")

        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again not in ['y', 'yes']:
            break

    print("\nFinal Score:")
    print(f"You: {score['user']} | Computer: {score['computer']} | Draws: {score['draw']}")

    if score['user'] > score['computer']:
        print("\nCongratulations! You won overall!")
    elif score['computer'] > score['user']:
        print("\nComputer won overall! Better luck next time!")
    else:
        print("\nIt's a tie overall!")

    print("\nThanks for playing!\n")


if __name__ == "__main__":
    main()
