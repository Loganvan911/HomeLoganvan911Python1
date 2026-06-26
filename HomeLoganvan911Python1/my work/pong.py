import pygame
import sys
import math
import random

# ── Ініціалізація Pygame ───────────────────────────────────

pygame.init()

# ── Константи ──────────────────────────────────────────────

WIDTH, HEIGHT = 1200, 700
FPS = 60
PAD_W, PAD_H = 14, 100
PAD_SPEED = 6
WIN_SCORE = 5

# Кольори
BG_COLOR    = (15, 15, 35)
NET_COLOR   = (100, 100, 120)
P1_COLOR    = (0, 200, 255)    # Cyan
P2_COLOR    = (255, 100, 200)  # Magenta
ACCENT      = (100, 255, 150)  # Green
ACCENT2     = (255, 200, 100)  # Orange
GRAY        = (150, 150, 160)
WHITE       = (255, 255, 255)

# Складність
DIFFICULTIES = {
    "Легко": {"ball_speed": 5, "ai_speed": 3, "ai_error": 40},
    "Середньо": {"ball_speed": 7, "ai_speed": 5, "ai_error": 25},
    "Складно": {"ball_speed": 10, "ai_speed": 6.5, "ai_error": 15},
}

# Шрифти
FONT_BIG   = pygame.font.Font(None, 90)
FONT_MED   = pygame.font.Font(None, 50)
FONT_TINY  = pygame.font.Font(None, 20)

# ── Допоміжні функції ──────────────────────────────────────

def draw_glow(surf, color, rect, glow_rad):
    """Малює光圈навколо прямокутника"""
    glow_surf = pygame.Surface((rect.w + glow_rad*2, rect.h + glow_rad*2), pygame.SRCALPHA)
    for i in range(glow_rad, 0, -1):
        alpha = int(30 * (1 - i/glow_rad))
        pygame.draw.rect(glow_surf, (*color, alpha),
                         (glow_rad - i, glow_rad - i, rect.w + i*2, rect.h + i*2),
                         border_radius=3)
    surf.blit(glow_surf, (rect.x - glow_rad, rect.y - glow_rad))
    pygame.draw.rect(surf, color, rect, border_radius=3)

def render_outline(surf, text, font, color, x, y, outline_width=3):
    """Малює текст з чорним контуром"""
    main_text = font.render(text, True, color)
    outline_text = font.render(text, True, (0, 0, 0))
    
    for adj_x in range(-outline_width, outline_width + 1):
        for adj_y in range(-outline_width, outline_width + 1):
            if adj_x != 0 or adj_y != 0:
                surf.blit(outline_text, 
                         outline_text.get_rect(center=(x + adj_x, y + adj_y)))
    surf.blit(main_text, main_text.get_rect(center=(x, y)))

# ── Клас кнопки ─────────────────────────────────────────────

class Button:
    def __init__(self, text, x, y, w, h, color=ACCENT):
        self.text = text
        self.rect = pygame.Rect(x - w//2, y - h//2, w, h)
        self.color = color
        self.active = False

    def draw(self, surf):
        col = self.color if self.active else (70, 70, 90)
        draw_glow(surf, col, self.rect, 10)
        txt = FONT_MED.render(self.text, True, WHITE)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and 
                self.rect.collidepoint(event.pos))

# ── Клас м'яча ──────────────────────────────────────────────

class Ball:
    def __init__(self, speed):
        self.r = 8
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.base_speed = speed
        self.vx = speed
        self.vy = speed * 0.5
        self.color = WHITE

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        angle = random.choice([30, -30, 150, -150])
        rad = math.radians(angle)
        speed = self.base_speed
        self.vx = speed * math.cos(rad)
        self.vy = speed * math.sin(rad)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        # Віддзеркалення від стель/підлоги
        if self.y - self.r <= 0 or self.y + self.r >= HEIGHT:
            self.vy *= -1
            self.y = max(self.r, min(HEIGHT - self.r, self.y))

    def draw(self, surf):
        draw_glow(surf, self.color, 
                 pygame.Rect(self.x - self.r, self.y - self.r, self.r*2, self.r*2), 8)

    def collide_pad(self, pad_rect):
        return (self.x - self.r < pad_rect.right and
                self.x + self.r > pad_rect.left and
                self.y - self.r < pad_rect.bottom and
                self.y + self.r > pad_rect.top)


# ── Клас ракетки ───────────────────────────────────────────

class Paddle:
    def __init__(self, x, color):
        self.w = PAD_W
        self.h = PAD_H
        self.x = x
        self.y = HEIGHT // 2 - self.h // 2
        self.color = color
        self.score = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def clamp(self):
        self.y = max(0, min(HEIGHT - self.h, self.y))

    def draw(self, surf):
        draw_glow(surf, self.color, self.rect, 14)


# ── Основна гра ────────────────────────────────────────────

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🏓  Настільний Теніс")
        self.clock  = pygame.time.Clock()
        self.state  = "menu"         # menu | playing | pause | gameover
        self.diff_name = "Середньо"
        self._build_menu()
        self._particles = []

    # ── Меню ──

    def _build_menu(self):
        cx = WIDTH // 2
        self._play_btn = Button("▶  ГРАТИ",       cx, 290, 280, 58, ACCENT)
        self._diff_btns = {
            name: Button(name, cx - 240 + i*240, 390, 200, 48,
                         ACCENT if name=="Середньо" else GRAY)
            for i, name in enumerate(DIFFICULTIES)
        }
        self._quit_btn  = Button("✕  ВИЙТИ",      cx, 470, 220, 48, ACCENT2)

    def _draw_menu(self):
        self.screen.fill(BG_COLOR)
        self._draw_net()

        # Декоративні ракетки
        for x, col in [(40, P1_COLOR), (WIDTH-40-PAD_W, P2_COLOR)]:
            r = pygame.Rect(x, HEIGHT//2 - PAD_H//2, PAD_W, PAD_H)
            draw_glow(self.screen, col, r, 14)

        # Заголовок
        render_outline(self.screen, "НАСТІЛЬНИЙ ТЕНІС",
                       FONT_BIG, ACCENT, WIDTH//2, 110)
        render_outline(self.screen, "PING  PONG",
                       FONT_MED, ACCENT2, WIDTH//2, 180)

        # Підпис складності
        lbl = FONT_TINY.render("РІВЕНЬ СКЛАДНОСТІ", True, GRAY)
        self.screen.blit(lbl, lbl.get_rect(center=(WIDTH//2, 355)))

        for name, btn in self._diff_btns.items():
            btn.active = (name == self.diff_name)
            btn.draw(self.screen)

        self._play_btn.draw(self.screen)
        self._quit_btn.draw(self.screen)

        # Підказки
        tips = [
            "W / S  — гравець 1  (ліво)",
            "↑ / ↓  — гравець 2  (право)  або ШІ",
            f"Перемагає той, хто набере  {WIN_SCORE}  очок",
        ]
        for i, t in enumerate(tips):
            s = FONT_TINY.render(t, True, GRAY)
            self.screen.blit(s, s.get_rect(center=(WIDTH//2, 520 + i*20)))

    def _handle_menu(self, event):
        if self._play_btn.is_clicked(event):
            self._start_game()
        if self._quit_btn.is_clicked(event):
            pygame.quit(); sys.exit()
        for name, btn in self._diff_btns.items():
            if btn.is_clicked(event):
                self.diff_name = name

    # ── Запуск гри ──

    def _start_game(self):
        cfg = DIFFICULTIES[self.diff_name]
        self.ball       = Ball(cfg["ball_speed"])
        self.p1         = Paddle(30,           P1_COLOR)
        self.p2         = Paddle(WIDTH-30-PAD_W, P2_COLOR)
        self.ai_speed   = cfg["ai_speed"]
        self.ai_error   = cfg["ai_error"]
        self.state      = "playing"
        self._particles = []

    # ── Пауза ──

    def _build_pause(self):
        cx = WIDTH//2
        self._resume_btn  = Button("▶  ПРОДОВЖИТИ", cx, 270, 280, 54)
        self._menu_btn_p  = Button("⌂  МЕНЮ",        cx, 345, 220, 48, ACCENT2)

    def _draw_pause(self):
        # Напівпрозорий оверлей
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        render_outline(self.screen, "ПАУЗА", FONT_BIG, ACCENT, WIDTH//2, 190)
        self._resume_btn.draw(self.screen)
        self._menu_btn_p.draw(self.screen)

    def _handle_pause(self, event):
        if self._resume_btn.is_clicked(event):
            self.state = "playing"
        if self._menu_btn_p.is_clicked(event):
            self.state = "menu"

    # ── Гра ──

    def _update_game(self, keys):
        # Гравець 1 (W/S)
        if keys[pygame.K_w]: self.p1.y -= PAD_SPEED
        if keys[pygame.K_s]: self.p1.y += PAD_SPEED
        self.p1.clamp()

        # Гравець 2 / ШІ (стрілки)
        if keys[pygame.K_UP]:   self.p2.y -= PAD_SPEED
        elif keys[pygame.K_DOWN]: self.p2.y += PAD_SPEED
        else:
            # ШІ
            target = self.ball.y + random.uniform(-self.ai_error, self.ai_error)
            cy2 = self.p2.y + PAD_H // 2
            if cy2 < target - 4:
                self.p2.y += self.ai_speed
            elif cy2 > target + 4:
                self.p2.y -= self.ai_speed
        self.p2.clamp()

        # М'яч
        self.ball.update()

        # Зіткнення з ракетками
        for pad in [self.p1, self.p2]:
            if self.ball.collide_pad(pad.rect):
                # Відскок
                rel = (self.ball.y - (pad.y + PAD_H/2)) / (PAD_H/2)
                angle = rel * 65
                speed = math.hypot(self.ball.vx, self.ball.vy)
                speed = min(speed * 1.04, 18)
                rad   = math.radians(angle)
                dirx  = 1 if self.ball.vx < 0 else -1
                self.ball.vx = dirx * speed * math.cos(rad)
                self.ball.vy = speed * math.sin(rad)
                # відштовхнути від ракетки
                if dirx == 1:
                    self.ball.x = pad.rect.right + self.ball.r + 1
                else:
                    self.ball.x = pad.rect.left  - self.ball.r - 1
                self._spawn_particles(int(self.ball.x), int(self.ball.y), pad.color)

        # Очко
        if self.ball.x - self.ball.r <= 0:
            self.p2.score += 1
            self._spawn_particles(0, HEIGHT//2, P2_COLOR, 25)
            self.ball.reset()
        elif self.ball.x + self.ball.r >= WIDTH:
            self.p1.score += 1
            self._spawn_particles(WIDTH, HEIGHT//2, P1_COLOR, 25)
            self.ball.reset()

        # Перемога
        if self.p1.score >= WIN_SCORE or self.p2.score >= WIN_SCORE:
            self.state = "gameover"
            self._winner = 1 if self.p1.score >= WIN_SCORE else 2
            self._build_gameover()

        # Частинки
        self._update_particles()

    def _draw_game(self):
        self.screen.fill(BG_COLOR)
        self._draw_net()
        self._draw_particles()
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        self.ball.draw(self.screen)
        self._draw_scores()
        # Підказка паузи
        hint = FONT_TINY.render("ESC — пауза", True, GRAY)
        self.screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 24))

    def _draw_scores(self):
        s1 = FONT_BIG.render(str(self.p1.score), True, P1_COLOR)
        s2 = FONT_BIG.render(str(self.p2.score), True, P2_COLOR)
        self.screen.blit(s1, (WIDTH//4  - s1.get_width()//2, 12))
        self.screen.blit(s2, (3*WIDTH//4 - s2.get_width()//2, 12))

        lbl_diff = FONT_TINY.render(self.diff_name, True, GRAY)
        self.screen.blit(lbl_diff,
                         lbl_diff.get_rect(center=(WIDTH//2, HEIGHT - 44)))

    def _draw_net(self):
        seg = 18
        for y in range(0, HEIGHT, seg*2):
            pygame.draw.rect(self.screen, NET_COLOR,
                             (WIDTH//2 - 2, y, 4, seg))

    # ── Кінець гри ──

    def _build_gameover(self):
        cx = WIDTH//2
        self._replay_btn  = Button("↺  ЩЕ РАЗ",  cx, 320, 240, 54)
        self._menu_btn_g  = Button("⌂  МЕНЮ",     cx, 395, 220, 48, ACCENT2)

    def _draw_gameover(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        w_col  = P1_COLOR if self._winner == 1 else P2_COLOR
        w_text = f"ГРАВЕЦЬ  {self._winner}  ПЕРЕМІГ!"
        render_outline(self.screen, w_text, FONT_MED, w_col, WIDTH//2, 210)

        s1 = FONT_MED.render(f"{self.p1.score}  :  {self.p2.score}", True, WHITE)
        self.screen.blit(s1, s1.get_rect(center=(WIDTH//2, 268)))

        self._replay_btn.draw(self.screen)
        self._menu_btn_g.draw(self.screen)

    def _handle_gameover(self, event):
        if self._replay_btn.is_clicked(event):
            self._start_game()
        if self._menu_btn_g.is_clicked(event):
            self.state = "menu"

    # ── Частинки ──

    def _spawn_particles(self, x, y, color, n=14):
        for _ in range(n):
            angle = random.uniform(0, math.pi*2)
            speed = random.uniform(2, 7)
            self._particles.append({
                "x": x, "y": y,
                "vx": math.cos(angle)*speed,
                "vy": math.sin(angle)*speed,
                "life": 1.0,
                "color": color,
                "r": random.randint(3,6)
            })

    def _update_particles(self):
        for p in self._particles:
            p["x"]    += p["vx"]
            p["y"]    += p["vy"]
            p["vy"]   += 0.18
            p["life"] -= 0.035
        self._particles = [p for p in self._particles if p["life"] > 0]

    def _draw_particles(self):
        for p in self._particles:
            alpha = int(255 * p["life"])
            s = pygame.Surface((p["r"]*2+2, p["r"]*2+2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p["color"], alpha),
                               (p["r"]+1, p["r"]+1), p["r"])
            self.screen.blit(s, (int(p["x"]) - p["r"], int(p["y"]) - p["r"]))

    # ── Головний цикл ──

    def run(self):
        self._build_menu()
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if self.state == "menu":
                    self._handle_menu(event)

                elif self.state == "playing":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "pause"
                        self._build_pause()

                elif self.state == "pause":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = "playing"
                    self._handle_pause(event)

                elif self.state == "gameover":
                    self._handle_gameover(event)

            # Оновлення
            if self.state == "playing":
                self._update_game(keys)

            # Малювання
            if self.state == "menu":
                self._draw_menu()
            elif self.state == "playing":
                self._draw_game()
            elif self.state == "pause":
                self._draw_game()
                self._draw_pause()
            elif self.state == "gameover":
                self._draw_game()
                self._draw_gameover()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    PongGame().run()