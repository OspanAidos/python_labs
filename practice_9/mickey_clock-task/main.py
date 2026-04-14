import pygame
from clock import MickeyClock 

pygame.init()
WIDTH, HEIGHT = 1245, 938
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

my_clock = MickeyClock(center_point=(600, 400))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    my_clock.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()