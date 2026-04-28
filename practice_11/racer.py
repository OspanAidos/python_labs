import pygame
import random
import sys

SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 500
FPS           = 60
ROAD_LEFT, ROAD_RIGHT = 80, 420
SPEED_UP_EVERY = 5

WHITE, BLACK, RED, GREEN, YELLOW, GRAY = (255, 255, 255), (0, 0, 0), (200, 0, 0), (0, 200, 0), (255, 215, 0), (100, 100, 100)

COIN_TYPES = [
    {"label": "$",  "face": (255, 215, 0),   "ring": (200, 160, 0), "text": (120,  80, 0), "value": 1,  "weight": 60},
    {"label": "2$", "face": (192, 192, 192), "ring": (150, 150, 150),"text": (60,  60, 60), "value": 2,  "weight": 25},
    {"label": "5$", "face": (255, 100, 100), "ring": (200,  50,  50),"text": (120,   0, 0), "value": 5,  "weight": 10},
    {"label": "★",  "face": (100, 200, 255), "ring": ( 50, 150, 220),"text": (  0,  80,160), "value":10,  "weight": 5},
]

_COIN_POOL = []
for _ct in COIN_TYPES: _COIN_POOL.extend([_ct] * _ct["weight"])

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, 40, 70), border_radius=6)
        pygame.draw.rect(self.image, WHITE, (5, 5, 30, 20), border_radius=3)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT: self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT: self.rect.x += self.speed

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        color = random.choice([(0, 100, 200), (0, 180, 0), (180, 0, 180)])
        pygame.draw.rect(self.image, color, (0, 0, 40, 70), border_radius=6)
        pygame.draw.rect(self.image, WHITE, (5, 45, 30, 20), border_radius=3)
        self.rect = self.image.get_rect(x=random.randint(ROAD_LEFT, ROAD_RIGHT - 40), y=-80)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT: self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        ct = random.choice(_COIN_POOL)
        self.value, size = ct["value"], 24
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ct["face"], (size//2, size//2), size//2)
        pygame.draw.circle(self.image, ct["ring"], (size//2, size//2), size//2, 2)
        font = pygame.font.SysFont("Arial", 10 if len(ct["label"]) > 1 else 14, bold=True)
        label = font.render(ct["label"], True, ct["text"])
        self.image.blit(label, label.get_rect(center=(size//2, size//2)))
        self.rect = self.image.get_rect(x=random.randint(ROAD_LEFT, ROAD_RIGHT - size), y=-30)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT: self.kill()

class RoadStripe:
    def __init__(self):
        self.y, self.gap = 0, 60
    def update(self, speed): self.y = (self.y + speed) % self.gap
    def draw(self, surface):
        x, y = SCREEN_WIDTH // 2 - 4, self.y - self.gap
        while y < SCREEN_HEIGHT:
            pygame.draw.rect(surface, WHITE, (x, y, 8, 30))
            y += self.gap

def draw_road(surface):
    surface.fill(GRAY)
    pygame.draw.rect(surface, (50, 50, 50), (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))
    pygame.draw.rect(surface, WHITE, (ROAD_LEFT - 5, 0, 5, SCREEN_HEIGHT))
    pygame.draw.rect(surface, WHITE, (ROAD_RIGHT, 0, 5, SCREEN_HEIGHT))

def draw_hud(surface, font, score, coins, speed):
    surface.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    surface.blit(font.render(f"Coins: {coins}", True, YELLOW), (SCREEN_WIDTH - 120, 10))
    surface.blit(font.render(f"Speed: {speed}", True, GREEN), (SCREEN_WIDTH // 2 - 40, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock, font, big_font = pygame.time.Clock(), pygame.font.SysFont("Arial", 22, bold=True), pygame.font.SysFont("Arial", 48, bold=True)
    all_sprites, enemy_group, coin_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    player = PlayerCar()
    all_sprites.add(player)
    stripe = RoadStripe()
    score, coins_collected, scroll_speed, speed_ups = 0, 0, 4, 0
    e_timer, c_timer, game_over = 0, 0, False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over: main(); return
        if not game_over:
            score += 1
            e_timer += 1
            if e_timer >= max(40, 80 - score // 200):
                e = EnemyCar(scroll_speed); enemy_group.add(e); all_sprites.add(e); e_timer = 0
            c_timer += 1
            if c_timer >= random.randint(90, 180):
                c = Coin(scroll_speed); coin_group.add(c); all_sprites.add(c); c_timer = 0
            all_sprites.update(); stripe.update(scroll_speed)
            if pygame.sprite.spritecollide(player, enemy_group, False): game_over = True
            for c in pygame.sprite.spritecollide(player, coin_group, True): coins_collected += c.value
            if coins_collected // SPEED_UP_EVERY > speed_ups:
                speed_ups = coins_collected // SPEED_UP_EVERY
                scroll_speed = min(scroll_speed + 1, 14)
                for s in enemy_group: s.speed = scroll_speed
                for s in coin_group: s.speed = scroll_speed
        draw_road(screen); stripe.draw(screen); all_sprites.draw(screen); draw_hud(screen, font, score // 10, coins_collected, scroll_speed)
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 160)); screen.blit(overlay, (0, 0))
            screen.blit(big_font.render("GAME OVER", True, RED), (120, 180))
            screen.blit(font.render(f"Score: {score // 10} | Coins: {coins_collected}", True, WHITE), (150, 250))
            screen.blit(font.render("Press R to restart", True, GREEN), (160, 310))
        pygame.display.flip()

if __name__ == "__main__": main()