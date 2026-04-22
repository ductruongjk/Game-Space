"""
Ship Upgrade Screen - Customize ship stats before battle
"""
import pygame
import sys
import random
import math
from pygame.locals import *
from settings import *

class UpgradeScreen:
    """Upgrade ship stats with budget system - Futuristic UI"""
    
    def __init__(self, window, virtual_surf, player_num, is_ai=False, initial_budget=1000):
        self.window = window
        self.virtual_surf = virtual_surf
        self.player_num = player_num
        self.is_ai = is_ai
        
        self.font_large = pygame.font.Font(FONT_SPACE, 36)
        self.font_medium = pygame.font.Font(FONT_MAIN, 22)
        self.font_small = pygame.font.Font(FONT_MAIN, 16)
        
        # Upgrade categories
        self.categories = [
            {"name": "Ship Speed", "key": "speed", "value": 1.0, "min": 0.5, "max": 3.0, "cost": 50},
            {"name": "Maneuverability", "key": "maneuver", "value": 1.0, "min": 0.5, "max": 3.0, "cost": 50},
            {"name": "Rocket Max Speed", "key": "rocket", "value": 1.0, "min": 0.5, "max": 3.0, "cost": 50}
        ]
        
        self.superweapons = [SUPERWEAPON_PLASMA, SUPERWEAPON_LIGHTSPEED, SUPERWEAPON_GRAVITY]
        self.selected_super = 1
        self.selected = 0
        self.budget = initial_budget  # Dùng điểm tích lũy thay vì cố định 1000
        self.spent = 0
        self.section_count = len(self.categories) + 1
        self.frame = 0
        
        # Load assets
        self.border_img = self._load_img(ASSET_VIEN, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.plasma_preview = self._load_img(ASSET_PLASMA_BLAST, (64, 64))
        self.cursor_img = self._load_img(os.path.join(RESOURCES_DIR, 'cursor.png'), (32, 32))
        
        # Particles
        self.particles = []
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.3),
                'size': random.randint(1, 2)
            })
        
        # Colors
        self.player_colors = [CYAN, RED, GREEN, ORANGE]
        self.player_color = self.player_colors[player_num - 1]
    
    def _load_img(self, path, size=None):
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                return pygame.transform.smoothscale(img, size)
            return img
        except:
            return None
    
    def _remove_white_bg(self, img):
        if img is None:
            return None
        try:
            img_rgba = img.convert_alpha()
            pixels = pygame.surfarray.pixels3d(img_rgba)
            alpha = pygame.surfarray.pixels_alpha(img_rgba)
            white_mask = (pixels[:,:,0] > 240) & (pixels[:,:,1] > 240) & (pixels[:,:,2] > 240)
            alpha[white_mask] = 0
            del pixels, alpha
            return img_rgba
        except:
            return img
    
    def _draw_background(self):
        # Fill with dark space color
        self.virtual_surf.fill((5, 10, 25))
        
        # Grid with Perspective effect
        grid_color = (20, 60, 120)
        for i in range(20):
            t = i / 20.0
            y = SCREEN_HEIGHT - (t ** 0.7) * (SCREEN_HEIGHT * 0.7)
            pygame.draw.line(self.virtual_surf, grid_color, (0, int(y)), (SCREEN_WIDTH, int(y)))
        
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
        if self.border_img:
            border_clean = self._remove_white_bg(self.border_img)
            if border_clean:
                self.virtual_surf.blit(border_clean, (0, 0))

    def show(self):
        """Display upgrade screen and return stats dict"""
        if self.is_ai:
            return {
                "speed": round(random.uniform(1.0, 2.0), 1),
                "maneuver": round(random.uniform(1.0, 2.0), 1),
                "rocket": round(random.uniform(1.0, 2.0), 1),
                "super": random.choice(self.superweapons)
            }
        
        clock = pygame.time.Clock()
        pygame.key.set_repeat(0)
        
        while True:
            self.frame += 1
            
            # 1. Background
            self._draw_background()
            
            # 2. Screen Border
            self._draw_screen_border()
            
            # 3. Title with glow
            title_text = f"PLAYER {self.player_num} UPGRADES"
            title = self.font_large.render(title_text, True, self.player_color)
            title_x = SCREEN_WIDTH//2 - title.get_width()//2
            title_y = 35
            # Glow
            glow = pygame.Surface((title.get_width()+30, title.get_height()+15), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (*self.player_color[:3], 60), glow.get_rect())
            self.virtual_surf.blit(glow, (title_x-15, title_y-7))
            self.virtual_surf.blit(title, (title_x, title_y))
            
            # 4. Budget box
            budget_box = pygame.Surface((300, 45), pygame.SRCALPHA)
            pygame.draw.rect(budget_box, (20, 40, 70, 180), budget_box.get_rect(), border_radius=10)
            pygame.draw.rect(budget_box, (self.player_color[0], self.player_color[1], self.player_color[2], 150), budget_box.get_rect(), 2, border_radius=10)
            self.virtual_surf.blit(budget_box, (100, 90))
            budget_text = self.font_medium.render(f"Budget: ${self.budget}", True, WHITE)
            self.virtual_surf.blit(budget_text, (120, 100))
            
            # 5. Upgrade categories (Cards)
            for i, cat in enumerate(self.categories):
                y_pos = 160 + i * 55
                is_selected = i == self.selected
                
                # Card background
                card_w = 620
                card_h = 45
                card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                
                if is_selected:
                    pygame.draw.rect(card, (0, 150, 200, 100), card.get_rect(), border_radius=10)
                    pygame.draw.rect(card, (0, 220, 255, 200), card.get_rect(), 3, border_radius=10)
                    # Pulse glow
                    pulse = 1.0 + math.sin(self.frame * 0.1) * 0.1
                    pygame.draw.rect(card, (0, 200, 255, 80), (5, 5, card_w-10, card_h-10), border_radius=8)
                else:
                    pygame.draw.rect(card, (40, 60, 90, 120), card.get_rect(), border_radius=10)
                    pygame.draw.rect(card, (80, 120, 160, 150), card.get_rect(), 2, border_radius=10)
                
                self.virtual_surf.blit(card, (90, y_pos))
                
                # Cursor indicator
                if is_selected and self.cursor_img:
                    self.virtual_surf.blit(self.cursor_img, (55, y_pos + 5))

                # Name
                name_text = self.font_small.render(f"{cat['name']}:", True, WHITE)
                self.virtual_surf.blit(name_text, (110, y_pos + 12))

                # Value display
                val_text = self.font_small.render(f"{cat['value']:.1f}x", True, CYAN if is_selected else (180, 200, 220))
                self.virtual_surf.blit(val_text, (280, y_pos + 12))

                # Slider bar
                bar_x = 360
                bar_w = 180
                pygame.draw.rect(self.virtual_surf, (40, 40, 60), (bar_x, y_pos + 17, bar_w, 12), border_radius=6)
                progress = (cat["value"] - cat["min"]) / (cat["max"] - cat["min"])
                bar_color = (0, 200, 255) if is_selected else (100, 150, 180)
                pygame.draw.rect(self.virtual_surf, bar_color, (bar_x, y_pos + 17, int(bar_w * progress), 12), border_radius=6)
            
            # 6. Superweapon selection
            weapon_row_y = 340
            
            # Weapon card
            weapon_card = pygame.Surface((620, 110), pygame.SRCALPHA)
            if self.selected == len(self.categories):
                pygame.draw.rect(weapon_card, (0, 150, 200, 100), weapon_card.get_rect(), border_radius=10)
                pygame.draw.rect(weapon_card, (0, 220, 255, 200), weapon_card.get_rect(), 3, border_radius=10)
            else:
                pygame.draw.rect(weapon_card, (40, 60, 90, 120), weapon_card.get_rect(), border_radius=10)
                pygame.draw.rect(weapon_card, (80, 120, 160, 150), weapon_card.get_rect(), 2, border_radius=10)
            self.virtual_surf.blit(weapon_card, (90, weapon_row_y))
            
            # Title
            self.virtual_surf.blit(self.font_small.render("SELECT SUPERWEAPON:", True, (180, 220, 255)), (110, weapon_row_y + 10))

            # Draw weapons
            weapon_labels = ["Plasma Blast", "Light Speed", "Naval Mine"]
            for i, weapon in enumerate(self.superweapons):
                x_pos = 110 + i * 200
                y_pos = weapon_row_y + 40
                is_sel = i == self.selected_super
                
                # Weapon box
                w_box = pygame.Surface((180, 50), pygame.SRCALPHA)
                if is_sel:
                    pygame.draw.rect(w_box, (0, 200, 255, 150), w_box.get_rect(), border_radius=8)
                    pygame.draw.rect(w_box, (0, 255, 255, 255), w_box.get_rect(), 2, border_radius=8)
                else:
                    pygame.draw.rect(w_box, (60, 80, 100, 100), w_box.get_rect(), border_radius=8)
                self.virtual_surf.blit(w_box, (x_pos, y_pos))
                
                label = weapon_labels[i]
                color = CYAN if is_sel else (180, 200, 220)
                text = self.font_small.render(label, True, color)
                text_x = x_pos + 90 - text.get_width()//2
                self.virtual_surf.blit(text, (text_x, y_pos + 15))
            
            # Preview
            if self.plasma_preview and self.selected_super == 0:
                self.virtual_surf.blit(self.plasma_preview, (540, weapon_row_y + 30))
            
            # 7. Buttons
            mx, my = self._get_mouse_pos()
            
            # START GAME Button
            btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, 470, 240, 45)
            is_hover = btn_rect.collidepoint(mx, my)
            btn_surf = pygame.Surface((btn_rect.width, btn_rect.height), pygame.SRCALPHA)
            if is_hover:
                pygame.draw.rect(btn_surf, (0, 150, 200, 200), btn_surf.get_rect(), border_radius=8)
                pygame.draw.rect(btn_surf, (0, 220, 255, 255), btn_surf.get_rect(), 3, border_radius=8)
            else:
                pygame.draw.rect(btn_surf, (30, 80, 120, 180), btn_surf.get_rect(), border_radius=8)
                pygame.draw.rect(btn_surf, (100, 180, 220, 200), btn_surf.get_rect(), 2, border_radius=8)
            self.virtual_surf.blit(btn_surf, btn_rect)
            txt = self.font_medium.render("CONFIRM", True, WHITE if is_hover else (200, 230, 255))
            self.virtual_surf.blit(txt, txt.get_rect(center=btn_rect.center))
            
            # MENU Button
            menu_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 525, 200, 38)
            is_q_hover = menu_rect.collidepoint(mx, my)
            quit_surf = pygame.Surface((menu_rect.width, menu_rect.height), pygame.SRCALPHA)
            if is_q_hover:
                pygame.draw.rect(quit_surf, (180, 40, 40, 200), quit_surf.get_rect(), border_radius=8)
                pygame.draw.rect(quit_surf, (255, 100, 100, 255), quit_surf.get_rect(), 3, border_radius=8)
            else:
                pygame.draw.rect(quit_surf, (100, 30, 30, 180), quit_surf.get_rect(), border_radius=8)
                pygame.draw.rect(quit_surf, (180, 80, 80, 200), quit_surf.get_rect(), 2, border_radius=8)
            self.virtual_surf.blit(quit_surf, menu_rect)
            q_txt = self.font_medium.render("MAIN MENU", True, WHITE)
            self.virtual_surf.blit(q_txt, q_txt.get_rect(center=menu_rect.center))

            # Hint
            hint = self.font_small.render("UP/DOWN: Navigate | LEFT/RIGHT: Adjust | ENTER: Confirm | ESC: Cancel", True, (150, 180, 200))
            self.virtual_surf.blit(hint, (100, 580))
            
            self._update_display()
            
            # Event handling (single loop)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Check upgrade cards
                    for i in range(len(self.categories)):
                        card_rect = pygame.Rect(90, 160 + i * 55, 620, 45)
                        if card_rect.collidepoint(mx, my):
                            self.selected = i
                    # Check weapon selection
                    weapon_row_y = 340
                    for i in range(len(self.superweapons)):
                        w_rect = pygame.Rect(110 + i * 200, weapon_row_y + 40, 180, 50)
                        if w_rect.collidepoint(mx, my):
                            self.selected_super = i
                            self.selected = len(self.categories)
                    # Check buttons
                    if btn_rect.collidepoint(mx, my):
                        stats = {cat["key"]: cat["value"] for cat in self.categories}
                        stats["super"] = self.superweapons[self.selected_super]
                        return stats
                    if menu_rect.collidepoint(mx, my):
                        return None
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % self.section_count
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % self.section_count
                    elif event.key == K_LEFT:
                        if self.selected < len(self.categories):
                            self._downgrade_selected()
                        else:
                            self.selected_super = (self.selected_super - 1) % len(self.superweapons)
                    elif event.key == K_RIGHT:
                        if self.selected < len(self.categories):
                            self._upgrade_selected()
                        else:
                            self.selected_super = (self.selected_super + 1) % len(self.superweapons)
                    elif event.key == K_1:
                        self.selected_super = 0
                        self.selected = len(self.categories)
                    elif event.key == K_2:
                        self.selected_super = 1
                        self.selected = len(self.categories)
                    elif event.key == K_3:
                        self.selected_super = 2
                        self.selected = len(self.categories)
                    elif event.key == K_RETURN or event.key == K_SPACE:
                        stats = {cat["key"]: cat["value"] for cat in self.categories}
                        stats["super"] = self.superweapons[self.selected_super]
                        return stats
                    elif event.key == K_ESCAPE:
                        return None
            
            clock.tick(FPS)
    
    def _upgrade_selected(self):
        """Upgrade selected category"""
        cat = self.categories[self.selected]
        if self.budget >= cat["cost"] and cat["value"] < cat["max"]:
            cat["value"] = round(cat["value"] + 0.5, 1)
            self.budget -= cat["cost"]
            self.spent += cat["cost"]
    
    def _downgrade_selected(self):
        """Downgrade selected category"""
        cat = self.categories[self.selected]
        if cat["value"] > cat["min"]:
            cat["value"] = round(cat["value"] - 0.5, 1)
            self.budget += cat["cost"]
            self.spent -= cat["cost"]
    
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
