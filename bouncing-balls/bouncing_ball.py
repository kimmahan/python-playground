import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
SQUARE_SIZE = 300
BALL_RADIUS = 15
ROTATION_SPEED = 0.5  # degrees per frame
BALL_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Square with Bouncing Ball")
clock = pygame.time.Clock()

# Ball properties
ball_pos = np.array([0.0, 0.0])  # Relative to square center
ball_vel = np.array([BALL_SPEED, BALL_SPEED])

# Square rotation angle
angle = 0

def rotate_point(point, angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    return np.dot(rotation_matrix, point)

def check_collision(pos):
    # Check collision with square boundaries (in local space)
    half_size = SQUARE_SIZE / 2 - BALL_RADIUS
    new_pos = pos.copy()
    new_vel = ball_vel.copy()
    
    if abs(pos[0]) > half_size:
        new_pos[0] = half_size if pos[0] > 0 else -half_size
        new_vel[0] *= -1
        
    if abs(pos[1]) > half_size:
        new_pos[1] = half_size if pos[1] > 0 else -half_size
        new_vel[1] *= -1
        
    return new_pos, new_vel

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Update
    angle = (angle + ROTATION_SPEED) % 360
    
    # Update ball position (in local space)
    ball_pos += ball_vel
    ball_pos, ball_vel = check_collision(ball_pos)
    
    # Transform ball position to screen space
    rotated_ball_pos = rotate_point(ball_pos, angle)
    screen_ball_pos = rotated_ball_pos + np.array([WIDTH/2, HEIGHT/2])
    
    # Draw
    screen.fill(BLACK)
    
    # Draw rotating square
    square_points = [
        rotate_point(np.array([-SQUARE_SIZE/2, -SQUARE_SIZE/2]), angle),
        rotate_point(np.array([SQUARE_SIZE/2, -SQUARE_SIZE/2]), angle),
        rotate_point(np.array([SQUARE_SIZE/2, SQUARE_SIZE/2]), angle),
        rotate_point(np.array([-SQUARE_SIZE/2, SQUARE_SIZE/2]), angle)
    ]
    
    # Offset points to screen center
    screen_points = [(p[0] + WIDTH/2, p[1] + HEIGHT/2) for p in square_points]
    
    # Draw square
    pygame.draw.polygon(screen, WHITE, screen_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, YELLOW, screen_ball_pos.astype(int), BALL_RADIUS)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()