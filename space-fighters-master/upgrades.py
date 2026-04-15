"""
Upgrade screen - Spend money on ship upgrades
"""
import pygame
import sys
import random
from pygame.locals import *
from settings import *

class UpgradeScreen:
    """Upgrade ship stats with budget system"""
    
    def __init__(self, window, virtual_surf, player_num, stats, money, is_ai=False):
        self.window = window
        self.virtual_surf = virtual_surf
        self.player_num = player_num
        self.is_ai = is_ai
        
        # Stats: [speed, maneuver, rocket_speed, money, superweapon]
        self.stats = list(stats)  # Copy
        if len(self.stats) < 5:
            self.stats = [1, 1, 1, money, 1]
        self.money = self.stats[3]
        self.starting_money = self.money
        
        # Upgrade categories
        self.categories = [
            {"name": "Ship Speed", "index": 0, "level": int(self.stats[0]), "cost": UPGRADE_COST},
            {"name": "Maneuverability", "index": 1, "level": int(self.stats[1]), "cost": UPGRADE_COST},
            {"name": "Rocket Max Speed", "index": 2, "level": int(self.stats[2]), "cost": UPGRADE_COST}
        ]
        
        # Superweapon selection
        self.superweapons = ["Light Speed", "Spacemine", "Plasma Blast"]
        self.selected_super = int(self.stats[4]) - 1 if len(self.stats) > 4 else 0
        self.selected_super = max(0, min(2, self.selected_super))
        
        self.selected = 0  # Selected upgrade category
        
    def show(self):
        """Display upgrade screen and return new stats"""
        if self.is_ai:
            # AI auto-assigns stats
            return [
                random.randint(2, 4),  # Speed
                random.randint(2, 4),  # Maneuver
                random.randint(2, 4),  # Rocket
                self.money,
                random.randint(1, 3)   # Superweapon
            ]
            
        clock = pygame.time.Clock()
        
        while True:
            self.virtual_surf.fill(BLACK)
            
            # Border
            pygame.draw.rect(self.virtual_surf, CYAN, (20, 20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2, border_radius=10)
            
            # Title
            title = FONT_TITLE.render(f"PLAYER {self.player_num} UPGRADES", True, CYAN if self.player_num == 1 else RED)
            self.virtual_surf.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
            
            # Money display
            money_text = FONT_MED.render(f"Money: ${self.money}", True, GOLD)
            self.virtual_surf.blit(money_text, (100, 120))
            
            # Draw upgrade categories
            for i, cat in enumerate(self.categories):
                y_pos = 180 + i * 60
                is_selected = i == self.selected
                
                # Name
                color = CYAN if is_selected else WHITE
                name_text = FONT_MED.render(f"{cat['name']}:", True, color)
                self.virtual_surf.blit(name_text, (100, y_pos))
                
                # Level bars
                bar_x = 350
                for level in range(MAX_UPGRADE_LEVEL):
                    bar_color = GREEN if level < cat['level'] else DARK_GRAY
                    pygame.draw.rect(self.virtual_surf, bar_color, 
                                   (bar_x + level * 35, y_pos + 5, 30, 20), border_radius=3)
                    
                # Cost
                if cat['level'] < MAX_UPGRADE_LEVEL:
                    cost_text = FONT_SMALL.render(f"${cat['cost']}", True, YELLOW)
                    self.virtual_surf.blit(cost_text, (bar_x + 200, y_pos + 5))
                else:
                    max_text = FONT_SMALL.render("MAX", True, GREEN)
                    self.virtual_surf.blit(max_text, (bar_x + 200, y_pos + 5))
                    
            # Superweapon selection
            y_super = 400
            sw_text = FONT_MED.render("Superweapon:", True, WHITE)
            self.virtual_surf.blit(sw_text, (100, y_super))
            
            for i, weapon in enumerate(self.superweapons):
                x_pos = 300 + i * 150
                is_sel = i == self.selected_super
                color = CYAN if is_sel else GRAY
                pygame.draw.rect(self.virtual_surf, color, 
                               (x_pos - 5, y_super - 5, 130, 30), border_radius=3)
                w_text = FONT_SMALL.render(weapon, True, WHITE)
                self.virtual_surf.blit(w_text, (x_pos, y_super))
                
            # Buttons
            start_btn = FONT_MED.render("START GAME", True, GREEN)
            btn_rect = start_btn.get_rect(center=(SCREEN_WIDTH//2, 500))
            pygame.draw.rect(self.virtual_surf, (0, 100, 0), btn_rect.inflate(40, 20), border_radius=5)
            pygame.draw.rect(self.virtual_surf, GREEN, btn_rect.inflate(40, 20), 2, border_radius=5)
            self.virtual_surf.blit(start_btn, btn_rect)
            
            # Controls hint
            hint = FONT_TINY.render("LEFT/RIGHT: Change | UP/DOWN: Select | ENTER: Confirm", True, GRAY)
            self.virtual_surf.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 50))
            
            self._update_display()
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.categories)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.categories)
                    elif event.key == K_LEFT:
                        if self.selected < len(self.categories):
                            self._downgrade(self.selected)
                        else:
                            self.selected_super = (self.selected_super - 1) % len(self.superweapons)
                    elif event.key == K_RIGHT:
                        if self.selected < len(self.categories):
                            self._upgrade(self.selected)
                        else:
                            self.selected_super = (self.selected_super + 1) % len(self.superweapons)
                    elif event.key == K_1:
                        self.selected_super = 0
                    elif event.key == K_2:
                        self.selected_super = 1
                    elif event.key == K_3:
                        self.selected_super = 2
                    elif event.key == K_RETURN:
                        # Return updated stats
                        return [
                            self.categories[0]['level'],  # Speed
                            self.categories[1]['level'],  # Maneuver
                            self.categories[2]['level'],  # Rocket
                            self.money,                    # Money left
                            self.selected_super + 1        # Superweapon
                        ]
                    elif event.key == K_ESCAPE:
                        return None
                        
            clock.tick(FPS)
            
    def _upgrade(self, index):
        """Upgrade a stat if enough money"""
        cat = self.categories[index]
        if self.money >= cat['cost'] and cat['level'] < MAX_UPGRADE_LEVEL:
            cat['level'] += 1
            self.money -= cat['cost']
            
    def _downgrade(self, index):
        """Downgrade a stat and refund money"""
        cat = self.categories[index]
        if cat['level'] > 1:
            cat['level'] -= 1
            self.money += cat['cost']
            
    def _update_display(self):
        """Scale and update display"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
