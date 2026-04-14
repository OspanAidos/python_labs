import pygame
import sys
from player import MusicPlayer

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Pygame Music Player")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    # Путь к папке с музыкой (убедись, что она создана!)
    player = MusicPlayer("music")

    while True:
        screen.fill((30, 30, 30))  # Темный фон
        
        # Текстовая информация
        status = "Playing" if player.is_playing else "Stopped"
        track_info = font.render(f"Track: {player.get_current_track_name()}", True, (255, 255, 255))
        status_info = font.render(f"Status: {status}", True, (0, 255, 0) if player.is_playing else (255, 0, 0))
        controls_hint = font.render("P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (200, 200, 200))

        screen.blit(track_info, (50, 100))
        screen.blit(status_info, (50, 150))
        screen.blit(controls_hint, (50, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()