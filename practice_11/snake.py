import pygame
import random
import sys

CELL = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

FPS_BASE = 8
FPS_STEP = 2
FOOD_PER_LEVEL = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 160, 0)
GREEN = (0, 200, 0)
RED = (220, 30, 30)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 0, 200)
CYAN = (0, 200, 220)
WALL_COLOR = (80, 80, 80)
BG_COLOR = (15, 15, 15)
GRID_COLOR = (25, 25, 25)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FOOD_TYPES = [
    {"colour": RED, "value": 1, "weight": 50, "lifetime": None},
    {"colour": ORANGE, "value": 2, "weight": 25, "lifetime": 5000},
    {"colour": PURPLE, "value": 3, "weight": 15, "lifetime": 4000},
    {"colour": CYAN, "value": 5, "weight": 7, "lifetime": 3000},
    {"colour": YELLOW, "value": 10, "weight": 3, "lifetime": 2000},
]

_FOOD_POOL = []
for _ft in FOOD_TYPES:
    _FOOD_POOL.extend([_ft] * _ft["weight"])

MAX_FOODS = 3

def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))

def draw_walls(surface):
    pygame.draw.rect(surface, WALL_COLOR, (0, 0, WIDTH, CELL))
    pygame.draw.rect(surface, WALL_COLOR, (0, HEIGHT - CELL, WIDTH, CELL))
    pygame.draw.rect(surface, WALL_COLOR, (0, 0, CELL, HEIGHT))
    pygame.draw.rect(surface, WALL_COLOR, (WIDTH - CELL, 0, CELL, HEIGHT))

def cell_rect(col, row):
    return pygame.Rect(col * CELL, row * CELL, CELL, CELL)

def random_free_position(occupied_set):
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in occupied_set:
            return col, row

def draw_hud(surface, font, score, level):
    surface.blit(font.render(f"Score: {score}", True, WHITE), (CELL + 4, 2))
    lvl = font.render(f"Level: {level}", True, YELLOW)
    surface.blit(lvl, (WIDTH // 2 - lvl.get_width() // 2, 2))

class FoodItem:
    def __init__(self, pos, food_type):
        self.pos = pos
        self.colour = food_type["colour"]
        self.value = food_type["value"]
        self.lifetime = food_type["lifetime"]
        self.born_at = pygame.time.get_ticks()

    def is_expired(self):
        if self.lifetime is None:
            return False
        return (pygame.time.get_ticks() - self.born_at) >= self.lifetime

    def time_left_fraction(self):
        if self.lifetime is None:
            return 1.0
        elapsed = pygame.time.get_ticks() - self.born_at
        return max(0.0, 1.0 - elapsed / self.lifetime)

    def draw(self, surface):
        rect = cell_rect(*self.pos).inflate(-4, -4)
        frac = self.time_left_fraction()
        if self.lifetime is not None:
            r = int(self.colour[0] * frac + 80 * (1 - frac))
            g = int(self.colour[1] * frac + 80 * (1 - frac))
            b = int(self.colour[2] * frac + 80 * (1 - frac))
            draw_colour = (r, g, b)
        else:
            draw_colour = self.colour
        pygame.draw.ellipse(surface, draw_colour, rect)
        if self.lifetime is not None and frac < 0.5:
            pygame.draw.ellipse(surface, WHITE, rect, max(1, int(frac * 4)))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 18, bold=True)
    big_font = pygame.font.SysFont("Consolas", 40, bold=True)

    snake = [(COLS // 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2 - 2, ROWS // 2)]
    direction = RIGHT
    next_direction = RIGHT

    foods = [FoodItem(random_free_position(set(snake)), FOOD_TYPES[0])]
    score = 0
    level = 1
    food_eaten = 0
    fps = FPS_BASE
    game_over = False
    grow = False

    STEP_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(STEP_EVENT, 1000 // fps)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    next_direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    next_direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    next_direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    next_direction = RIGHT
                if event.key == pygame.K_r and game_over:
                    main()
                    return

            if event.type == STEP_EVENT and not game_over:
                direction = next_direction
                hc, hr = snake[0]
                dc, dr = direction
                new_head = (hc + dc, hr + dr)
                nc, nr = new_head

                if nc <= 0 or nc >= COLS - 1 or nr <= 0 or nr >= ROWS - 1:
                    game_over = True
                    continue

                if new_head in snake:
                    game_over = True
                    continue

                snake.insert(0, new_head)
                eaten_food = None
                for food in foods:
                    if food.pos == new_head:
                        eaten_food = food
                        break

                if eaten_food:
                    score += eaten_food.value * 10
                    food_eaten += 1
                    foods.remove(eaten_food)
                    grow = True
                    if food_eaten >= FOOD_PER_LEVEL:
                        level += 1
                        food_eaten = 0
                        fps = FPS_BASE + (level - 1) * FPS_STEP
                        pygame.time.set_timer(STEP_EVENT, 1000 // fps)

                if grow:
                    grow = False
                else:
                    snake.pop()

        if not game_over:
            foods = [f for f in foods if not f.is_expired()]
            occupied = set(snake) | {f.pos for f in foods}
            while len(foods) < MAX_FOODS:
                ftype = random.choice(_FOOD_POOL)
                pos = random_free_position(occupied)
                foods.append(FoodItem(pos, ftype))
                occupied.add(pos)

        screen.fill(BG_COLOR)
        draw_grid(screen)
        draw_walls(screen)

        for i, (col, row) in enumerate(snake):
            colour = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, colour, cell_rect(col, row))
            pygame.draw.rect(screen, BLACK, cell_rect(col, row), 1)

        for food in foods:
            food.draw(screen)

        draw_hud(screen, font, score, level)

        legend_x = WIDTH - CELL * 6
        legend_y = HEIGHT - CELL - len(FOOD_TYPES) * 16 - 4
        for ft in FOOD_TYPES:
            label = f"+{ft['value']} pt" + (f"  {ft['lifetime']//1000}s" if ft["lifetime"] else "  ∞")
            pygame.draw.circle(screen, ft["colour"], (legend_x, legend_y + 6), 5)
            screen.blit(pygame.font.SysFont("Consolas", 11).render(label, True, ft["colour"]), (legend_x + 10, legend_y))
            legend_y += 16

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            over = big_font.render("GAME OVER", True, RED)
            info = font.render(f"Score: {score} | Level: {level}", True, WHITE)
            restart = font.render("Press R to restart", True, YELLOW)
            screen.blit(over, over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
            screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

        pygame.display.flip()

if __name__ == "__main__":
    main()