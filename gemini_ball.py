import pygame
import math

# Initialize Pygame
pygame.init()

# Set window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Square")

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_x_speed = 5
ball_y_speed = 5
ball_color = (255, 255, 0)  # Yellow

# Square properties
square_size = 300
square_x = (width - square_size) // 2
square_y = (height - square_size) // 2
square_color = (255, 255, 255)  # White
square_angle = 0
rotation_speed = 0.1  # Degrees per frame

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the ball
    ball_x += ball_x_speed
    ball_y += ball_y_speed

    # Collision detection with square walls (consider rotation)
    square_center_x = square_x + square_size // 2
    square_center_y = square_y + square_size // 2

    # Calculate ball's position relative to the rotating square
    ball_rel_x = ball_x - square_center_x
    ball_rel_y = ball_y - square_center_y
    rotated_x = ball_rel_x * math.cos(math.radians(-square_angle)) - ball_rel_y * math.sin(math.radians(-square_angle))
    rotated_y = ball_rel_x * math.sin(math.radians(-square_angle)) + ball_rel_y * math.cos(math.radians(-square_angle))

    # Check for collisions with the rotated square's boundaries
    if rotated_x + ball_radius > square_size // 2:
        ball_x_speed *= -1
    if rotated_x - ball_radius < -square_size // 2:
        ball_x_speed *= -1
    if rotated_y + ball_radius > square_size // 2:
        ball_y_speed *= -1
    if rotated_y - ball_radius < -square_size // 2:
        ball_y_speed *= -1

    # Rotate the square
    square_angle += rotation_speed

    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Draw the rotating square
    rotated_square = pygame.transform.rotate(pygame.Surface((square_size, square_size)), square_angle)
    rotated_rect = rotated_square.get_rect(center=(square_center_x, square_center_y))
    screen.blit(rotated_square, rotated_rect)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()