import pygame
import random
import math

pygame.init()
pygame.mixer.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Celestial Fireworks Display")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
gold = (255, 215, 0)
rainbow_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

# Define create_sine_wave HERE, before it's used
def create_sine_wave(freq, duration, sample_rate=44100):
    import numpy as np
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return (32767 * np.sin(2 * np.pi * freq * t)).astype(np.int16)

# Sounds (simple sine waves for demonstration)
explosion_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(create_sine_wave(440, 0.2)))
rainbow_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(create_sine_wave(880, 0.5)))  # Higher pitch for triumph

# Starfield
stars = []
for _ in range(200):
    x = random.randint(0, width)
    y = random.randint(0, height)
    size = random.randint(1, 3)
    stars.append([x, y, size])

# Particle class
class Particle:
    def __init__(self, x, y, color, size, dx, dy):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.dx = dx
        self.dy = dy
        self.gravity = 0.1

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity
        self.size = max(0, self.size - 0.05)  # Particles fade out

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Fireworks function
def create_fireworks(x, y, rainbow=False):
    particles = []
    num_particles = 80
    for _ in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        color = random.choice(rainbow_colors) if rainbow else random.choice([red, blue, gold])
        size = random.randint(2, 5)
        particles.append(Particle(x, y, color, size, dx, dy))
    return particles

# Game variables
fireworks = []
score = 0
rainbow_mode = False
click_count = 0
mouse_trail = []


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x > width - 100 and y < 100:  # Easter egg check
                click_count += 1
                if click_count >= 10:
                    rainbow_mode = True
                    score *= 2  # Double score for rainbow
                    rainbow_sound.play()
            else:
               click_count = 0 # reset if not in the easter egg area
               
            new_fireworks = create_fireworks(x, y, rainbow_mode)
            fireworks.extend(new_fireworks)
            explosion_sound.play()
            score += 50
    
    # Mouse trail
    mouse_trail.append(pygame.mouse.get_pos())
    if len(mouse_trail) > 20: # Keep trail length reasonable
        mouse_trail.pop(0)

    screen.fill(black)

    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, white, (star[0], star[1]), star[2])

    # Update and draw fireworks
    for i in range(len(fireworks) - 1, -1, -1):  # Iterate backwards for safe removal
        firework = fireworks[i]
        firework.update()
        firework.draw(screen)
        if firework.size <= 0:
            del fireworks[i]

    # Draw mouse trail
    for i, pos in enumerate(mouse_trail):
        pygame.draw.circle(screen, (150,150,150), pos, 5 - i*0.2) # Diminishing size

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()