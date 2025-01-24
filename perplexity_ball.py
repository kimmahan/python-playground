import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Square")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 5
ball_speed_y = 5

# Square properties
square_size = 400
square_center = (width // 2, height // 2)
square_angle = 0
rotation_speed = 0.5

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def rotate_point(point, center, angle):
    x, y = point
    cx, cy = center
    s, c = math.sin(angle), math.cos(angle)
    x, y = x - cx, y - cy
    new_x = x * c - y * s
    new_y = x * s + y * c
    return new_x + cx, new_y + cy

def check_collision(ball_pos, square_corners):
    x, y = ball_pos
    for i in range(4):
        x1, y1 = square_corners[i]
        x2, y2 = square_corners[(i + 1) % 4]
        
        normal = (y2 - y1, x1 - x2)
        length = math.sqrt(normal[0]**2 + normal[1]**2)
        normal = (normal[0] / length, normal[1] / length)
        
        distance = abs((x - x1) * normal[0] + (y - y1) * normal[1])
        
        if distance <= ball_radius:
            return True, normal
    return False, None

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(WHITE)

    # Update square rotation
    square_angle += math.radians(rotation_speed)

    # Calculate rotated square corners
    half_size = square_size // 2
    corners = [
        (-half_size, -half_size),
        (half_size, -half_size),
        (half_size, half_size),
        (-half_size, half_size)
    ]
    rotated_corners = [rotate_point(corner, (0, 0), square_angle) for corner in corners]
    square_corners = [(x + square_center[0], y + square_center[1]) for x, y in rotated_corners]

    # Draw rotated square
    pygame.draw.polygon(screen, BLACK, square_corners, 2)

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collision with square
    collision, normal = check_collision((ball_x, ball_y), square_corners)
    if collision:
        # Reflect ball's velocity
        dot_product = ball_speed_x * normal[0] + ball_speed_y * normal[1]
        ball_speed_x = ball_speed_x - 2 * dot_product * normal[0]
        ball_speed_y = ball_speed_y - 2 * dot_product * normal[1]

    # Draw ball
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)