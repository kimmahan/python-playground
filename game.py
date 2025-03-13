import random
import time

# ASCII art for the game
ROCK = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

PAPER = """
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
"""

SCISSORS = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

# Game logic
choices = {"rock": ROCK, "paper": PAPER, "scissors": SCISSORS}
score = {"player": 0, "computer": 0}

def play_game():
    print("\nWelcome to Rock, Paper, Scissors!")
    while True:
        print(f"\nScore - You: {score['player']} | Computer: {score['computer']}")
        player_choice = input("Enter your choice (rock/paper/scissors) or 'quit' to exit: ").lower()
        if player_choice == "quit":
            print(f"Final Score - You: {score['player']} | Computer: {score['computer']}")
            break
        if player_choice not in choices:
            print("Invalid choice! Try again.")
            continue

        computer_choice = random.choice(list(choices.keys()))
        print("\nYou chose:")
        print(choices[player_choice])
        print("Computer chose:")
        print(choices[computer_choice])
        time.sleep(1)

        if player_choice == computer_choice:
            print("It's a tie!")
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "scissors" and computer_choice == "paper") or \
             (player_choice == "paper" and computer_choice == "rock"):
            print("You win!")
            score["player"] += 1
        else:
            print("Computer wins!")
            score["computer"] += 1

if __name__ == "__main__":
    play_game()