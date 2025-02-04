import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.8
BALL_RADIUS = 10
HEX_RADIUS = 200
ROTATION_SPEED = 0.5  # degrees per frame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Rotating Hexagon")
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0])
    
    def update(self):
        # Apply gravity
        self.vel[1] += GRAVITY
        
        # Update position
        self.pos += self.vel

class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center = np.array([center_x, center_y])
        self.radius = radius
        self.angle = 0  # rotation angle in degrees
        self.vertices = self.calculate_vertices()
    
    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle_rad = math.radians(self.angle + i * 60)
            x = self.center[0] + self.radius * math.cos(angle_rad)
            y = self.center[1] + self.radius * math.sin(angle_rad)
            vertices.append(np.array([x, y]))
        return vertices
    
    def rotate(self):
        self.angle += ROTATION_SPEED
        self.vertices = self.calculate_vertices()
    
    def draw(self, screen):
        vertices = [(int(v[0]), int(v[1])) for v in self.vertices]
        pygame.draw.polygon(screen, WHITE, vertices, 2)

def check_collision(ball, hexagon):
    for i in range(6):
        # Get line segment (wall) from hexagon
        p1 = hexagon.vertices[i]
        p2 = hexagon.vertices[(i + 1) % 6]
        
        # Vector from p1 to p2 (wall vector)
        wall = p2 - p1
        wall_norm = np.linalg.norm(wall)
        wall_unit = wall / wall_norm
        
        # Vector from p1 to ball
        to_ball = ball.pos - p1
        
        # Project ball position onto wall vector
        proj_length = np.dot(to_ball, wall_unit)
        
        # Find closest point on wall to ball
        if proj_length < 0:
            closest = p1
        elif proj_length > wall_norm:
            closest = p2
        else:
            closest = p1 + wall_unit * proj_length
        
        # Check if ball is colliding with wall
        dist = np.linalg.norm(ball.pos - closest)
        if dist < BALL_RADIUS:
            # Calculate normal vector of the wall
            normal = np.array([-wall_unit[1], wall_unit[0]])
            if np.dot(normal, to_ball) < 0:
                normal = -normal
            
            # Move ball out of wall
            ball.pos = closest + normal * BALL_RADIUS
            
            # Reflect velocity with friction
            vel_normal = np.dot(ball.vel, normal) * normal
            vel_tangent = ball.vel - vel_normal
            ball.vel = vel_tangent * FRICTION - vel_normal * FRICTION

# Create game objects
ball = Ball(WIDTH//2, HEIGHT//2)
hexagon = Hexagon(WIDTH//2, HEIGHT//2, HEX_RADIUS)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Reset ball position and give it random velocity
                ball.pos = np.array([WIDTH//2, HEIGHT//2], dtype=float)
                ball.vel = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 0)])
    
    # Update
    hexagon.rotate()
    ball.update()
    check_collision(ball, hexagon)
    
    # Draw
    screen.fill(BLACK)
    hexagon.draw(screen)
    pygame.draw.circle(screen, RED, (int(ball.pos[0]), int(ball.pos[1])), BALL_RADIUS)
    pygame.display.flip()
    
    # Cap framerate
    clock.tick(FPS)

pygame.quit()