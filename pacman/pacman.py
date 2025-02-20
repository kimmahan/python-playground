import pygame
import random
import os
import math
from collections import deque

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 40  # Size of each grid cell
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Game variables
PACMAN_SIZE = CELL_SIZE // 2
GHOST_SIZE = CELL_SIZE // 2
DOT_SIZE = 4
POWER_DOT_SIZE = 8
WALL_THICKNESS = CELL_SIZE // 4
PACMAN_SPEED = 4
GHOST_SPEED = PACMAN_SPEED - 1  # Slightly faster ghosts for challenge
MAX_GHOSTS = 4
GHOST_SPAWN_DELAY = 5000  # 5 seconds in milliseconds
POWER_DOT_DURATION = 15000  # 15 seconds in milliseconds

# High score handling
HIGH_SCORE_FILE = "high_scores.txt"

def load_high_scores():
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as f:
                scores = [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]
            # Ensure exactly 5 unique scores, sorted in descending order
            unique_scores = sorted(list(set(scores)), reverse=True)[:5]
            return unique_scores + [0] * (5 - len(unique_scores))  # Pad with zeros if needed
        return [0] * 5  # Default to 5 zeros if file doesn't exist
    except (ValueError, IOError):
        return [0] * 5  # Handle any file reading errors

def save_high_scores(scores):
    with open(HIGH_SCORE_FILE, "w") as f:
        for score in sorted(scores, reverse=True)[:5]:
            f.write(f"{score}\n")

# Wall class for maze
class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Game objects
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = PACMAN_SPEED
        self.direction = 0  # 0: right, 1: left, 2: up, 3: down

    def move(self, dx, dy, walls):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_rect = pygame.Rect(new_x, new_y, PACMAN_SIZE, PACMAN_SIZE)
        
        # Check for wall collisions
        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            if 0 <= new_x <= WIDTH - PACMAN_SIZE and 0 <= new_y <= HEIGHT - PACMAN_SIZE:
                self.x = new_x
                self.y = new_y
                if dx > 0: self.direction = 0
                elif dx < 0: self.direction = 1
                elif dy < 0: self.direction = 2
                elif dy > 0: self.direction = 3
        # Wrap around horizontally (classic Pac-Man style)
        elif 0 > new_x or new_x > WIDTH - PACMAN_SIZE:
            self.x = WIDTH - PACMAN_SIZE if new_x < 0 else 0
            if dx > 0: self.direction = 0
            elif dx < 0: self.direction = 1

    def draw(self):
        center = (int(self.x + PACMAN_SIZE/2), int(self.y + PACMAN_SIZE/2))
        start_angle = [0, math.pi, 3*math.pi/2, math.pi/2][self.direction]
        pygame.draw.arc(screen, YELLOW, 
                       (self.x, self.y, PACMAN_SIZE, PACMAN_SIZE),
                       start_angle + math.pi/6, start_angle + 11*math.pi/6, 
                       PACMAN_SIZE//2)

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = GHOST_SPEED
        self.color = RED
        self.path = deque()  # Queue for random pathfinding
        self.is_blue = False  # Track if ghost is vulnerable

    def move_random(self, walls, pacman_pos):
        if not self.path or random.random() < 0.1:  # 10% chance to regenerate path for variety
            # Generate a random path, occasionally biasing toward Pac-Man
            if random.random() < 0.3:  # 30% chance to move toward Pac-Man
                dx = 1 if pacman_pos[0] > self.x else -1 if pacman_pos[0] < self.x else 0
                dy = 1 if pacman_pos[1] > self.y else -1 if pacman_pos[1] < self.y else 0
            else:
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Random direction
            self.path = deque([(dx, dy) for _ in range(random.randint(3, 6))])
        
        dx, dy = self.path.popleft()
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if not self.check_collision(new_x, new_y, walls):
            self.x = new_x
            self.y = new_y
        else:
            # If collision, try the opposite direction or a random direction
            opposite_dx, opposite_dy = -dx, -dy
            new_x = self.x + opposite_dx * self.speed
            new_y = self.y + opposite_dy * self.speed
            if not self.check_collision(new_x, new_y, walls):
                self.x = new_x
                self.y = new_y
            else:
                # Try a completely random direction if still blocked
                new_dx, new_dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                new_x = self.x + new_dx * self.speed
                new_y = self.y + new_dy * self.speed
                if not self.check_collision(new_x, new_y, walls):
                    self.x = new_x
                    self.y = new_y
                else:
                    self.path.clear()  # Reset path if still stuck

    def check_collision(self, x, y, walls):
        ghost_rect = pygame.Rect(x, y, GHOST_SIZE, GHOST_SIZE)
        return any(ghost_rect.colliderect(wall.rect) for wall in walls)

    def draw(self):
        pygame.draw.rect(screen, BLUE if self.is_blue else self.color, 
                        (self.x, self.y, GHOST_SIZE, GHOST_SIZE))

class Dot:
    def __init__(self, x, y, is_power=False):
        self.x = x
        self.y = y
        self.is_power = is_power

    def draw(self):
        if self.is_power:
            pygame.draw.circle(screen, WHITE, (self.x + POWER_DOT_SIZE, self.y + POWER_DOT_SIZE), POWER_DOT_SIZE)
        else:
            pygame.draw.circle(screen, WHITE, (self.x + DOT_SIZE, self.y + DOT_SIZE), DOT_SIZE)

# Classic Pac-Man style maze layout
walls = [
    Wall(0, 0, WIDTH, WALL_THICKNESS),  # Top
    Wall(0, HEIGHT-WALL_THICKNESS, WIDTH, WALL_THICKNESS),  # Bottom
    Wall(0, 0, WALL_THICKNESS, HEIGHT),  # Left
    Wall(WIDTH-WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT),  # Right
    # Outer walls forming corridors
    Wall(CELL_SIZE*2, CELL_SIZE, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*6, CELL_SIZE, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*10, CELL_SIZE, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*14, CELL_SIZE, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*2, CELL_SIZE*4, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*6, CELL_SIZE*4, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*10, CELL_SIZE*4, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*14, CELL_SIZE*4, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*2, CELL_SIZE*8, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*6, CELL_SIZE*8, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*10, CELL_SIZE*8, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*14, CELL_SIZE*8, CELL_SIZE*2, WALL_THICKNESS),
    # Vertical walls
    Wall(CELL_SIZE, CELL_SIZE*2, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*4, CELL_SIZE*2, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*8, CELL_SIZE*2, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*12, CELL_SIZE*2, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*16, CELL_SIZE*2, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE, CELL_SIZE*6, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*4, CELL_SIZE*6, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*8, CELL_SIZE*6, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*12, CELL_SIZE*6, WALL_THICKNESS, CELL_SIZE*2),
    Wall(CELL_SIZE*16, CELL_SIZE*6, WALL_THICKNESS, CELL_SIZE*2),
    # Central box (ghost house)
    Wall(CELL_SIZE*7, CELL_SIZE*5, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*9, CELL_SIZE*5, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*7, CELL_SIZE*7, CELL_SIZE*2, WALL_THICKNESS),
    Wall(CELL_SIZE*9, CELL_SIZE*7, CELL_SIZE*2, WALL_THICKNESS),
]

# More dots and power dots (grid-based, excluding walls)
dots = []
power_dots = []
for y in range(CELL_SIZE, HEIGHT-CELL_SIZE, CELL_SIZE//2):
    for x in range(CELL_SIZE, WIDTH-CELL_SIZE, CELL_SIZE//2):
        if not any(pygame.Rect(x, y, DOT_SIZE*2, DOT_SIZE*2).colliderect(wall.rect) for wall in walls):
            if (x == CELL_SIZE and y == CELL_SIZE) or (x == WIDTH-CELL_SIZE and y == HEIGHT-CELL_SIZE):
                power_dots.append(Dot(x, y, is_power=True))
            else:
                dots.append(Dot(x, y))

current_dots = dots + power_dots

# Initialize game objects
def initialize_game():
    return Pacman(CELL_SIZE, CELL_SIZE), [], current_dots.copy(), 0, 0, None  # Reset last_spawn_time to 0

pacman, ghosts, current_dots, score, last_spawn_time, power_dot_timer = initialize_game()
high_scores = load_high_scores()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Main game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            pacman, ghosts, current_dots, score, last_spawn_time, power_dot_timer = initialize_game()
            game_over = False

    if not game_over:
        # Handle movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        pacman.move(dx, dy, walls)

        # Spawn ghosts one at a time
        current_time = pygame.time.get_ticks()
        if len(ghosts) < MAX_GHOSTS and (last_spawn_time == 0 or current_time - last_spawn_time > GHOST_SPAWN_DELAY):
            # Spawn ghost in the central ghost house
            spawn_positions = [
                (CELL_SIZE*8, CELL_SIZE*6),  # Center of ghost house
            ]
            if spawn_positions:
                x, y = spawn_positions[0]
                ghosts.append(Ghost(x, y))
                last_spawn_time = current_time

        # Update power dot timer
        if power_dot_timer is not None:
            if current_time - power_dot_timer > POWER_DOT_DURATION:
                power_dot_timer = None
                for ghost in ghosts:
                    ghost.is_blue = False

        # Move ghosts randomly with occasional bias toward Pac-Man
        for ghost in ghosts[:]:
            ghost.move_random(walls, (pacman.x, pacman.y))
            if ghost.is_blue and (abs(pacman.x - ghost.x) < PACMAN_SIZE and abs(pacman.y - ghost.y) < PACMAN_SIZE):
                ghosts.remove(ghost)
                score += 200  # Points for eating a ghost

        # Check collisions with dots
        for dot in current_dots[:]:
            if (abs(pacman.x - dot.x) < PACMAN_SIZE and abs(pacman.y - dot.y) < PACMAN_SIZE):
                current_dots.remove(dot)
                if dot.is_power:
                    power_dot_timer = current_time
                    for ghost in ghosts:
                        ghost.is_blue = True
                    score += 50  # Points for power dot
                else:
                    score += 10
                if not current_dots:
                    current_dots = dots.copy() + power_dots.copy()

        # Check collisions with ghosts
        for ghost in ghosts:
            if not ghost.is_blue and (abs(pacman.x - ghost.x) < PACMAN_SIZE and 
                                    abs(pacman.y - ghost.y) < PACMAN_SIZE):
                high_scores.append(score)
                high_scores = sorted(list(set(high_scores)), reverse=True)[:5]  # Remove duplicates, keep top 5
                save_high_scores(high_scores)
                game_over = True

    # Draw everything
    screen.fill(BLACK)
    for wall in walls:
        wall.draw()
    pacman.draw()
    for ghost in ghosts:
        ghost.draw()
    for dot in current_dots:
        dot.draw()

    # Draw score (ensure proper display)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_scores[0]}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    # Game over screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        game_over_text = font.render("Game Over!", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 70, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - 70, HEIGHT//2 - 20))
        screen.blit(restart_text, (WIDTH//2 - 90, HEIGHT//2 + 20))
        
        for i, hs in enumerate(high_scores[:5]):
            hs_text = font.render(f"{i+1}. {hs}", True, WHITE)
            screen.blit(hs_text, (WIDTH//2 - 50, HEIGHT//2 + 60 + i*30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()