import pygame
import sys
import math

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 600
TOOLBAR_WIDTH = 180

CANVAS_X = TOOLBAR_WIDTH
CANVAS_Y = 0
CANVAS_W = SCREEN_WIDTH - TOOLBAR_WIDTH
CANVAS_H = SCREEN_HEIGHT

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY  = (60,  60,  60 )
BG_COLOR   = (40,  40,  40 )

PALETTE = [
    (0,   0,   0  ), (255, 255, 255), (200,  20,  20), (220, 120,  30),
    (220, 220,  0 ), ( 20, 180,  20), (  0, 150, 200), ( 30,  80, 200),
    (130,  30, 200), (200,  30, 140), (100, 100, 100), (160,  80,  20),
    (  0, 200, 150), (255, 165,   0), (128,   0, 128), (  0, 128, 128),
    (255, 105, 180), (144, 238, 144), (135, 206, 250), (255, 222, 173),
]

TOOLS = [
    "Pencil",
    "Eraser",
    "Rectangle",
    "Square",
    "Circle",
    "R-Triangle",
    "Eq-Triangle",
    "Rhombus",
]

class Button:
    def __init__(self, rect, label, color=DARK_GRAY, text_color=WHITE):
        self.rect       = pygame.Rect(rect)
        self.label      = label
        self.color      = color
        self.text_color = text_color
        self.active     = False

    def draw(self, surface, font):
        bg = (100, 180, 100) if self.active else self.color
        pygame.draw.rect(surface, bg,          self.rect, border_radius=5)
        pygame.draw.rect(surface, LIGHT_GRAY,  self.rect, 1, border_radius=5)
        text = font.render(self.label, True, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_right_triangle(surface, color, start, end, width):
    ax, ay = start
    bx, by = end
    pygame.draw.polygon(surface, color, [(ax, ay), (bx, ay), (bx, by)], width)

def draw_equilateral_triangle(surface, color, start, end, width):
    ax, ay = start
    bx, by = end
    base_len = abs(bx - ax)
    if base_len == 0: return
    h = int(base_len * math.sqrt(3) / 2)
    apex_y = ay - h if by < ay else ay + h
    pygame.draw.polygon(surface, color, [(ax, ay), (bx, ay), ((ax + bx) // 2, apex_y)], width)

def draw_rhombus(surface, color, start, end, width):
    x1, y1 = min(start[0], end[0]), min(start[1], end[1])
    x2, y2 = max(start[0], end[0]), max(start[1], end[1])
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    pygame.draw.polygon(surface, color, [(mx, y1), (x2, my), (mx, y2), (x1, my)], width)

def draw_square(surface, color, start, end, width):
    dx, dy = end[0] - start[0], end[1] - start[1]
    side = min(abs(dx), abs(dy))
    sx = start[0] + (side if dx >= 0 else -side)
    sy = start[1] + (side if dy >= 0 else -side)
    rect = pygame.Rect(min(start[0], sx), min(start[1], sy), side, side)
    pygame.draw.rect(surface, color, rect, width)

SHAPE_TOOLS = {
    "Rectangle":  (lambda s, c, a, b, w: pygame.draw.rect(s, c, pygame.Rect(min(a[0],b[0]), min(a[1],b[1]), abs(b[0]-a[0]), abs(b[1]-a[1])), w),) * 2,
    "Square":     (draw_square,) * 2,
    "Circle":     (lambda s, c, a, b, w: (pygame.draw.circle(s, c, ((a[0]+b[0])//2, (a[1]+b[1])//2), max(abs(b[0]-a[0]), abs(b[1]-a[1])) // 2, w) if max(abs(b[0]-a[0]), abs(b[1]-a[1])) > 0 else None),) * 2,
    "R-Triangle": (draw_right_triangle,)  * 2,
    "Eq-Triangle":(draw_equilateral_triangle,) * 2,
    "Rhombus":    (draw_rhombus,) * 2,
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("Arial", 13, bold=True)
    small = pygame.font.SysFont("Arial", 11)

    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(WHITE)

    current_tool = "Pencil"
    draw_color   = BLACK
    brush_size   = 5
    eraser_size  = 20
    drawing      = False
    start_pos    = None
    temp_canvas  = None

    tool_buttons = []
    btn_h, btn_gap, btn_y0 = 34, 4, 50
    for i, name in enumerate(TOOLS):
        btn = Button((6, btn_y0 + i * (btn_h + btn_gap), TOOLBAR_WIDTH - 12, btn_h), name)
        if name == current_tool: btn.active = True
        tool_buttons.append(btn)

    controls_y = btn_y0 + len(TOOLS) * (btn_h + btn_gap) + 10
    size_slider_rect = pygame.Rect(10, controls_y + 16, TOOLBAR_WIDTH - 20, 10)
    MAX_BRUSH = 40
    palette_start_y, swatch_size, cols_in_palette = size_slider_rect.y + 30, 26, 4

    clear_btn = Button((10, SCREEN_HEIGHT - 50, TOOLBAR_WIDTH - 20, 36), "Clear", color=(150, 40, 40))

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        canvas_mouse = (mouse_pos[0] - CANVAS_X, mouse_pos[1] - CANVAS_Y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = mouse_pos
                if mx < TOOLBAR_WIDTH:
                    for btn in tool_buttons:
                        if btn.is_clicked(mouse_pos):
                            current_tool = btn.label
                            for b in tool_buttons: b.active = False
                            btn.active = True
                    if clear_btn.is_clicked(mouse_pos): canvas.fill(WHITE)
                    if size_slider_rect.collidepoint(mouse_pos):
                        ratio = (mx - size_slider_rect.x) / size_slider_rect.width
                        brush_size = max(1, min(MAX_BRUSH, int(ratio * MAX_BRUSH)))
                        eraser_size = brush_size * 4
                    for idx, color in enumerate(PALETTE):
                        sx = 10 + (idx % cols_in_palette) * (swatch_size + 4)
                        sy = palette_start_y + (idx // cols_in_palette) * (swatch_size + 4)
                        if pygame.Rect(sx, sy, swatch_size, swatch_size).collidepoint(mouse_pos):
                            draw_color, current_tool = color, "Pencil"
                            for b in tool_buttons: b.active = (b.label == "Pencil")
                elif 0 <= canvas_mouse[0] < CANVAS_W and 0 <= canvas_mouse[1] < CANVAS_H:
                    drawing, start_pos, temp_canvas = True, canvas_mouse, canvas.copy()
                    if current_tool == "Pencil": pygame.draw.circle(canvas, draw_color, canvas_mouse, brush_size)
                    elif current_tool == "Eraser": pygame.draw.circle(canvas, WHITE, canvas_mouse, eraser_size)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and start_pos and current_tool in SHAPE_TOOLS:
                    _, commit_fn = SHAPE_TOOLS[current_tool]
                    commit_fn(canvas, draw_color, start_pos, canvas_mouse, brush_size)
                drawing, start_pos, temp_canvas = False, None, None

            if event.type == pygame.MOUSEMOTION:
                if drawing and 0 <= canvas_mouse[0] < CANVAS_W and 0 <= canvas_mouse[1] < CANVAS_H:
                    if current_tool == "Pencil":
                        prev = (event.pos[0] - event.rel[0] - CANVAS_X, event.pos[1] - event.rel[1] - CANVAS_Y)
                        pygame.draw.line(canvas, draw_color, prev, canvas_mouse, brush_size * 2)
                        pygame.draw.circle(canvas, draw_color, canvas_mouse, brush_size)
                    elif current_tool == "Eraser":
                        pygame.draw.circle(canvas, WHITE, canvas_mouse, eraser_size)

        screen.fill(BG_COLOR)
        if drawing and temp_canvas and current_tool in SHAPE_TOOLS:
            preview = temp_canvas.copy()
            preview_fn, _ = SHAPE_TOOLS[current_tool]
            preview_fn(preview, draw_color, start_pos, canvas_mouse, brush_size)
            screen.blit(preview, (CANVAS_X, CANVAS_Y))
        else:
            screen.blit(canvas, (CANVAS_X, CANVAS_Y))

        pygame.draw.rect(screen, BG_COLOR, (0, 0, TOOLBAR_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(screen, LIGHT_GRAY, (TOOLBAR_WIDTH, 0), (TOOLBAR_WIDTH, SCREEN_HEIGHT), 1)
        screen.blit(font.render("TOOLS", True, LIGHT_GRAY), (10, 10))
        for btn in tool_buttons: btn.draw(screen, font)
        screen.blit(font.render(f"Size: {brush_size}", True, LIGHT_GRAY), (10, controls_y))
        pygame.draw.rect(screen, LIGHT_GRAY, size_slider_rect)
        pygame.draw.rect(screen, (100, 200, 100), (size_slider_rect.x, size_slider_rect.y, int(size_slider_rect.width * brush_size / MAX_BRUSH), 10))
        pygame.draw.rect(screen, WHITE, size_slider_rect, 1)
        screen.blit(font.render("Colors:", True, LIGHT_GRAY), (10, palette_start_y - 18))
        for idx, color in enumerate(PALETTE):
            sx = 10 + (idx % cols_in_palette) * (swatch_size + 4)
            sy = palette_start_y + (idx // cols_in_palette) * (swatch_size + 4)
            swatch = pygame.Rect(sx, sy, swatch_size, swatch_size)
            pygame.draw.rect(screen, color, swatch, border_radius=4)
            if color == draw_color: pygame.draw.rect(screen, WHITE, swatch, 2, border_radius=4)
        pygame.draw.rect(screen, draw_color, (10, palette_start_y + ((len(PALETTE) + 3) // 4) * (swatch_size + 4) + 4, TOOLBAR_WIDTH - 20, 22), border_radius=5)
        clear_btn.draw(screen, font)
        pygame.display.flip()

if __name__ == "__main__":
    main()