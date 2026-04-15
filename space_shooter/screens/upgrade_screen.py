"""
Ship Upgrade Screen - Customize ship stats before battle
"""
import pygame
import sys
import random
from pygame.locals import *
from settings import *

class UpgradeScreen:
    """Upgrade ship stats with budget system"""
    
    def __init__(self, window, virtual_surf, player_num, is_ai=False):
        self.window = window
        self.virtual_surf = virtual_surf
        self.player_num = player_num
        self.is_ai = is_ai
        
        self.font_large = pygame.font.Font(FONT_SPACE, 36)
        self.font_medium = pygame.font.Font(FONT_MAIN, 22)
        self.font_small = pygame.font.Font(FONT_MAIN, 14)
        
        # Upgrade categories
        self.categories = [
            {"name": "Ship Speed", "key": "speed", "value": 1.0, "min": 0.5, "max": 3.0, "cost": 50},
            {"name": "Maneuverability", "key": "maneuver", "value": 1.0, "min": 0.5, "max": 3.0, "cost": 50},
            {"name": "Rocket Max Speed", "key": "rocket", "value": 1.0, "min": 0.5, "max": 3.0, "cost": 50}
        ]
        
        self.superweapons = [SUPERWEAPON_PLASMA, SUPERWEAPON_LIGHTSPEED, SUPERWEAPON_GRAVITY]
        self.selected_super = 1  # Default to Light Speed as per image
        self.selected = 0
        self.budget = 1000
        self.spent = 0
        
        # Colors
        self.player_colors = [CYAN, RED, GREEN, ORANGE] # CYAN for Player 1 as per image
        self.player_color = self.player_colors[player_num - 1]
    
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
        
        while True:
            self.virtual_surf.fill(BLACK)
            # Simple futuristic border
            pygame.draw.rect(self.virtual_surf, (0, 150, 255), (20, 20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2, border_radius=10)
            
            # Title
            title_text = f"Which mode would you like to play?"
            title = self.font_medium.render(title_text, True, WHITE)
            self.virtual_surf.blit(title, (100, 50))
            
            subtitle = self.font_medium.render(f"Player {self.player_num}: Select Your Upgrades", True, WHITE)
            self.virtual_surf.blit(subtitle, (100, 85))
            
            # Money display
            budget_text = self.font_medium.render(f"Money left for Upgrades: {self.budget} $", True, WHITE)
            self.virtual_surf.blit(budget_text, (100, 130))
            
            # Draw upgrade categories (Sliders)
            for i, cat in enumerate(self.categories):
                y_pos = 180 + i * 40
                is_selected = i == self.selected
                
                # Name
                name_text = self.font_small.render(f"{cat['name']}:", True, WHITE)
                self.virtual_surf.blit(name_text, (100, y_pos))
                
                # Slider bar
                bar_x = 350
                bar_w = 200
                pygame.draw.rect(self.virtual_surf, (60, 60, 60), (bar_x, y_pos + 5, bar_w, 10), border_radius=5)
                
                # Progress
                progress = (cat["value"] - cat["min"]) / (cat["max"] - cat["min"])
                pygame.draw.rect(self.virtual_surf, (0, 200, 255), (bar_x, y_pos + 5, int(bar_w * progress), 10), border_radius=5)
                
                # X marker
                self.virtual_surf.blit(self.font_small.render("X", True, WHITE), (bar_x + bar_w + 10, y_pos))
            
            # Superweapon selection
            y_super = 320
            self.virtual_surf.blit(self.font_small.render("Choose your Superweapon:", True, WHITE), (100, y_super))
            
            # Draw weapons in a row with arrows for the selected one
            for i, weapon in enumerate(self.superweapons):
                x_pos = 100 + i * 180
                is_sel = i == self.selected_super
                color = (0, 255, 255) if is_sel else (150, 150, 150)
                
                text = self.font_small.render(weapon, True, color)
                if is_sel:
                    self.virtual_surf.blit(self.font_small.render("<", True, WHITE), (x_pos - 15, y_super + 30))
                    self.virtual_surf.blit(text, (x_pos, y_super + 30))
                    self.virtual_surf.blit(self.font_small.render(">", True, WHITE), (x_pos + text.get_width() + 5, y_super + 30))
                else:
                    self.virtual_surf.blit(text, (x_pos, y_super + 30))
            
            # Buttons
            btn_start = self.font_medium.render("START GAME", True, CYAN)
            btn_rect = btn_start.get_rect(center=(SCREEN_WIDTH//2, 450))
            pygame.draw.rect(self.virtual_surf, (30, 60, 80), btn_rect.inflate(100, 10), border_radius=5)
            pygame.draw.rect(self.virtual_surf, CYAN, btn_rect.inflate(100, 10), 2, border_radius=5)
            self.virtual_surf.blit(btn_start, btn_rect)
            
            btn_menu = self.font_medium.render("MAIN MENU", True, RED)
            menu_rect = btn_menu.get_rect(center=(SCREEN_WIDTH//2, 510))
            pygame.draw.rect(self.virtual_surf, (80, 30, 30), menu_rect.inflate(100, 10), border_radius=5)
            pygame.draw.rect(self.virtual_surf, RED, menu_rect.inflate(100, 10), 2, border_radius=5)
            self.virtual_surf.blit(btn_menu, menu_rect)
            
            self._update_display()
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP: self.selected = (self.selected - 1) % len(self.categories)
                    if event.key == K_DOWN: self.selected = (self.selected + 1) % len(self.categories)
                    if event.key == K_LEFT and self.selected == 0: self._downgrade_selected()
                    if event.key == K_RIGHT and self.selected == 0: self._upgrade_selected()
                    # For rocket and maneuver
                    if event.key == K_LEFT and self.selected > 0: self._downgrade_selected()
                    if event.key == K_RIGHT and self.selected > 0: self._upgrade_selected()
                    
                    # Superweapon toggle
                    if event.key == K_1: self.selected_super = 0
                    if event.key == K_2: self.selected_super = 1
                    if event.key == K_3: self.selected_super = 2
                    
                    if event.key == K_RETURN:
                        stats = {cat["key"]: cat["value"] for cat in self.categories}
                        stats["super"] = self.superweapons[self.selected_super]
                        return stats
                    if event.key == K_ESCAPE: return None
            
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
    
    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
