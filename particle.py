import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Explosion Madness")
clock = pygame.time.Clock()

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

particles = []
running = True
rainbow_mode = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for _ in range(100):  # Create explosion of 100 particles
                particles.append(Particle(mx, my))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Toggle rainbow mode
                rainbow_mode = not rainbow_mode

    # Update and draw particles
    screen.fill((20, 20, 40))  # Dark background
    
    # Add random background particles
    if random.random() < 0.3:
        particles.append(Particle(random.randint(0, WIDTH), 0))
    
    for particle in particles[:]:
        particle.update()
        if rainbow_mode:
            particle.color = (
                (pygame.time.get_ticks() // 10 + particle.x) % 255,
                (pygame.time.get_ticks() // 15 + particle.y) % 255,
                (pygame.time.get_ticks() // 20 + particle.x + particle.y) % 255
            )
        particle.draw()
        if particle.life <= 0 or particle.y > HEIGHT:
            particles.remove(particle)

    # Display instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Click to Explode! Press R for Rainbow Mode", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()