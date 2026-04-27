"""
ui.py — All non-gameplay Pygame screens.
Screens: MainMenu, UsernameScreen, LeaderboardScreen, SettingsScreen, GameOverScreen
"""

import pygame
from persistence import load_leaderboard, load_settings, save_settings

# ── palette ──────────────────────────────────
C_BG       = (14, 14, 22)
C_ROAD     = (30, 30, 40)
C_ACCENT   = (255, 200, 0)
C_WHITE    = (240, 240, 255)
C_GRAY     = (100, 100, 120)
C_RED      = (220, 60, 60)
C_GREEN    = (60, 200, 100)
C_BLUE     = (60, 130, 230)
C_DARK     = (22, 22, 35)
C_PANEL    = (28, 28, 42)

CAR_COLOR_OPTIONS = [
    ("Red",    (220, 60,  60)),
    ("Blue",   (60,  130, 230)),
    ("Green",  (60,  200, 100)),
    ("Yellow", (230, 200, 40)),
    ("Purple", (160, 60,  220)),
    ("White",  (230, 230, 240)),
]


# ─────────────────────────────────────────────
#  Drawing helpers
# ─────────────────────────────────────────────
def draw_rect_alpha(surface, color, rect, alpha=180, radius=10):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=radius)
    surface.blit(s, rect.topleft)


def draw_button(surface, font, text, rect, hovered=False,
                color=C_ACCENT, text_color=C_DARK, radius=10):
    col = tuple(min(255, c + 30) for c in color) if hovered else color
    pygame.draw.rect(surface, col, rect, border_radius=radius)
    lbl = font.render(text, True, text_color)
    surface.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def draw_title(surface, font, text, cx, y, color=C_ACCENT):
    lbl = font.render(text, True, color)
    surface.blit(lbl, lbl.get_rect(centerx=cx, top=y))


def draw_stripe_bg(surface, W, H, offset):
    """Animated road stripe background."""
    surface.fill(C_BG)
    stripe_w = W // 6
    for i in range(7):
        x = i * stripe_w
        pygame.draw.rect(surface, C_ROAD, (x, 0, stripe_w - 4, H))
    # dashed center lines
    dash_h, gap_h = 30, 20
    for lane in range(1, 6):
        x = lane * stripe_w - 2
        y = (offset % (dash_h + gap_h)) - dash_h
        while y < H:
            pygame.draw.rect(surface, C_ACCENT, (x, y, 4, dash_h))
            y += dash_h + gap_h


# ─────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────
class MainMenu:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.font_title  = pygame.font.SysFont("impact",    72)
        self.font_sub    = pygame.font.SysFont("impact",    28)
        self.font_btn    = pygame.font.SysFont("segoeui",   22, bold=True)
        self.offset      = 0
        labels = ["Play", "Leaderboard", "Settings", "Quit"]
        btn_w, btn_h = 240, 52
        start_y = H // 2 - 20
        self.buttons = {}
        for i, lbl in enumerate(labels):
            rect = pygame.Rect(W // 2 - btn_w // 2, start_y + i * (btn_h + 12), btn_w, btn_h)
            self.buttons[lbl] = rect

    def run(self, screen, clock):
        """Return one of: 'play', 'leaderboard', 'settings', 'quit'."""
        while True:
            self.offset += 1
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for lbl, rect in self.buttons.items():
                        if rect.collidepoint(mp):
                            return lbl.lower()

            draw_stripe_bg(screen, self.W, self.H, self.offset)

            # Title panel
            draw_rect_alpha(screen, C_DARK, pygame.Rect(self.W//2 - 220, 60, 440, 130), 200, 16)
            draw_title(screen, self.font_title, "RACER", self.W // 2, 70, C_ACCENT)
            draw_title(screen, self.font_sub,   "TSIS 3 — Arcade Edition", self.W // 2, 155, C_GRAY)

            for lbl, rect in self.buttons.items():
                hovered = rect.collidepoint(mp)
                clr = C_RED if lbl == "Quit" else C_ACCENT
                draw_button(screen, self.font_btn, lbl, rect, hovered, clr)

            pygame.display.flip()
            clock.tick(60)


# ─────────────────────────────────────────────
#  Username entry
# ─────────────────────────────────────────────
class UsernameScreen:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.font_title = pygame.font.SysFont("impact",   48)
        self.font_input = pygame.font.SysFont("consolas", 32)
        self.font_hint  = pygame.font.SysFont("segoeui",  18)
        self.offset     = 0

    def run(self, screen, clock):
        """Return the entered username string (or '' if escaped)."""
        name = ""
        cursor_timer = 0
        while True:
            self.offset += 1
            cursor_timer += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ""
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        return name.strip()
                    elif event.key == pygame.K_ESCAPE:
                        return ""
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 16 and event.unicode.isprintable():
                        name += event.unicode

            draw_stripe_bg(screen, self.W, self.H, self.offset)
            cx = self.W // 2

            draw_rect_alpha(screen, C_DARK, pygame.Rect(cx - 280, self.H//2 - 130, 560, 260), 210, 16)
            draw_title(screen, self.font_title, "Enter Your Name", cx, self.H//2 - 120, C_ACCENT)

            # Input box
            box = pygame.Rect(cx - 200, self.H//2 - 30, 400, 52)
            pygame.draw.rect(screen, C_PANEL, box, border_radius=8)
            pygame.draw.rect(screen, C_ACCENT, box, 2, border_radius=8)
            cursor = "|" if (cursor_timer // 30) % 2 == 0 else ""
            txt = self.font_input.render(name + cursor, True, C_WHITE)
            screen.blit(txt, txt.get_rect(center=box.center))

            hint = self.font_hint.render("Press Enter to start · Esc to go back", True, C_GRAY)
            screen.blit(hint, hint.get_rect(centerx=cx, top=self.H//2 + 40))

            pygame.display.flip()
            clock.tick(60)


# ─────────────────────────────────────────────
#  Leaderboard
# ─────────────────────────────────────────────
class LeaderboardScreen:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.font_title = pygame.font.SysFont("impact",   48)
        self.font_row   = pygame.font.SysFont("consolas", 20)
        self.font_hdr   = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_btn   = pygame.font.SysFont("segoeui",  20, bold=True)
        self.offset     = 0

    def run(self, screen, clock):
        board = load_leaderboard()
        back_btn = pygame.Rect(self.W // 2 - 90, self.H - 72, 180, 46)
        while True:
            self.offset += 1
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_btn.collidepoint(mp):
                        return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            draw_stripe_bg(screen, self.W, self.H, self.offset)
            cx = self.W // 2

            panel = pygame.Rect(cx - 360, 30, 720, self.H - 110)
            draw_rect_alpha(screen, C_DARK, panel, 215, 16)

            draw_title(screen, self.font_title, "LEADERBOARD", cx, 44, C_ACCENT)

            # Header
            cols = [("#", 60), ("Name", 200), ("Score", 340), ("Dist (m)", 480), ("Coins", 610)]
            hy = 115
            for label, ox in cols:
                lbl = self.font_hdr.render(label, True, C_ACCENT)
                screen.blit(lbl, (panel.left + ox, hy))
            pygame.draw.line(screen, C_GRAY, (panel.left + 40, hy + 26), (panel.right - 40, hy + 26))

            for i, entry in enumerate(board):
                y = hy + 36 + i * 32
                row_color = C_ACCENT if i == 0 else (C_WHITE if i < 3 else C_GRAY)
                data = [
                    (f"{i+1}.",          60),
                    (entry.get("name",  "?")[:14], 200),
                    (str(entry.get("score",    0)),  340),
                    (str(entry.get("distance", 0)),  480),
                    (str(entry.get("coins",    0)),  610),
                ]
                for text, ox in data:
                    lbl = self.font_row.render(text, True, row_color)
                    screen.blit(lbl, (panel.left + ox, y))

            draw_button(screen, self.font_btn, "Back", back_btn, back_btn.collidepoint(mp), C_GRAY, C_WHITE)
            pygame.display.flip()
            clock.tick(60)


# ─────────────────────────────────────────────
#  Settings
# ─────────────────────────────────────────────
class SettingsScreen:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.font_title = pygame.font.SysFont("impact",   48)
        self.font_lbl   = pygame.font.SysFont("segoeui",  22, bold=True)
        self.font_btn   = pygame.font.SysFont("segoeui",  20, bold=True)
        self.offset     = 0

    def run(self, screen, clock, settings: dict) -> dict:
        """Modify and return settings dict."""
        import copy
        s = copy.deepcopy(settings)

        cx = self.W // 2
        # Toggle: sound
        sound_rect = pygame.Rect(cx + 60, 200, 160, 44)
        # Difficulty buttons
        diff_rects = {}
        for i, d in enumerate(["easy", "normal", "hard"]):
            diff_rects[d] = pygame.Rect(cx - 210 + i * 150, 310, 130, 44)
        # Car color swatches
        color_rects = {}
        for i, (name, col) in enumerate(CAR_COLOR_OPTIONS):
            row, ci = divmod(i, 3)
            color_rects[name] = (
                col,
                pygame.Rect(cx - 200 + ci * 140, 420 + row * 70, 120, 54),
            )
        # Back button
        back_btn = pygame.Rect(cx - 90, self.H - 72, 180, 46)

        while True:
            self.offset += 1
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_settings(s)
                    return s
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    save_settings(s)
                    return s
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if sound_rect.collidepoint(mp):
                        s["sound"] = not s["sound"]
                    for d, rect in diff_rects.items():
                        if rect.collidepoint(mp):
                            s["difficulty"] = d
                    for name, (col, rect) in color_rects.items():
                        if rect.collidepoint(mp):
                            s["car_color"] = list(col)
                    if back_btn.collidepoint(mp):
                        save_settings(s)
                        return s

            draw_stripe_bg(screen, self.W, self.H, self.offset)

            panel = pygame.Rect(cx - 360, 30, 720, self.H - 110)
            draw_rect_alpha(screen, C_DARK, panel, 215, 16)
            draw_title(screen, self.font_title, "SETTINGS", cx, 44, C_ACCENT)

            # Sound toggle
            snd_lbl = self.font_lbl.render("Sound:", True, C_WHITE)
            screen.blit(snd_lbl, (cx - 220, 214))
            snd_on = s["sound"]
            draw_button(screen, self.font_btn,
                        "ON" if snd_on else "OFF",
                        sound_rect,
                        sound_rect.collidepoint(mp),
                        C_GREEN if snd_on else C_RED)

            # Difficulty
            diff_lbl = self.font_lbl.render("Difficulty:", True, C_WHITE)
            screen.blit(diff_lbl, (cx - 220, 322))
            for d, rect in diff_rects.items():
                active = s["difficulty"] == d
                col = C_ACCENT if active else C_GRAY
                draw_button(screen, self.font_btn, d.capitalize(), rect, rect.collidepoint(mp), col)

            # Car color
            car_lbl = self.font_lbl.render("Car Color:", True, C_WHITE)
            screen.blit(car_lbl, (cx - 220, 432))
            for name, (col, rect) in color_rects.items():
                pygame.draw.rect(screen, col, rect, border_radius=8)
                active_col = tuple(s["car_color"])
                if tuple(col) == active_col:
                    pygame.draw.rect(screen, C_WHITE, rect, 3, border_radius=8)
                name_lbl = self.font_btn.render(name, True, C_DARK)
                screen.blit(name_lbl, name_lbl.get_rect(center=rect.center))

            draw_button(screen, self.font_btn, "Save & Back", back_btn, back_btn.collidepoint(mp), C_GRAY, C_WHITE)
            pygame.display.flip()
            clock.tick(60)


# ─────────────────────────────────────────────
#  Game Over
# ─────────────────────────────────────────────
class GameOverScreen:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.font_title = pygame.font.SysFont("impact",   64)
        self.font_stat  = pygame.font.SysFont("consolas", 24)
        self.font_btn   = pygame.font.SysFont("segoeui",  22, bold=True)
        self.offset     = 0

    def run(self, screen, clock, score, distance, coins):
        """Return 'retry' or 'menu'."""
        cx = self.W // 2
        retry_btn = pygame.Rect(cx - 210, self.H // 2 + 130, 180, 52)
        menu_btn  = pygame.Rect(cx + 30,  self.H // 2 + 130, 180, 52)
        while True:
            self.offset += 1
            mp = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_btn.collidepoint(mp):
                        return "retry"
                    if menu_btn.collidepoint(mp):
                        return "menu"

            draw_stripe_bg(screen, self.W, self.H, self.offset)
            panel = pygame.Rect(cx - 300, self.H // 2 - 200, 600, 380)
            draw_rect_alpha(screen, C_DARK, panel, 215, 16)

            draw_title(screen, self.font_title, "GAME OVER", cx, self.H // 2 - 190, C_RED)

            stats = [
                ("Score",    str(score)),
                ("Distance", f"{distance} m"),
                ("Coins",    str(coins)),
            ]
            for i, (label, val) in enumerate(stats):
                y = self.H // 2 - 80 + i * 52
                l1 = self.font_stat.render(label + ":", True, C_GRAY)
                l2 = self.font_stat.render(val,         True, C_ACCENT)
                screen.blit(l1, (cx - 240, y))
                screen.blit(l2, (cx + 40,  y))

            draw_button(screen, self.font_btn, "Retry",     retry_btn, retry_btn.collidepoint(mp), C_GREEN)
            draw_button(screen, self.font_btn, "Main Menu", menu_btn,  menu_btn.collidepoint(mp),  C_GRAY, C_WHITE)

            pygame.display.flip()
            clock.tick(60)