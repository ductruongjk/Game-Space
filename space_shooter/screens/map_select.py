"""
Map Selection Screen
"""
import pygame
import sys
from pygame.locals import *
from settings import *
from maps import DeepSpaceMap, GravityChaosMap, ReverseGravityMap

class MapSelect:
    """Map selection with preview"""

    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.font_large = pygame.font.Font(FONT_SPACE, 40)
        self.font_medium = pygame.font.Font(FONT_MAIN, 24)
        self.font_small = pygame.font.Font(FONT_MAIN, 14)

        self.maps = [
            {
                "name": "Deep Space Arena",
                "desc": "Pure combat - no obstacles. Perfect for beginners!",
                "feature": "Starfield background",
                "difficulty": "Easy",
                "color": GREEN,
                "class": DeepSpaceMap
            },
            {
                "name": "Gravity Chaos Zone",
                "desc": "Black hole pulls ships in! Asteroids orbit as shields.",
                "feature": "Central black hole gravity",
                "difficulty": "Hard",
                "color": RED,
                "class": GravityChaosMap
            },
            {
                "name": "Reverse Gravity Zone",
                "desc": "Gravity reverses every 15s! Watch for the warning!",
                "feature": "Reversing gravity",
                "difficulty": "Medium",
                "color": YELLOW,
                "class": ReverseGravityMap
            }
        ]
        self.selected = 0

    def show(self, mode_name="PLAYER vs ENVIRONMENT", p1_name="..........", p2_name=None):
        """Display map selection and return selected map class"""
        clock = pygame.time.Clock()
        pygame.key.set_repeat(0)  # Disable key repeat

        while True:
            self.virtual_surf.fill(BLACK)
            pygame.draw.rect(self.virtual_surf, (0, 150, 255), (20, 20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2, border_radius=10)

            title = self.font_large.render(mode_name, True, CYAN)
            self.virtual_surf.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

            p_text = self.font_medium.render(f"Player 1: {p1_name}", True, WHITE)
            self.virtual_surf.blit(p_text, (100, 120))
            if p2_name is not None:
                p2_text = self.font_medium.render(f"Player 2: {p2_name}", True, WHITE)
                self.virtual_surf.blit(p2_text, (100, 150))

            prompt = self.font_small.render("# Select Map... Show [E]keys...", True, WHITE)
            self.virtual_surf.blit(prompt, (100, 190))

            for i, map_data in enumerate(self.maps):
                y_pos = 230 + i * 50
                is_selected = i == self.selected

                circle_center = (120, y_pos + 12)
                pygame.draw.circle(self.virtual_surf, WHITE, circle_center, 12, 2)
                if is_selected:
                    pygame.draw.circle(self.virtual_surf, CYAN, circle_center, 8)

                if i == 0:
                    pygame.draw.rect(self.virtual_surf, WHITE, (108, y_pos, 24, 24), 2)
                    if is_selected:
                        pygame.draw.line(self.virtual_surf, CYAN, (112, y_pos + 12), (118, y_pos + 20), 3)
                        pygame.draw.line(self.virtual_surf, CYAN, (118, y_pos + 20), (128, y_pos + 6), 3)

                name_color = WHITE if is_selected else (180, 180, 180)
                name = self.font_medium.render(map_data["name"], True, name_color)
                self.virtual_surf.blit(name, (150, y_pos))

            btn_start = self.font_medium.render("START GAME", True, CYAN)
            self.start_rect = btn_start.get_rect(center=(SCREEN_WIDTH//2, 470))
            pygame.draw.rect(self.virtual_surf, (30, 60, 80), self.start_rect.inflate(100, 10), border_radius=5)
            pygame.draw.rect(self.virtual_surf, CYAN, self.start_rect.inflate(100, 10), 2, border_radius=5)
            self.virtual_surf.blit(btn_start, self.start_rect)

            btn_back = self.font_medium.render("BACK", True, RED)
            self.back_rect = btn_back.get_rect(center=(SCREEN_WIDTH//2, 530))
            pygame.draw.rect(self.virtual_surf, (80, 30, 30), self.back_rect.inflate(100, 10), border_radius=5)
            pygame.draw.rect(self.virtual_surf, RED, self.back_rect.inflate(100, 10), 2, border_radius=5)
            self.virtual_surf.blit(btn_back, self.back_rect)

            self._update_display()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        scale_x = SCREEN_WIDTH / self.window.get_width()
                        scale_y = SCREEN_HEIGHT / self.window.get_height()
                        virtual_mouse = (int(mouse_pos[0] * scale_x), int(mouse_pos[1] * scale_y))

                        if self.start_rect.collidepoint(virtual_mouse):
                            return self.maps[self.selected]["name"]
                        elif self.back_rect.collidepoint(virtual_mouse):
                            return "back"
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.maps)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.maps)
                    elif event.key in (K_RETURN, K_KP_ENTER):
                        return self.maps[self.selected]["name"]
                    elif event.key == K_ESCAPE:
                        return "back"

            clock.tick(FPS)

    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
