import pygame
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Celestial Fireworks Display")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FIREWORK_COLORS = [(255, 0, 0), (0, 0, 255), (255, 215, 0)]
RAINBOW_COLORS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

# Clock
clock = pygame.time.Clock()

# Function to generate a simple sine wave sound with stereo formatting
def generate_sound(frequency=500, duration=300, sample_rate=44100):
    """Generate a simple sine wave sound for Pygame."""
    t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), endpoint=False)
    wave = (np.sin(2 * np.pi * frequency * t) * 32767).astype(np.int16)

    # Convert to 2D stereo format
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

# Generate explosion and triumph sounds
explosion_sound = generate_sound(600, 500)
triumph_sound = generate_sound(800, 700)

# Starry Background
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)) for _ in range(100)]

# Fireworks and trails storage
fireworks = []
trails = []
score = 0
easter_egg_clicks = 0
easter_egg_active = False

# Particle class
class Particle:
    def __init__(self, x, y, color, speed, angle, lifetime=50):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.angle = angle
        self.lifetime = lifetime
        self.gravity = 0.15  # Simulated gravity

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle) + self.gravity
        self.lifetime -= 1

# Function to create a firework explosion
def create_firework(x, y):
    global score, easter_egg_active
    color_choices = RAINBOW_COLORS if easter_egg
