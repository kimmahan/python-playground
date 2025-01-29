import random

class Hangman:
    def __init__(self):
        self.words = ['python', 'programming', 'computer', 'algorithm', 'database', 'network', 'software']
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.max_tries = 6
        self.tries = 0

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

    def play(self):
        print("Welcome to Hangman!")
        print(self.display_hangman())
        print(self.display_word())

        while True:
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
                print(f"Wrong guess! You have {self.max_tries - self.tries} tries left.")
            else:
                print("Good guess!")

            print(self.display_hangman())
            current_state = self.display_word()
            print(current_state)

            if '_' not in current_state:
                print("Congratulations! You won!")
                break

            if self.tries >= self.max_tries:
                print(f"Game Over! The word was: {self.word}")
                break

if __name__ == "__main__":
    game = Hangman()
    game.play()