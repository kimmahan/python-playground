import tkinter as tk
import random

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]
COLORS = ['cyan', 'yellow', 'purple', 'orange', 'blue', 'green', 'red']

class Tetris:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Tetris')
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root, 
            width=BLOCK_SIZE * GRID_WIDTH,
            height=BLOCK_SIZE * GRID_HEIGHT,
            bg='black'
        )
        self.canvas.pack()

        # Initialize game state
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_shape = None
        self.current_color = None
        self.game_over = False
        self.score = 0
        
        # Score display
        self.score_var = tk.StringVar()
        self.score_var.set(f"Score: {self.score}")
        self.score_label = tk.Label(self.root, textvariable=self.score_var)
        self.score_label.pack()

        # Bind keys
        self.root.bind('<Left>', lambda e: self.move(-1, 0))
        self.root.bind('<Right>', lambda e: self.move(1, 0))
        self.root.bind('<Down>', lambda e: self.move(0, 1))
        self.root.bind('<Up>', lambda e: self.rotate())
        self.root.bind('<space>', lambda e: self.drop())

        # Start game
        self.spawn_piece()
        self.update()
        
    def spawn_piece(self):
        if self.game_over:
            return
            
        # Choose random shape and color
        shape_index = random.randint(0, len(SHAPES) - 1)
        self.current_shape = [row[:] for row in SHAPES[shape_index]]
        self.current_color = COLORS[shape_index]
        
        # Starting position
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        
        # Check if piece can be placed
        if not self.is_valid_move(self.current_x, self.current_y):
            self.game_over = True
            self.show_game_over()
            
    def show_game_over(self):
        game_over_text = "Game Over! Score: " + str(self.score)
        self.canvas.create_text(
            BLOCK_SIZE * GRID_WIDTH // 2,
            BLOCK_SIZE * GRID_HEIGHT // 2,
            text=game_over_text,
            fill="white",
            font=("Arial", 20)
        )
            
    def is_valid_move(self, new_x, new_y):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = new_y + y
                    grid_x = new_x + x
                    
                    if (grid_y >= GRID_HEIGHT or
                        grid_x < 0 or
                        grid_x >= GRID_WIDTH or
                        (grid_y >= 0 and self.grid[grid_y][grid_x])):
                        return False
        return True
        
    def move(self, dx, dy):
        if self.game_over:
            return
            
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        
        if self.is_valid_move(new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
        elif dy > 0:  # If moving down and blocked
            self.freeze_piece()
            self.clear_lines()
            self.spawn_piece()
            
    def rotate(self):
        if self.game_over:
            return
            
        # Create new rotated shape
        new_shape = list(zip(*self.current_shape[::-1]))
        new_shape = [list(row) for row in new_shape]
        
        # Store old shape
        old_shape = self.current_shape
        
        # Try rotation
        self.current_shape = new_shape
        if not self.is_valid_move(self.current_x, self.current_y):
            self.current_shape = old_shape
            
    def drop(self):
        if self.game_over:
            return
            
        while self.is_valid_move(self.current_x, self.current_y + 1):
            self.current_y += 1
        self.freeze_piece()
        self.clear_lines()
        self.spawn_piece()
        
    def freeze_piece(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_y + y
                    if grid_y >= 0:
                        self.grid[grid_y][self.current_x + x] = self.current_color
                        
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                lines_to_clear.append(y)
                
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
            
        # Update score
        cleared_lines = len(lines_to_clear)
        if cleared_lines > 0:
            self.score += [100, 300, 500, 800][cleared_lines - 1]
            self.score_var.set(f"Score: {self.score}")
        
    def draw(self):
        self.canvas.delete('all')
        
        # Draw fallen pieces
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color:
                    self.draw_block(x, y, color)
                    
        # Draw current piece
        if self.current_shape:
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell and self.current_y + y >= 0:
                        self.draw_block(
                            self.current_x + x,
                            self.current_y + y,
                            self.current_color
                        )
                        
    def draw_block(self, x, y, color):
        x1 = x * BLOCK_SIZE
        y1 = y * BLOCK_SIZE
        x2 = x1 + BLOCK_SIZE
        y2 = y1 + BLOCK_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
        
    def update(self):
        if not self.game_over:
            self.move(0, 1)  # Move down one step
            self.draw()
            self.root.after(1000, self.update)  # Update every second
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = Tetris()
    game.run()