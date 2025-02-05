import random
import time

def display_welcome():
    print("""
    ====================================
    🎮 ROCK, PAPER, SCISSORS, LIGHTNING! 
    ====================================
    Rules:
    - Rock crushes Scissors
    - Paper covers Rock
    - Scissors cuts Paper
    - Lightning beats Rock and Scissors
    - Paper insulates against Lightning Rods
    """)

def get_player_choice():
    while True:
        choice = input("\nChoose your weapon (rock/paper/scissors/lightning) or 'quit' to end: ").lower().strip()
        if choice in ['rock', 'paper', 'scissors', 'lightning', 'quit']:
            return choice
        print("Invalid choice! Please try again.")

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors', 'lightning'])

def determine_winner(player_choice, computer_choice):
    rules = {
        'rock': {'scissors': 'crushes', 'lightning': 'conducts'},
        'paper': {'rock': 'covers', 'lightning': 'insulates against'},
        'scissors': {'paper': 'cuts', 'lightning': 'conducts'},
        'lightning': {'rock': 'strikes', 'scissors': 'melts'}
    }
    
    if player_choice == computer_choice:
        return 'tie', None
    elif computer_choice in rules[player_choice]:
        return 'player', rules[player_choice][computer_choice]
    else:
        return 'computer', rules[computer_choice][player_choice]

def display_battle(player_choice, computer_choice, verb):
    print("\n🎲 Battle Results:")
    print(f"You chose: {player_choice.upper()}")
    time.sleep(0.5)
    print(f"Computer chose: {computer_choice.upper()}")
    time.sleep(0.5)

def play_game():
    scores = {'player': 0, 'computer': 0, 'ties': 0}
    display_welcome()
    
    while True:
        player_choice = get_player_choice()
        if player_choice == 'quit':
            break
            
        computer_choice = get_computer_choice()
        winner, verb = determine_winner(player_choice, computer_choice)
        
        display_battle(player_choice, computer_choice, verb)
        
        if winner == 'tie':
            print("\n🤝 It's a tie!")
            scores['ties'] += 1
        elif winner == 'player':
            print(f"\n🎉 You win! Your {player_choice} {verb} their {computer_choice}!")
            scores['player'] += 1
        else:
            print(f"\n💔 Computer wins! Their {computer_choice} {verb} your {player_choice}!")
            scores['computer'] += 1
            
        print("\n📊 Current Scores:")
        print(f"You: {scores['player']} | Computer: {scores['computer']} | Ties: {scores['ties']}")

    print("\n🎮 Final Scores:")
    print(f"You: {scores['player']} | Computer: {scores['computer']} | Ties: {scores['ties']}")
    print("\nThanks for playing! 👋")

if __name__ == "__main__":
    play_game()