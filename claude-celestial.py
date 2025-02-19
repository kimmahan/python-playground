import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Fireworks Display")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GOLD = (255, 215, 0)
COLORS = [RED, BLUE, GOLD]

# Score tracking
score = 0
font = pygame.font.SysFont('Arial', 24)

# Generate sound effects using simple approach
def create_sound_effects():
    # Create a simple beep sound effect
    sample_rate = 44100
    duration = 0.3  # seconds
    
    # Create simple sound buffers with proper dimensions for stereo
    buffer_size = int(sample_rate * duration)
    
    # Explosion sound - lower frequency
    explosion_buffer = bytearray()
    for i in range(buffer_size):
        # Generate a simple sine wave at 440Hz that fades out
        value = int(127 * math.sin(2 * math.pi * 440 * i / sample_rate) * (1 - i/buffer_size))
        # Add the same value to both left and right channels (stereo)
        explosion_buffer.extend([value + 128, value + 128])
    explosion_sound = pygame.mixer.Sound(buffer=explosion_buffer)
    explosion_sound.set_volume(0.3)
    
    # Rainbow sound - higher frequency
    rainbow_buffer = bytearray()
    for i in range(buffer_size):
        # Higher pitch note (880Hz) with longer sustain
        value = int(127 * math.sin(2 * math.pi * 880 * i / sample_rate) * (1 - i/buffer_size)**2)
        rainbow_buffer.extend([value + 128, value + 128])
    rainbow_sound = pygame.mixer.Sound(buffer=rainbow_buffer)
    rainbow_sound.set_volume(0.3)
    
    return explosion_sound, rainbow_sound

# Create the sound effects
explosion_sound, rainbow_sound = create_sound_effects()

# Star class for background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2)
        self.twinkle_speed = random.uniform(0.02, 0.05)
        self.brightness = random.uniform(0.3, 1.0)
        self.phase = random.uniform(0, 2 * math.pi)
        
    def update(self):
        # Make stars twinkle by varying brightness
        self.phase += self.twinkle_speed
        self.brightness = 0.5 + 0.5 * math.sin(self.phase)
        
    def draw(self):
        alpha = int(255 * self.brightness)
        color = (min(255, int(200 + 55 * self.brightness)), 
                min(255, int(200 + 55 * self.brightness)), 
                min(255, int(200 + 55 * self.brightness)))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

# Particle class for fireworks
class Particle:
    def __init__(self, x, y, color, is_rainbow=False):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        self.is_rainbow = is_rainbow
        
        # Random velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Lifetime and fade
        self.lifetime = random.uniform(1.5, 3.0)
        self.age = 0
        
        # For rainbow particles, cycle through colors
        if is_rainbow:
            self.color_cycle_speed = random.uniform(0.05, 0.1)
            self.hue = random.uniform(0, 1.0)
    
    def update(self, dt):
        # Update position with gravity
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        
        # Age the particle
        self.age += dt
        
        # Update color for rainbow particles
        if self.is_rainbow:
            self.hue = (self.hue + self.color_cycle_speed) % 1.0
            # Convert HSV to RGB (simplified)
            h = self.hue * 6
            i = int(h)
            f = h - i
            q = 1 - f
            if i == 0:
                self.color = (255, int(255 * f), 0)
            elif i == 1:
                self.color = (int(255 * q), 255, 0)
            elif i == 2:
                self.color = (0, 255, int(255 * f))
            elif i == 3:
                self.color = (0, int(255 * q), 255)
            elif i == 4:
                self.color = (int(255 * f), 0, 255)
            else:
                self.color = (255, 0, int(255 * q))
    
    def is_alive(self):
        return self.age < self.lifetime
    
    def draw(self):
        # Calculate alpha based on age
        alpha = max(0, int(255 * (1 - self.age / self.lifetime)))
        color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
        
        # Draw with transparency
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

# Firework explosion
class Explosion:
    def __init__(self, x, y, is_rainbow=False):
        self.particles = []
        particle_count = random.randint(50, 100)
        
        for _ in range(particle_count):
            if is_rainbow:
                color = random.choice(COLORS)  # Initial color (will cycle)
                self.particles.append(Particle(x, y, color, True))
            else:
                color = random.choice(COLORS)
                self.particles.append(Particle(x, y, color))
    
    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self):
        for particle in self.particles:
            particle.draw()
    
    def is_active(self):
        return len(self.particles) > 0

# Cursor trail
class CursorTrail:
    def __init__(self):
        self.positions = []
        self.max_length = 20
    
    def update(self, pos):
        self.positions.append(pos)
        if len(self.positions) > self.max_length:
            self.positions.pop(0)
    
    def draw(self):
        if len(self.positions) <= 1:
            return
            
        for i in range(1, len(self.positions)):
            alpha = int(255 * (i / len(self.positions)))
            color = (200, 200, 255, alpha)
            start_pos = self.positions[i-1]
            end_pos = self.positions[i]
            
            # Draw line with thickness based on position
            thickness = int(i / 2) + 1
            pygame.draw.line(screen, color, start_pos, end_pos, thickness)

# Main game function
def main():
    global score
    
    # Create stars
    stars = [Star() for _ in range(200)]
    
    # Explosions list
    explosions = []
    
    # Cursor trail
    cursor_trail = CursorTrail()
    
    # Easter egg tracking
    corner_clicks = []
    corner_threshold = 10  # Number of clicks needed
    corner_area = (WIDTH - 100, 0, 100, 100)  # Top-right corner area
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    
                    # Check if click is in corner (for Easter egg)
                    if x > corner_area[0] and y < corner_area[3]:
                        corner_clicks.append(pygame.time.get_ticks())
                        # Remove clicks older than 5 seconds
                        corner_clicks = [t for t in corner_clicks if pygame.time.get_ticks() - t < 5000]
                    
                    # Check if Easter egg is triggered
                    is_rainbow = len(corner_clicks) >= corner_threshold
                    
                    # Create explosion
                    explosions.append(Explosion(x, y, is_rainbow))
                    
                    # Play sound
                    if is_rainbow:
                        rainbow_sound.play()
                        score += 100  # Double points for rainbow
                    else:
                        explosion_sound.play()
                        score += 50
        
        # Get mouse position for cursor trail
        cursor_pos = pygame.mouse.get_pos()
        cursor_trail.update(cursor_pos)
        
        # Clear screen
        screen.fill(BLACK)
        
        # Update and draw stars
        for star in stars:
            star.update()
            star.draw()
        
        # Update and draw explosions
        for explosion in explosions:
            explosion.update(dt)
            explosion.draw()
        
        # Remove inactive explosions
        explosions = [e for e in explosions if e.is_active()]
        
        # Draw cursor trail
        cursor_trail.draw()
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        # Update display
        pygame.display.flip()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()