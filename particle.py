import pygame
import random
import math
import sys

# Initialize Pygame with debug info
print("Starting Particle Explosion Challenge...")
print(f"Python version: {sys.version}")
print(f"Pygame version: {pygame.version.ver}")

try:
    pygame.init()
    print("Pygame initialized successfully")
except Exception as e:
    print(f"Pygame initialization failed: {e}")
    sys.exit(1)

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set up display
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Explosion Challenge")
    clock = pygame.time.Clock()
    print("Display set up successfully")
except Exception as e:
    print(f"Display setup failed: {e}")
    sys.exit(1)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 8)
        self.life = random.randint(20, 60)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.life -= 1
        self.size = max(1, self.size * 0.98)

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Target:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = random.randint(50, HEIGHT-50)
        self.size = 30
        self.color = (255, 0, 0)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size-5)

# Game variables
particles = []
running = True
rainbow_mode = False
score = 0
target = Target()
target_timer = 180  # 3 seconds at 60 FPS

# Font setup with fallback
font = None
try:
    font = pygame.font.SysFont("arial", 36)
    print("Arial font loaded successfully")
except Exception as e:
    print(f"Failed to load Arial font: {e}")
    try:
        font = pygame.font.Font(None, 36)  # Default Pygame font
        print("Falling back to default Pygame font")
    except Exception as e:
        print(f"Failed to load default font: {e}")
        font = None

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Create particle explosion on every click
            for _ in range(100):  # Big, impressive explosion
                particles.append(Particle(mx, my))
            # Check if click hits target
            dist = math.sqrt((mx - target.x)**2 + (my - target.y)**2)
            if dist < target.size + 5:
                score += max(10, 100 - int(dist))  # More points for closer hits
                target = Target()  # New target
                target_timer = 180  # Reset timer
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rainbow_mode = not rainbow_mode

    # Clear screen
    screen.fill((20, 20, 40))  # Dark, moody background for contrast
    
    # Add background particles for extra visual flair
    if random.random() < 0.3:
        particles.append(Particle(random.randint(0, WIDTH), 0))

    # Update and draw particles
    for particle in particles[:]:
        particle.update()
        if rainbow_mode:
            particle.color = (
                (pygame.time.get_ticks() // 10 + particle.x) % 255,
                (pygame.time.get_ticks() // 15 + particle.y) % 255,
                (pygame.time.get_ticks() // 20 + particle.x + particle.y) % 255
            )
        particle.draw()
        if particle.life <= 0 or particle.y > HEIGHT + 10:
            particles.remove(particle)

    # Target logic
    if target_timer > 0:
        target_timer -= 1
        target.draw()
    else:
        target = Target()
        target_timer = 180
        score -= 50  # Penalty for missing target

    # Draw HUD if font is available
    if font:
        try:
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            instr_text = font.render("Click anywhere to explode! Hit targets for points! R for Rainbow", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(instr_text, (10, 40))
            if target_timer > 0:
                time_text = font.render(f"Time: {target_timer//60 + 1}", True, (255, 255, 255))
                screen.blit(time_text, (10, 70))
        except Exception as e:
            print(f"HUD rendering failed: {e}")
    else:
        print("No font available, skipping HUD rendering")

    # Update display
    try:
        pygame.display.flip()
    except Exception as e:
        print(f"Display update failed: {e}")
        running = False

    clock.tick(FPS)

# Cleanup
print("Shutting down...")
pygame.quit()
sys.exit(0)