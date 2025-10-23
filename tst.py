import pygame, sys

particles = pygame.sprite.Group()


WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Wave Simulation")

clock = pygame.time.Clock()


# --- Define a Circle Sprite ---
class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, particle_size=2):
        super().__init__()

        # Create an image surface for the sprite
        self.image = pygame.Surface((particle_size*2, particle_size*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (particle_size, particle_size), particle_size)
        self.rect = self.image.get_rect(center=(x, y))

circle = Circle(200, 200, (255, 0, 0))
particles.add(circle)

# --- Main loop ---
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    dt = clock.tick(60) / 1000  # delta time in seconds

    # Update and draw all sprites
    screen.fill((30, 30, 30))
    particles.draw(screen)

    pygame.display.flip()