import pygame
import sys
from ball import Ball

def main():
    pygame.init()
    
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_caption("Moving Ball Game")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    ball = Ball(WIDTH, HEIGHT)

    while True:
        screen.fill((255, 255, 255)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -ball.step)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, ball.step)
                elif event.key == pygame.K_LEFT:
                    ball.move(-ball.step, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(ball.step, 0)

        ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)  

if __name__ == "__main__":
    main()