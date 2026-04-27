"""
paint.py — Paint Application (TSIS 2)
Controls:
  Tools      : P pencil | L line | R rect | C circle | E eraser
               F fill   | T text | S square | G right-triangle
               Q equilateral-triangle | H rhombus
  Brush size : 1 small(2px)  2 medium(5px)  3 large(10px)
  Save       : Ctrl+S  → saves canvas as timestamped .png
  Color pick : click a swatch in the palette
"""

import sys
import datetime
import pygame

from tools import (
    PencilTool, LineTool, RectangleTool, CircleTool, EraserTool,
    FillTool, TextTool, SquareTool, RightTriangleTool,
    EquilateralTriangleTool, RhombusTool,
)

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
SCREEN_W, SCREEN_H = 1200, 750
TOOLBAR_H = 64
CANVAS_TOP = TOOLBAR_H
CANVAS_H = SCREEN_H - TOOLBAR_H

BG_COLOR      = (30, 30, 35)
TOOLBAR_COLOR = (22, 22, 28)
CANVAS_BG     = (255, 255, 255)
ACCENT        = (90, 140, 255)
TEXT_COLOR    = (220, 220, 230)
HOVER_COLOR   = (55, 55, 65)
ACTIVE_COLOR  = (70, 110, 200)

BRUSH_SIZES = {1: 2, 2: 5, 3: 10}   # key → px

PALETTE = [
    (0,   0,   0),   (80,  80,  80), (160, 160, 160), (255, 255, 255),
    (220, 50,  50),  (230, 130, 50), (230, 210, 50),  (60,  190, 80),
    (50,  160, 230), (80,  80,  220),(160, 60,  200),  (220, 80,  150),
    (100, 50,  20),  (30,  100, 80), (0,   60,  120),  (200, 170, 100),
]

TOOL_DEFS = [
    ("P",  "Pencil",   PencilTool()),
    ("L",  "Line",     LineTool()),
    ("R",  "Rect",     RectangleTool()),
    ("C",  "Circle",   CircleTool()),
    ("S",  "Square",   SquareTool()),
    ("G",  "R.Tri",    RightTriangleTool()),
    ("Q",  "Eq.Tri",   EquilateralTriangleTool()),
    ("H",  "Rhombus",  RhombusTool()),
    ("E",  "Eraser",   EraserTool()),
    ("F",  "Fill",     FillTool()),
    ("T",  "Text",     TextTool()),
]

KEY_MAP = {
    pygame.K_p: "Pencil",
    pygame.K_l: "Line",
    pygame.K_r: "Rect",
    pygame.K_c: "Circle",
    pygame.K_s: "Square",
    pygame.K_g: "R.Tri",
    pygame.K_q: "Eq.Tri",
    pygame.K_h: "Rhombus",
    pygame.K_e: "Eraser",
    pygame.K_f: "Fill",
    pygame.K_t: "Text",
}


# ─────────────────────────────────────────────
#  Helper: draw a rounded rect
# ─────────────────────────────────────────────
def draw_rounded_rect(surface, color, rect, radius=8):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


# ─────────────────────────────────────────────
#  Toolbar
# ─────────────────────────────────────────────
class Toolbar:
    BTN_W, BTN_H = 62, 44
    BTN_GAP = 4
    SIDE_PAD = 8

    def __init__(self, font_small, font_key):
        self.font_small = font_small
        self.font_key   = font_key
        self._build_layout()

    def _build_layout(self):
        """Pre-calculate button rects."""
        self.tool_rects = {}          # name → Rect
        self.size_rects = {}          # 1/2/3 → Rect
        self.palette_rects = {}       # color → Rect

        x = self.SIDE_PAD
        cy = TOOLBAR_H // 2

        # Tool buttons
        for shortcut, name, _tool in TOOL_DEFS:
            rect = pygame.Rect(x, cy - self.BTN_H // 2, self.BTN_W, self.BTN_H)
            self.tool_rects[name] = (rect, shortcut)
            x += self.BTN_W + self.BTN_GAP

        x += 12  # separator gap

        # Brush size buttons
        for k in (1, 2, 3):
            rect = pygame.Rect(x, cy - 18, 36, 36)
            self.size_rects[k] = rect
            x += 40

        x += 12  # separator gap

        # Palette swatches
        sw = 26
        gap = 3
        per_row = 8
        for i, color in enumerate(PALETTE):
            row = i // per_row
            col = i % per_row
            rx = x + col * (sw + gap)
            ry = cy - (sw + gap) // 2 - row * (sw + gap) + 2
            self.palette_rects[color] = pygame.Rect(rx, ry, sw, sw)

    def draw(self, surface, active_tool_name, active_size, active_color):
        # Background
        pygame.draw.rect(surface, TOOLBAR_COLOR, (0, 0, SCREEN_W, TOOLBAR_H))
        pygame.draw.line(surface, (50, 50, 60), (0, TOOLBAR_H - 1), (SCREEN_W, TOOLBAR_H - 1))

        # Tool buttons
        for name, (rect, shortcut) in self.tool_rects.items():
            color = ACTIVE_COLOR if name == active_tool_name else HOVER_COLOR
            draw_rounded_rect(surface, color, rect, 6)
            label = self.font_small.render(name, True, TEXT_COLOR)
            key_lbl = self.font_key.render(shortcut, True, (150, 200, 255))
            surface.blit(label, label.get_rect(centerx=rect.centerx, centery=rect.centery + 4))
            surface.blit(key_lbl, key_lbl.get_rect(centerx=rect.centerx, centery=rect.centery - 10))

        # Size buttons
        dot_sizes = {1: 3, 2: 6, 3: 10}
        for k, rect in self.size_rects.items():
            color = ACTIVE_COLOR if k == active_size else HOVER_COLOR
            draw_rounded_rect(surface, color, rect, 6)
            pygame.draw.circle(surface, TEXT_COLOR, rect.center, dot_sizes[k])

        # Palette
        for color, rect in self.palette_rects.items():
            draw_rounded_rect(surface, color, rect, 4)
            if color == active_color:
                pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=4)

    def hit_tool(self, pos):
        for name, (rect, _) in self.tool_rects.items():
            if rect.collidepoint(pos):
                return name
        return None

    def hit_size(self, pos):
        for k, rect in self.size_rects.items():
            if rect.collidepoint(pos):
                return k
        return None

    def hit_color(self, pos):
        for color, rect in self.palette_rects.items():
            if rect.collidepoint(pos):
                return color
        return None


# ─────────────────────────────────────────────
#  Status bar
# ─────────────────────────────────────────────
def draw_status(surface, font, tool_name, size_px, color, mouse_pos, message=""):
    bar_y = SCREEN_H - 22
    pygame.draw.rect(surface, TOOLBAR_COLOR, (0, bar_y, SCREEN_W, 22))
    cx, cy = mouse_pos
    info = f"  Tool: {tool_name}   Size: {size_px}px   Pos: ({cx}, {cy - CANVAS_TOP})"
    if message:
        info += f"   {message}"
    txt = font.render(info, True, (140, 140, 155))
    surface.blit(txt, (6, bar_y + 4))
    # Color preview
    pygame.draw.rect(surface, color, (SCREEN_W - 40, bar_y + 3, 16, 16), border_radius=3)


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Paint — TSIS 2")
    clock = pygame.time.Clock()

    # Fonts
    font_ui     = pygame.font.SysFont("segoeui",    11, bold=True)
    font_key    = pygame.font.SysFont("consolas",   11, bold=True)
    font_status = pygame.font.SysFont("consolas",   12)

    # Canvas surface (persistent drawing target)
    canvas = pygame.Surface((SCREEN_W, CANVAS_H))
    canvas.fill(CANVAS_BG)

    # Preview overlay (drawn on top each frame, not blit to canvas until confirmed)
    preview = pygame.Surface((SCREEN_W, CANVAS_H), pygame.SRCALPHA)

    toolbar = Toolbar(font_ui, font_key)

    # State
    tool_map   = {name: tool for _, name, tool in TOOL_DEFS}
    active_name = "Pencil"
    active_tool = tool_map[active_name]
    active_size = 2           # key 1/2/3
    active_color = (0, 0, 0)
    drawing = False
    status_msg = ""
    status_timer = 0

    def set_tool(name):
        nonlocal active_name, active_tool, drawing
        active_name = name
        active_tool = tool_map[name]
        drawing = False

    def canvas_pos(screen_pos):
        return (screen_pos[0], screen_pos[1] - CANVAS_TOP)

    def in_canvas(screen_pos):
        return screen_pos[1] >= CANVAS_TOP

    def show_msg(msg, duration=120):
        nonlocal status_msg, status_timer
        status_msg = msg
        status_timer = duration

    def save_canvas():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{ts}.png"
        pygame.image.save(canvas, filename)
        show_msg(f"Saved: {filename}")

    # ── event loop ────────────────────────────
    running = True
    while running:
        size_px = BRUSH_SIZES[active_size]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── keyboard ──────────────────────
            elif event.type == pygame.KEYDOWN:
                text_tool = tool_map["Text"]
                if isinstance(active_tool, type(text_tool)) and text_tool.is_active:
                    # Delegate all keys to text tool
                    text_tool.handle_key(event, canvas, active_color, active_size)
                else:
                    mods = pygame.key.get_mods()
                    if event.key == pygame.K_s and mods & pygame.KMOD_CTRL:
                        save_canvas()
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        active_size = event.key - pygame.K_0
                    elif event.key in KEY_MAP:
                        set_tool(KEY_MAP[event.key])

            # ── mouse down ────────────────────
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if pos[1] < CANVAS_TOP:
                    # Toolbar click
                    hit_t = toolbar.hit_tool(pos)
                    hit_s = toolbar.hit_size(pos)
                    hit_c = toolbar.hit_color(pos)
                    if hit_t:
                        set_tool(hit_t)
                    elif hit_s:
                        active_size = hit_s
                    elif hit_c:
                        active_color = hit_c
                else:
                    drawing = True
                    active_tool.on_mouse_down(canvas, canvas_pos(pos), active_color, size_px)

            # ── mouse drag ────────────────────
            elif event.type == pygame.MOUSEMOTION:
                if drawing and in_canvas(event.pos):
                    active_tool.on_mouse_drag(canvas, canvas_pos(event.pos), active_color, size_px)

            # ── mouse up ──────────────────────
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and in_canvas(event.pos):
                    active_tool.on_mouse_up(canvas, canvas_pos(event.pos), active_color, size_px)
                drawing = False

        # ── draw frame ────────────────────────
        screen.fill(BG_COLOR)

        # Canvas
        screen.blit(canvas, (0, CANVAS_TOP))

        # Preview overlay
        preview.fill((0, 0, 0, 0))
        active_tool.draw_preview(preview, active_color, size_px)
        screen.blit(preview, (0, CANVAS_TOP))

        # Toolbar
        toolbar.draw(screen, active_name, active_size, active_color)

        # Status bar
        if status_timer > 0:
            status_timer -= 1
            if status_timer == 0:
                status_msg = ""
        mouse_screen = pygame.mouse.get_pos()
        draw_status(screen, font_status, active_name, size_px, active_color, mouse_screen, status_msg)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()