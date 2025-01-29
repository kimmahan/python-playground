import random

class Hangman:
    def __init__(self):
        self.words = ['python', 'programming', 'computer', 'algorithm', 'database', 'network', 'software']
        self.reset_game()
        self.total_score = 0
        self.games_played = 0
        self.games_won = 0

    def reset_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.max_tries = 6
        self.tries = 0
        self.current_word_score = 100  # Start with 100 points for each word

    def display_word(self):
        return ' '.join(letter if letter in self.guessed_letters else '_' for letter in self.word)

    def display_hangman(self):
        stages = [  # Final state: head, torso, both arms, and both legs
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -
            """,
            # Head, torso, both arms, and one leg
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     /
               -
            """,
            # Head, torso, and both arms
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |
               -
            """,
            # Head, torso, and one arm
            """
               --------
               |      |
               |      O
               |     \\|
               |      |
               |
               -
            """,
            # Head and torso
            """
               --------
               |      |
               |      O
               |      |
               |      |
               |
               -
            """,
            # Head
            """
               --------
               |      |
               |      O
               |
               |
               |
               -
            """,
            # Initial empty state
            """
               --------
               |      |
               |
               |
               |
               |
               -
            """
        ]
        return stages[self.max_tries - self.tries]

    def display_score(self):
        print("\n=== Score Board ===")
        print(f"Current Word Score: {self.current_word_score}")
        print(f"Total Score: {self.total_score}")
        print(f"Games Won: {self.games_won}")
        print(f"Games Played: {self.games_played}")
        if self.games_played > 0:
            win_rate = (self.games_won / self.games_played) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        print("================\n")

    def play_round(self):
        print("\nNew word started!")
        print(self.display_hangman())
        print(self.display_word())

        while True:
            self.display_score()
            guess = input("Guess a letter: ").lower()

            if not guess.isalpha() or len(guess) != 1:
                print("Please enter a single letter.")
                continue

            if guess in self.guessed_letters:
                print("You already guessed that letter.")
                continue

            self.guessed_letters.add(guess)

            if guess not in self.word:
                self.tries += 1
                self.current_word_score -= 10  # Deduct 10 points for wrong guess
                print(f"Wrong guess! You have {self.max_tries - self.tries} tries left.")
            else:
                # Award points based on letter frequency
                frequency = self.word.count(guess)
                points = 10 * frequency
                self.current_word_score += points
                print(f"Good guess! +{points} points!")

            print(self.display_hangman())
            current_state = self.display_word()
            print(current_state)

            if '_' not in current_state:
                print("Congratulations! You won!")
                self.total_score += self.current_word_score
                self.games_won += 1
                return True

            if self.tries >= self.max_tries:
                print(f"Game Over! The word was: {self.word}")
                return False

    def play(self):
        print("Welcome to Hangman!")
        
        while True:
            self.games_played += 1
            won = self.play_round()
            self.display_score()
            
            if not won:
                print("Don't worry! Keep practicing to improve your score!")
            
            play_again = input("Would you like to play again? (yes/no): ").lower()
            if play_again != 'yes':
                print("\nFinal Stats:")
                self.display_score()
                print("Thanks for playing!")
                break
                
            self.reset_game()

if __name__ == "__main__":
    game = Hangman()
    game.play()