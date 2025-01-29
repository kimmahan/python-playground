import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra space for score/next piece
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 240, 240),  # Cyan
    (240, 240, 0),  # Yellow
    (160, 0, 240),  # Purple
    (240, 160, 0),  # Orange
    (0, 0, 240),    # Blue
    (0, 240, 0),    # Green
    (240, 0, 0)     # Red
]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        
        # Initialize game state
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500  # Time in milliseconds
        
    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': [row[:] for row in SHAPES[shape_idx]],
            'color': COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }

    def valid_move(self, piece, x, y):
        for row_idx, row in enumerate(piece['shape']):
            for col_idx, cell in enumerate(row):
                if cell:
                    new_x = x + col_idx
                    new_y = y + row_idx
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x] is not None)):
                        return False
        return True

    def rotate_piece(self, piece):
        new_shape = list(zip(*piece['shape'][::-1]))
        new_shape = [list(row) for row in new_shape]
        if self.valid_move({'shape': new_shape, 'color': piece['color']}, 
                          piece['x'], piece['y']):
            piece['shape'] = new_shape

    def drop_piece(self):
        if self.valid_move(self.current_piece, 
                          self.current_piece['x'], 
                          self.current_piece['y'] + 1):
            self.current_piece['y'] += 1
        else:
            self.freeze_piece()

    def freeze_piece(self):
        for row_idx, row in enumerate(self.current_piece['shape']):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece['y'] + row_idx
                    if grid_y >= 0:
                        grid_x = self.current_piece['x'] + col_idx
                        self.grid[grid_y][grid_x] = self.current_piece['color']
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if not self.valid_move(self.current_piece, 
                             self.current_piece['x'], 
                             self.current_piece['y']):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for row in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[row]):
                lines_cleared += 1
                del self.grid[row]
                self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        if lines_cleared:
            self.score += [100, 300, 500, 800][lines_cleared - 1]

    def draw_grid(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, color in enumerate(row):
                if color:
                    pygame.draw.rect(
                        self.screen, 
                        color,
                        (col_idx * BLOCK_SIZE, 
                         row_idx * BLOCK_SIZE, 
                         BLOCK_SIZE - 1, 
                         BLOCK_SIZE - 1)
                    )

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for row_idx, row in enumerate(piece['shape']):
            for col_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        piece['color'],
                        ((piece['x'] + col_idx) * BLOCK_SIZE + offset_x,
                         (piece['y'] + row_idx) * BLOCK_SIZE + offset_y,
                         BLOCK_SIZE - 1,
                         BLOCK_SIZE - 1)
                    )

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        self.draw_grid()
        
        # Draw current piece
        if not self.game_over:
            self.draw_piece(self.current_piece)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 20))
        
        # Draw "Next Piece" text and box
        next_text = self.font.render('Next:', True, WHITE)
        self.screen.blit(next_text, (GRID_WIDTH * BLOCK_SIZE + 10, 80))
        
        # Draw next piece
        next_piece_copy = self.next_piece.copy()
        next_piece_copy['x'] = GRID_WIDTH + 1
        next_piece_copy['y'] = 4
        self.draw_piece(next_piece_copy)
        
        # Draw game over
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, WHITE)
            self.screen.blit(
                game_over_text,
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2)
            )
        
        pygame.display.flip()

    def run(self):
        while True:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'] - 1,
                                         self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece,
                                         self.current_piece['x'] + 1,
                                         self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        self.drop_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece(self.current_piece)
                    elif event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece,
                                            self.current_piece['x'],
                                            self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                        self.freeze_piece()
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            # Handle piece falling
            if not self.game_over:
                if self.fall_time >= self.fall_speed:
                    self.drop_piece()
                    self.fall_time = 0

            self.draw()

if __name__ == '__main__':
    game = Tetris()
    game.run()