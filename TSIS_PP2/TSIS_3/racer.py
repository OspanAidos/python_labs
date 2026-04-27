"""
racer.py — Core gameplay for TSIS 3 Racer.
Handles: road, player car, traffic, obstacles, power-ups, coins, HUD, scoring.
"""

import pygame
import random
import math
from persistence import DIFFICULTY_PARAMS
from sound import SoundManager

# ── colors ───────────────────────────────────
C_WHITE  = (240, 240, 255)
C_BLACK  = (10,  10,  15)
C_ROAD   = (35,  35,  48)
C_MARK   = (200, 180, 40)
C_CURB_L = (230, 60,  60)
C_CURB_R = (240, 240, 240)
C_GRASS  = (40,  90,  40)
C_GRAY   = (100, 100, 120)
C_ACCENT = (255, 200, 0)
C_GREEN  = (60,  200, 100)
C_RED    = (220, 60,  60)
C_BLUE   = (60,  130, 230)
C_SHIELD = (80,  160, 255)
C_NITRO  = (255, 140, 0)
C_OIL    = (20,  20,  30)
C_BUMP   = (180, 140, 60)
C_STRIP  = (80,  220, 120)
C_PANEL  = (18,  18,  28)

LANE_COUNT = 6
COIN_VALS  = [(1, 0.60), (3, 0.30), (5, 0.10)]   # (value, probability)

POWER_TIMEOUT = 8_000   # ms before uncollected power-up despawns
NITRO_DUR     = 4_000   # ms
SHIELD_DUR    = 99_999  # until hit
REPAIR_DUR    = 1        # instant (ms, just for display)


# ─────────────────────────────────────────────
#  Utility
# ─────────────────────────────────────────────
def rand_lane(W, lanes=LANE_COUNT):
    lw = W // lanes
    return random.randint(0, lanes - 1) * lw + lw // 2


def draw_rounded_rect(surf, color, rect, r=8, width=0):
    pygame.draw.rect(surf, color, rect, width, border_radius=r)


# ─────────────────────────────────────────────
#  Player car
# ─────────────────────────────────────────────
class PlayerCar:
    W, H = 44, 76

    def __init__(self, screen_w, screen_h, color):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.color    = color
        self.x        = screen_w // 2
        self.y        = screen_h - 120
        self.speed    = 5
        self.shield   = False
        self.nitro    = False

    @property
    def rect(self):
        return pygame.Rect(self.x - self.W // 2, self.y - self.H // 2, self.W, self.H)

    def move(self, keys):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]:
            self.y += self.speed
        self.x = max(self.W // 2, min(self.screen_w - self.W // 2, self.x))
        self.y = max(self.H // 2, min(self.screen_h - self.H // 2, self.y))

    def draw(self, surf):
        r = self.rect
        # Body
        pygame.draw.rect(surf, self.color, r, border_radius=8)
        # Windshield
        ws = pygame.Rect(r.left + 6, r.top + 12, r.width - 12, 20)
        pygame.draw.rect(surf, (120, 200, 240), ws, border_radius=4)
        # Wheels
        for wx, wy in [(r.left - 4, r.top + 8), (r.right - 2, r.top + 8),
                       (r.left - 4, r.bottom - 24), (r.right - 2, r.bottom - 24)]:
            pygame.draw.rect(surf, C_BLACK, (wx, wy, 10, 18), border_radius=3)
        # Headlights
        for hx in [r.left + 6, r.right - 14]:
            pygame.draw.rect(surf, (255, 240, 180), (hx, r.top + 4, 8, 6), border_radius=2)
        # Shield aura
        if self.shield:
            pygame.draw.ellipse(surf, (*C_SHIELD, 0), r.inflate(16, 16), 3)
            pygame.draw.ellipse(surf, C_SHIELD, r.inflate(16, 16), 2)
        # Nitro flame
        if self.nitro:
            flame_pts = [
                (self.x - 8, r.bottom),
                (self.x,     r.bottom + random.randint(14, 26)),
                (self.x + 8, r.bottom),
            ]
            pygame.draw.polygon(surf, C_NITRO, flame_pts)


# ─────────────────────────────────────────────
#  Enemy / Traffic car
# ─────────────────────────────────────────────
ENEMY_COLORS = [(200, 80, 80), (80, 160, 200), (80, 200, 120),
                (200, 160, 60), (160, 80, 200), (200, 200, 200)]

class EnemyCar:
    W, H = 44, 76

    def __init__(self, x, y, speed):
        self.x     = x
        self.y     = float(y)
        self.speed = speed
        self.color = random.choice(ENEMY_COLORS)

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.W // 2, int(self.y) - self.H // 2, self.W, self.H)

    def update(self):
        self.y += self.speed

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.color, r, border_radius=8)
        ws = pygame.Rect(r.left + 6, r.top + 12, r.width - 12, 20)
        pygame.draw.rect(surf, (120, 200, 240), ws, border_radius=4)
        for wx, wy in [(r.left - 4, r.top + 8), (r.right - 2, r.top + 8),
                       (r.left - 4, r.bottom - 24), (r.right - 2, r.bottom - 24)]:
            pygame.draw.rect(surf, C_BLACK, (wx, wy, 10, 18), border_radius=3)


# ─────────────────────────────────────────────
#  Coin
# ─────────────────────────────────────────────
class Coin:
    def __init__(self, x, y, value):
        self.x, self.y = float(x), float(y)
        self.value = value
        self.radius = {1: 10, 3: 13, 5: 16}.get(value, 10)
        self.color  = {1: C_ACCENT, 3: (200, 200, 200), 5: (255, 130, 60)}.get(value, C_ACCENT)

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius,
                           self.radius * 2, self.radius * 2)

    def update(self, speed):
        self.y += speed

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surf, C_BLACK,    (int(self.x), int(self.y)), self.radius, 2)
        lbl = pygame.font.SysFont("consolas", 11, bold=True).render(str(self.value), True, C_BLACK)
        surf.blit(lbl, lbl.get_rect(center=(int(self.x), int(self.y))))


# ─────────────────────────────────────────────
#  Power-Up
# ─────────────────────────────────────────────
POWERUP_DEFS = {
    "nitro":  {"color": C_NITRO,  "label": "N", "desc": "Nitro"},
    "shield": {"color": C_SHIELD, "label": "S", "desc": "Shield"},
    "repair": {"color": C_GREEN,  "label": "R", "desc": "Repair"},
}

class PowerUp:
    SIZE = 32

    def __init__(self, x, y, kind):
        self.x, self.y = float(x), float(y)
        self.kind      = kind
        self.spawned   = pygame.time.get_ticks()
        self._font     = pygame.font.SysFont("impact", 18)

    @property
    def rect(self):
        s = self.SIZE
        return pygame.Rect(int(self.x) - s // 2, int(self.y) - s // 2, s, s)

    def expired(self):
        return pygame.time.get_ticks() - self.spawned > POWER_TIMEOUT

    def update(self, speed):
        self.y += speed

    def draw(self, surf):
        d = POWERUP_DEFS[self.kind]
        draw_rounded_rect(surf, d["color"], self.rect, 6)
        pygame.draw.rect(surf, C_WHITE, self.rect, 2, border_radius=6)
        lbl = self._font.render(d["label"], True, C_BLACK)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))


# ─────────────────────────────────────────────
#  Road Obstacle  (oil spill / speed bump / nitro strip)
# ─────────────────────────────────────────────
OBSTACLE_DEFS = {
    "oil":   {"color": C_OIL,  "w": 70, "h": 36, "label": "OIL"},
    "bump":  {"color": C_BUMP, "w": 80, "h": 18, "label": "BUMP"},
    "strip": {"color": C_STRIP,"w": 80, "h": 16, "label": "NITRO"},
}

class RoadObstacle:
    def __init__(self, x, y, kind):
        self.x, self.y = float(x), float(y)
        self.kind      = kind
        d = OBSTACLE_DEFS[kind]
        self.w, self.h = d["w"], d["h"]
        self._font = pygame.font.SysFont("consolas", 11, bold=True)

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - self.w // 2, int(self.y) - self.h // 2, self.w, self.h)

    def update(self, speed):
        self.y += speed

    def draw(self, surf):
        d = OBSTACLE_DEFS[self.kind]
        draw_rounded_rect(surf, d["color"], self.rect, 6)
        lbl = self._font.render(d["label"], True, C_WHITE)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))


# ─────────────────────────────────────────────
#  Road renderer
# ─────────────────────────────────────────────
class Road:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.lw     = W // LANE_COUNT
        self.offset = 0.0
        self.dash_h = 36
        self.gap_h  = 28

    def update(self, scroll_speed):
        self.offset = (self.offset + scroll_speed) % (self.dash_h + self.gap_h)

    def draw(self, surf):
        # Grass
        surf.fill(C_GRASS)
        # Road body
        pygame.draw.rect(surf, C_ROAD, (0, 0, self.W, self.H))
        # Curb stripes left/right
        for y in range(-40, self.H + 40, 40):
            yo = (y + int(self.offset * 2)) % (self.H + 80) - 40
            pygame.draw.rect(surf, C_CURB_L, (0,          yo, 12, 20))
            pygame.draw.rect(surf, C_CURB_R, (self.W - 12, yo, 12, 20))
        # Lane dashes
        for lane in range(1, LANE_COUNT):
            x = lane * self.lw
            y = self.offset - self.dash_h
            while y < self.H:
                pygame.draw.rect(surf, C_MARK, (x - 2, y, 4, self.dash_h))
                y += self.dash_h + self.gap_h


# ─────────────────────────────────────────────
#  HUD
# ─────────────────────────────────────────────
class HUD:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.font_lg = pygame.font.SysFont("impact",   26)
        self.font_sm = pygame.font.SysFont("consolas", 17)

    def draw(self, surf, score, coins, distance, finish_dist,
             active_pu, pu_time_left, difficulty):
        panel = pygame.Rect(0, 0, self.W, 52)
        s = pygame.Surface((self.W, 52), pygame.SRCALPHA)
        pygame.draw.rect(s, (14, 14, 22, 200), s.get_rect())
        surf.blit(s, (0, 0))

        # Score
        self._text(surf, self.font_lg, f"Score: {score}", 14, 14, C_ACCENT)
        # Coins
        self._text(surf, self.font_sm, f"Coins: {coins}", 220, 18, C_WHITE)
        # Distance
        pct = min(1.0, distance / max(finish_dist, 1))
        self._text(surf, self.font_sm, f"Dist: {distance}m / {finish_dist}m", 360, 18, C_WHITE)
        # Progress bar
        bar = pygame.Rect(360, 36, 240, 10)
        pygame.draw.rect(surf, C_GRAY,  bar, border_radius=4)
        pygame.draw.rect(surf, C_GREEN, pygame.Rect(bar.left, bar.top, int(bar.width * pct), bar.height), border_radius=4)
        # Active power-up
        if active_pu:
            d = POWERUP_DEFS[active_pu]
            secs = max(0, pu_time_left // 1000)
            self._text(surf, self.font_sm, f"[{d['desc']}] {secs}s", self.W - 200, 18, d["color"])
        # Difficulty
        self._text(surf, self.font_sm, difficulty.upper(), self.W - 80, 18, C_GRAY)

    def _text(self, surf, font, text, x, y, color):
        lbl = font.render(text, True, color)
        surf.blit(lbl, (x, y))


# ─────────────────────────────────────────────
#  Game session
# ─────────────────────────────────────────────
class RacerGame:
    FINISH_DIST = 3000   # metres to finish

    def __init__(self, screen, clock, settings, player_name):
        self.screen      = screen
        self.clock       = clock
        self.settings    = settings
        self.player_name = player_name
        self.W, self.H   = screen.get_size()

        diff_key  = settings.get("difficulty", "normal")
        self.diff = DIFFICULTY_PARAMS[diff_key]
        car_color = tuple(settings.get("car_color", [220, 60, 60]))

        self.road    = Road(self.W, self.H)
        self.player  = PlayerCar(self.W, self.H, car_color)
        self.hud     = HUD(self.W, self.H)

        self.enemies   = []
        self.coins     = []
        self.powerups  = []
        self.obstacles = []

        self.scroll_speed = 5.0 * self.diff["scale"]
        self.base_enemy_speed = self.diff["enemy_speed"]
        self.spawn_rate = self.diff["spawn_rate"]

        self.score        = 0
        self.coins_count  = 0
        self.distance     = 0.0    # metres
        self.alive        = True
        self.crashed      = False

        # Active power-up state
        self.active_pu      = None
        self.pu_end_time    = 0

        # Sound
        sound_on = settings.get("sound", True)
        self.sfx = SoundManager(enabled=sound_on)
        self.sfx.start_engine()

        # Timing
        self.last_time = pygame.time.get_ticks()

    # ── helpers ──────────────────────────────
    def _safe_spawn_x(self, existing_rects):
        lw = self.W // LANE_COUNT
        for _ in range(20):
            x = rand_lane(self.W)
            r = pygame.Rect(x - 30, -80, 60, 80)
            if all(not r.colliderect(er) for er in existing_rects):
                return x
        return rand_lane(self.W)

    def _existing_top_rects(self):
        return [e.rect for e in self.enemies] + [c.rect for c in self.coins] + \
               [p.rect for p in self.powerups] + [o.rect for o in self.obstacles]

    def _activate_powerup(self, kind):
        self.active_pu   = kind
        now = pygame.time.get_ticks()
        if kind == "nitro":
            self.player.nitro  = True
            self.player.shield = False
            self.pu_end_time   = now + NITRO_DUR
        elif kind == "shield":
            self.player.shield = True
            self.player.nitro  = False
            self.pu_end_time   = now + SHIELD_DUR
        elif kind == "repair":
            self.active_pu   = None   # instant
            self.crashed     = False

    def _expire_powerup(self):
        now = pygame.time.get_ticks()
        if self.active_pu and now >= self.pu_end_time:
            if self.active_pu == "nitro":
                self.player.nitro = False
            elif self.active_pu == "shield":
                self.player.shield = False
            self.active_pu = None

    # ── main loop ────────────────────────────
    def run(self):
        """Return (score, distance_int, coins)."""
        while self.alive:
            now = pygame.time.get_ticks()
            dt  = now - self.last_time
            self.last_time = now

            self._handle_events()
            self._update(now, dt)
            self._draw(now)
            self.clock.tick(60)

        self.sfx.stop_engine()
        return int(self.score), int(self.distance), self.coins_count

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.alive = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.alive = False

    def _update(self, now, dt):
        # Difficulty scaling over time
        progress = min(1.0, self.distance / self.FINISH_DIST)
        scroll   = self.scroll_speed + progress * 4.0
        if self.player.nitro:
            scroll *= 1.6

        # Road scroll
        self.road.update(scroll)

        # Distance
        self.distance += scroll * 0.04   # ~metres

        # Score: distance + bonus
        self.score = int(self.distance * 0.5 + self.coins_count * 10)

        # Player movement
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # Expire power-up
        self._expire_powerup()

        # ── Spawn logic ──────────────────────
        existing = self._existing_top_rects()
        spawn_r  = self.spawn_rate + progress * 0.02

        # Enemy cars
        if random.random() < spawn_r:
            x = self._safe_spawn_x(existing)
            spd = self.base_enemy_speed + progress * 3
            self.enemies.append(EnemyCar(x, -50, spd + scroll * 0.5))
            existing = self._existing_top_rects()

        # Coins
        if random.random() < 0.04:
            x = rand_lane(self.W)
            vals, weights = zip(*COIN_VALS)
            v = random.choices(vals, weights)[0]
            self.coins.append(Coin(x, -20, v))

        # Power-ups (only one on screen at a time)
        if not self.powerups and random.random() < 0.004:
            x = rand_lane(self.W)
            kind = random.choice(["nitro", "shield", "repair"])
            self.powerups.append(PowerUp(x, -20, kind))

        # Road obstacles
        if random.random() < spawn_r * 0.6:
            x = rand_lane(self.W)
            kind = random.choices(["oil", "bump", "strip"], weights=[0.5, 0.3, 0.2])[0]
            self.obstacles.append(RoadObstacle(x, -20, kind))

        # ── Update entities ──────────────────
        for e in self.enemies:
            e.update()
        for c in self.coins:
            c.update(scroll)
        for p in self.powerups:
            p.update(scroll)
        for o in self.obstacles:
            o.update(scroll)

        # ── Cull off-screen ──────────────────
        self.enemies   = [e for e in self.enemies   if e.y < self.H + 100]
        self.coins     = [c for c in self.coins     if c.y < self.H + 60]
        self.powerups  = [p for p in self.powerups  if p.y < self.H + 60 and not p.expired()]
        self.obstacles = [o for o in self.obstacles if o.y < self.H + 60]

        # Engine pitch tracks speed
        self.sfx.set_engine_pitch(scroll / 10.0)

        # ── Collisions ───────────────────────
        pr = self.player.rect

        # Enemy collision
        for e in self.enemies[:]:
            if pr.colliderect(e.rect):
                if self.player.shield:
                    self.player.shield = False
                    self.active_pu = None
                    self.enemies.remove(e)
                    self.sfx.play("shield")
                else:
                    self.sfx.play("crash")
                    self.alive = False
                    return

        # Obstacle collision
        for o in self.obstacles[:]:
            if pr.colliderect(o.rect):
                if o.kind == "oil":
                    self.player.x += random.choice([-1, 1]) * 30
                    self.sfx.play("bump")
                elif o.kind == "bump":
                    scroll *= 0.5
                    self.sfx.play("bump")
                elif o.kind == "strip":
                    if not self.player.nitro:
                        self._activate_powerup("nitro")
                        self.sfx.play("nitro")
                self.obstacles.remove(o)

        # Coin pickup
        for c in self.coins[:]:
            if pr.colliderect(c.rect):
                self.coins_count += c.value
                self.score       += c.value * 15
                self.coins.remove(c)
                self.sfx.play("coin")

        # Power-up pickup
        for p in self.powerups[:]:
            if pr.colliderect(p.rect):
                self._activate_powerup(p.kind)
                self.powerups.remove(p)
                self.sfx.play("powerup")

        # Check finish
        if self.distance >= self.FINISH_DIST:
            self.score += 500   # finish bonus
            self.alive = False

    def _draw(self, now):
        self.road.draw(self.screen)
        for o in self.obstacles:
            o.draw(self.screen)
        for c in self.coins:
            c.draw(self.screen)
        for p in self.powerups:
            p.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        self.player.draw(self.screen)

        pu_tl = max(0, self.pu_end_time - now) if self.active_pu else 0
        self.hud.draw(
            self.screen, self.score, self.coins_count,
            int(self.distance), self.FINISH_DIST,
            self.active_pu, pu_tl,
            self.settings.get("difficulty", "normal"),
        )
        pygame.display.flip()