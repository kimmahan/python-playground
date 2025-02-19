import pygame
import random
import math
import sys

# Initialize Pygame with debug info
print("Starting Celestial Fireworks Display...")
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
    pygame.display.set_caption("Celestial Fireworks Display")
    clock = pygame.time.Clock()
    print("Display set up successfully")
except Exception as e:
    print(f"Display setup failed: {e}")
    sys.exit(1)

# Initialize sound (using Pygame mixer for simple sound effects)
pygame.mixer.init()
try:
    explosion_sound = pygame.mixer.Sound(buffer=bytes([0x52, 0x49, 0x46, 0x46, 0x24, 0x08, 0x00, 0x00, 0x57, 0x41, 0x56, 0x45, 0x66, 0x6D, 0x74, 0x20, 0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x44, 0xAC, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00, 0x02, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))  # Simple boom sound
    triumph_sound = pygame.mixer.Sound(buffer=bytes([0x52, 0x49, 0x46, 0x46, 0x34, 0x08, 0x00, 0x00, 0x57, 0x41, 0x56, 0x45, 0x66, 0x6D, 0x74, 0x20, 0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x44, 0xAC, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00, 0x02, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61, 0x10, 0x08, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF]))  # Simple triumph sound
    print("Sounds initialized successfully")
except Exception as e:
    print(f"Sound initialization failed: {e}")
    explosion_sound = None
    triumph_sound = None

class Particle:
    def __init__(self, x, y, rainbow=False):
        self.x = x
        self.y = y
        self.size = random.randint(2, 8)
        self.life = random.randint(20, 60)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        if rainbow:
            self.color = (0, 0, 0)  # Will be updated dynamically for rainbow
        else:
            colors = [(255, 0, 0), (0, 0, 255), (255, 215, 0)]  # Red, Blue, Gold
            self.color = random.choice(colors)

    def update(self, rainbow_mode):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.life -= 1
        self.size = max(1, self.size * 0.98)
        if rainbow_mode and self.life > 0:
            t = pygame.time.get_ticks() / 1000
            self.color = (
                int(128 + 127 * math.sin(t + self.x / 100)),
                int(128 + 127 * math.cos(t + self.y / 100)),
                int(128 + 127 * math.sin(t + (self.x + self.y) / 100))
            )

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class TrailParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 3)
        self.life = random.randint(10, 20)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(1, self.size * 0.95)

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Game variables
particles = []
trail_particles = []
running = True
rainbow_mode = False
score = 0
top_right_clicks = 0  # Track clicks in top-right corner for Easter egg

# Starry background
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

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
            # Check for Easter egg (top-right corner, within 100 pixels of edge)
            if mx > WIDTH - 100 and my < 100:
                top_right_clicks += 1
                if top_right_clicks >= 10 and not rainbow_mode:
                    rainbow_mode = True
                    if triumph_sound:
                        triumph_sound.play()
                    print("Easter egg activated: Rainbow Fireworks!")
            else:
                top_right_clicks = 0  # Reset if not in top-right
            # Launch fireworks
            for _ in range(100):  # Big, impressive explosion
                particles.append(Particle(mx, my, rainbow_mode))
            if explosion_sound:
                explosion_sound.play()
            score += 50 * (2 if rainbow_mode else 1)  # Score: 50 for normal, 100 for rainbow

    # Clear screen (dark starry sky)
    screen.fill((0, 0, 0))
    
    # Draw twinkling stars
    for x, y in stars:
        if random.random() < 0.1:  # 10% chance to sparkle brighter
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 2)
        else:
            pygame.draw.circle(screen, (200, 200, 200), (x, y), 1)

    # Update and draw particles
    for particle in particles[:]:
        particle.update(rainbow_mode)
        particle.draw()
        if particle.life <= 0 or particle.y > HEIGHT + 10:
            particles.remove(particle)

    # Update and draw mouse trail particles
    mx, my = pygame.mouse.get_pos()
    trail_particles.append(TrailParticle(mx, my))
    for trail in trail_particles[:]:
        trail.update()
        trail.draw()
        if trail.life <= 0:
            trail_particles.remove(trail)
    if len(trail_particles) > 50:  # Limit trail length for performance
        trail_particles.pop(0)

    # Draw score if font is available
    if font:
        try:
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
        except Exception as e:
            print(f"Score rendering failed: {e}")
    else:
        print("No font available, skipping score rendering")

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