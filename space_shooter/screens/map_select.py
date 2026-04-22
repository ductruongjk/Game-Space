"""
Map Selection Screen
"""
import pygame
import sys
import random
import math
from pygame.locals import *
from settings import *
from maps import DeepSpaceMap, GravityChaosMap, ReverseGravityMap

class MapSelect:
    """Map selection with preview - Futuristic UI Style"""

    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.font_large = pygame.font.Font(FONT_SPACE, 40)
        self.font_medium = pygame.font.Font(FONT_MAIN, 24)
        self.font_small = pygame.font.Font(FONT_MAIN, 16)
        
        # Load assets
        self.border_img = self._load_img(ASSET_VIEN, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Particles
        self.particles = []
        for _ in range(40):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.4),
                'size': random.randint(1, 3)
            })
        self.frame = 0
        
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

    def _load_img(self, path, size=None):
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                return pygame.transform.smoothscale(img, size)
            return img
        except:
            return None

    def _draw_background(self):
        # Fill with dark space color
        self.virtual_surf.fill((5, 10, 25))
        
        # Grid with Perspective effect
        grid_color = (20, 60, 120)
        
        # Horizontal lines with perspective
        for i in range(20):
            t = i / 20.0
            y = SCREEN_HEIGHT - (t ** 0.7) * (SCREEN_HEIGHT * 0.7)
            pygame.draw.line(self.virtual_surf, grid_color, (0, int(y)), (SCREEN_WIDTH, int(y)))
        
        # Vertical lines converging to center
        vanishing_y = -100
        vanishing_x = SCREEN_WIDTH // 2
        for i in range(-10, 30, 2):
            bottom_x = (i / 20) * SCREEN_WIDTH * 1.5 + SCREEN_WIDTH // 2
            pygame.draw.line(self.virtual_surf, grid_color, 
                           (int(bottom_x), SCREEN_HEIGHT), 
                           (vanishing_x, vanishing_y))
        
        # Particles
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > SCREEN_HEIGHT: 
                p['y'] = 0
                p['x'] = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(self.virtual_surf, (200, 230, 255), (int(p['x']), int(p['y'])), p['size'])

    def _draw_screen_border(self):
        """Draw vien.png as border around entire screen"""
        if self.border_img:
            border_clean = self._remove_white_bg(self.border_img)
            if border_clean:
                self.virtual_surf.blit(border_clean, (0, 0))

    def _remove_white_bg(self, img):
        """Convert white background to transparent"""
        if img is None:
            return None
        img_rgba = img.convert_alpha()
        try:
            pixels = pygame.surfarray.pixels3d(img_rgba)
            alpha = pygame.surfarray.pixels_alpha(img_rgba)
            white_mask = (pixels[:,:,0] > 240) & (pixels[:,:,1] > 240) & (pixels[:,:,2] > 240)
            alpha[white_mask] = 0
            del pixels, alpha
        except:
            pass
        return img_rgba

    def show(self, mode_name="PLAYER vs ENVIRONMENT", p1_name="Player 1", p2_name="Player 2"):
        """Display map selection and return selected map class"""
        clock = pygame.time.Clock()
        pygame.key.set_repeat(0)

        while True:
            self.frame += 1
            
            # 1. Background
            self._draw_background()
            
            # 2. Screen Border
            self._draw_screen_border()

            # 3. Title with glow
            title = self.font_large.render(mode_name, True, CYAN)
            title_x = SCREEN_WIDTH//2 - title.get_width()//2
            title_y = 40
            # Glow effect
            glow = pygame.Surface((title.get_width()+20, title.get_height()+10), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (0, 100, 200, 80), glow.get_rect())
            self.virtual_surf.blit(glow, (title_x-10, title_y-5))
            self.virtual_surf.blit(title, (title_x, title_y))

            # 4. Player info box
            p_box = pygame.Surface((350, 80), pygame.SRCALPHA)
            pygame.draw.rect(p_box, (20, 40, 70, 180), p_box.get_rect(), border_radius=10)
            pygame.draw.rect(p_box, (0, 150, 200, 100), p_box.get_rect(), 2, border_radius=10)
            self.virtual_surf.blit(p_box, (100, 100))
            
            p_text = self.font_medium.render(f"Player 1: {p1_name}", True, WHITE)
            self.virtual_surf.blit(p_text, (120, 115))
            if p2_name:
                p2_text = self.font_medium.render(f"Player 2: {p2_name}", True, WHITE)
                self.virtual_surf.blit(p2_text, (120, 145))

            # 5. Map selection area
            prompt = self.font_small.render("# Select Map...", True, (180, 220, 255))
            self.virtual_surf.blit(prompt, (100, 200))

            # Draw map cards
            for i, map_data in enumerate(self.maps):
                card_y = 240 + i * 85
                is_selected = i == self.selected
                self._draw_map_card(100, card_y, map_data, is_selected, i)

            # 6. Buttons
            self._draw_buttons()

            self._update_display()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = self._get_mouse_pos()
                        # Check map cards
                        for i in range(len(self.maps)):
                            card_rect = pygame.Rect(100, 240 + i * 85, 600, 70)
                            if card_rect.collidepoint(mx, my):
                                self.selected = i
                        # Check buttons
                        if self.start_rect.collidepoint(mx, my):
                            return self.maps[self.selected]["name"]
                        elif self.back_rect.collidepoint(mx, my):
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
    
    def _draw_map_card(self, x, y, map_data, is_selected, index):
        """Draw a futuristic map selection card"""
        card_width = 600
        card_height = 70
        
        # Card background
        card_surf = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        
        if is_selected:
            # Glowing cyan border when selected
            pygame.draw.rect(card_surf, (0, 150, 200, 100), card_surf.get_rect(), border_radius=10)
            pygame.draw.rect(card_surf, (0, 220, 255, 200), card_surf.get_rect(), 3, border_radius=10)
            # Inner glow
            pygame.draw.rect(card_surf, (0, 100, 150, 60), (5, 5, card_width-10, card_height-10), border_radius=8)
        else:
            # Subtle border
            pygame.draw.rect(card_surf, (40, 60, 90, 120), card_surf.get_rect(), border_radius=10)
            pygame.draw.rect(card_surf, (80, 120, 160, 150), card_surf.get_rect(), 2, border_radius=10)
        
        self.virtual_surf.blit(card_surf, (x, y))
        
        # Radio button circle
        circle_x = x + 35
        circle_y = y + 35
        pygame.draw.circle(self.virtual_surf, WHITE, (circle_x, circle_y), 14, 2)
        if is_selected:
            pygame.draw.circle(self.virtual_surf, CYAN, (circle_x, circle_y), 10)
            # Pulse effect
            pulse = 1.0 + math.sin(self.frame * 0.1) * 0.2
            pygame.draw.circle(self.virtual_surf, (0, 200, 255, 100), (circle_x, circle_y), int(18 * pulse), 2)
        
        # Map name
        name_color = CYAN if is_selected else WHITE
        name = self.font_medium.render(map_data["name"], True, name_color)
        self.virtual_surf.blit(name, (x + 70, y + 15))
        
        # Difficulty indicator
        diff_color = map_data["color"]
        diff_text = self.font_small.render(f"[{map_data['difficulty']}]", True, diff_color)
        self.virtual_surf.blit(diff_text, (x + 70, y + 45))
        
        # Feature text on right
        feat_text = self.font_small.render(map_data["feature"], True, (180, 200, 220))
        self.virtual_surf.blit(feat_text, (x + 400, y + 25))
    
    def _draw_buttons(self):
        mx, my = self._get_mouse_pos()
        
        # START GAME Button
        self.start_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, 510, 240, 50)
        is_hover = self.start_rect.collidepoint(mx, my)
        
        btn_surf = pygame.Surface((self.start_rect.width, self.start_rect.height), pygame.SRCALPHA)
        if is_hover:
            pygame.draw.rect(btn_surf, (0, 150, 200, 200), btn_surf.get_rect(), border_radius=8)
            pygame.draw.rect(btn_surf, (0, 220, 255, 255), btn_surf.get_rect(), 3, border_radius=8)
        else:
            pygame.draw.rect(btn_surf, (30, 80, 120, 180), btn_surf.get_rect(), border_radius=8)
            pygame.draw.rect(btn_surf, (100, 180, 220, 200), btn_surf.get_rect(), 2, border_radius=8)
        
        self.virtual_surf.blit(btn_surf, self.start_rect)
        txt = self.font_medium.render("START GAME", True, WHITE if is_hover else (200, 230, 255))
        self.virtual_surf.blit(txt, txt.get_rect(center=self.start_rect.center))

        # BACK Button
        self.back_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 570, 200, 40)
        is_q_hover = self.back_rect.collidepoint(mx, my)
        
        quit_surf = pygame.Surface((self.back_rect.width, self.back_rect.height), pygame.SRCALPHA)
        if is_q_hover:
            pygame.draw.rect(quit_surf, (180, 40, 40, 200), quit_surf.get_rect(), border_radius=8)
            pygame.draw.rect(quit_surf, (255, 100, 100, 255), quit_surf.get_rect(), 3, border_radius=8)
        else:
            pygame.draw.rect(quit_surf, (100, 30, 30, 180), quit_surf.get_rect(), border_radius=8)
            pygame.draw.rect(quit_surf, (180, 80, 80, 200), quit_surf.get_rect(), 2, border_radius=8)
        
        self.virtual_surf.blit(quit_surf, self.back_rect)
        q_txt = self.font_medium.render("BACK", True, WHITE)
        self.virtual_surf.blit(q_txt, q_txt.get_rect(center=self.back_rect.center))
    
    def _get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        win_w, win_h = self.window.get_size()
        return mx * SCREEN_WIDTH / win_w, my * SCREEN_HEIGHT / win_h

    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
