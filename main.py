from flask import Flask, render_template, request, jsonify
import importlib
import sys

app = Flask(__name__)

# Dictionary mapping game names to their Python modules
games = {
    "bouncing_balls": "bouncing_ball",
    "hangman": "hangman",
    "pacman": "pacman",
    "rock_paper_scissors": "rock_paper",
    "tetris": "tetris",
    "chatgpt-celestial": "chatgpt_celestial",
    "claude-celestial": "claude_celestial",
    "gemini-celestial": "gemini_celestial",
    "particle": "particle"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<game_name>')
def play_game(game_name):
    if game_name in games:
        try:
            # Dynamically import and run the game module
            module_name = games[game_name]
            module = importlib.import_module(f"{module_name}")
            # Here, you'd need to adapt the game to run in a web context
            # For simplicity, we'll return a message (you'll need to implement game logic)
            return f"Playing {game_name}! (Add your game logic here)"
        except Exception as e:
            return f"Error running {game_name}: {str(e)}", 500
    return "Game not found!", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)