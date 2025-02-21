from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Dictionary mapping game names to their PygBag-generated HTML files in dist/
games = {
    "bouncing_balls": "bouncing_balls/index.html",
    "hangman": "hangman/index.html",
    "pacman": "pacman/index.html",
    "rock_paper_scissors": "rock_paper_scissors/index.html",
    "tetris": "tetris/index.html",
    "chatgpt-celestial": "chatgpt-celestial/index.html",
    "claude-celestial": "claude-celestial/index.html",
    "gemini-celestial": "gemini-celestial/index.html",
    "particle": "particle/index.html"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<game_name>')
def play_game(game_name):
    if game_name in games:
        try:
            # Serve the PygBag-generated HTML file for the game
            return send_from_directory('dist', games[game_name])
        except Exception as e:
            return f"Error loading {game_name}: {str(e)}", 500
    return "Game not found!", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)