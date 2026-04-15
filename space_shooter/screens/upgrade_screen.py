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
        self.section_count = len(self.categories) + 1
        self.plasma_preview = None
        self.cursor_img = None
        try:
            self.plasma_preview = pygame.image.load(ASSET_PLASMA_BLAST).convert_alpha()
            self.plasma_preview = pygame.transform.smoothscale(self.plasma_preview, (64, 64))
        except:
            self.plasma_preview = None
        try:
            self.cursor_img = pygame.image.load(os.path.join(RESOURCES_DIR, 'cursor.png')).convert_alpha()
            self.cursor_img = pygame.transform.smoothscale(self.cursor_img, (32, 32))
        except:
            self.cursor_img = None
        
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
        pygame.key.set_repeat(0)  # Disable key repeat
        
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
                
                # Highlight selected category row
                if is_selected:
                    pygame.draw.rect(self.virtual_surf, (20, 80, 120), (90, y_pos - 5, 520, 36), border_radius=8)
                    # Draw cursor indicator
                    if self.cursor_img:
                        self.virtual_surf.blit(self.cursor_img, (55, y_pos - 5))

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
            
            # Superweapon selection row highlight
            weapon_row_y = 340
            self.virtual_surf.blit(self.font_small.render("Choose your Superweapon:", True, WHITE), (100, weapon_row_y - 30))
            if self.selected == len(self.categories):
                pygame.draw.rect(self.virtual_surf, (20, 80, 120), (90, weapon_row_y - 10, 620, 120), border_radius=8)

            # Draw weapons in a row with arrows for the selected one
            weapon_labels = [
                "Plasma Blast (Chùm tia plasma)",
                "Light Speed (Tốc độ ánh sáng)",
                "Naval Mine (Mìn biển)"
            ]
            for i, weapon in enumerate(self.superweapons):
                x_pos = 100 + i * 220
                is_sel = i == self.selected_super
                color = (0, 255, 255) if is_sel else (150, 150, 150)
                
                label = weapon_labels[i] if i < len(weapon_labels) else weapon
                text = self.font_small.render(label, True, color)
                if is_sel:
                    self.virtual_surf.blit(self.font_small.render("<", True, WHITE), (x_pos - 15, weapon_row_y + 20))
                    self.virtual_surf.blit(text, (x_pos, weapon_row_y + 20))
                    self.virtual_surf.blit(self.font_small.render(">", True, WHITE), (x_pos + text.get_width() + 5, weapon_row_y + 20))
                else:
                    self.virtual_surf.blit(text, (x_pos, weapon_row_y + 20))
            
            # Weapon details and preview
            selected_label = weapon_labels[self.selected_super]
            if self.selected_super == 0:
                details = [
                    "+ Plasma Blast (Chùm tia plasma)",
                    "  Hiệu ứng: Bắn ra một viên đạn lớn, xuyên qua mọi vật cản (kể cả thiên thạch), gây sát thương",
                    "  Thời gian hồi: 5 giây",
                    "  Sử dụng: Ảnh Muzzle Mega Ion"
                ]
            elif self.selected_super == 1:
                details = [
                    "+ Light Speed (Tốc độ ánh sáng)",
                    "  Hiệu ứng: Tăng tốc độ di chuyển",
                    "  Thời gian hồi: 5 giây"
                ]
            else:
                details = [
                    "+ Naval Mine (Mìn biển)",
                    "  Hiệu ứng: 3 mìn bay ngẫu nhiên từ 4 góc (như thiên thạch)",
                    "  Màu sắc: Cùng màu người chơi đã chọn",
                    "  Người chơi chọn: Không bị ảnh hưởng, mìn xuyên qua",
                    "  Đối thủ khác màu: Bị trúng, mất điểm",
                    "  Sử dụng: navalmine1.webp (Ship1) / navalmine2.jpg (Ship2)"
                ]

            for idx, line in enumerate(details):
                color = CYAN if idx == 0 else (200, 200, 200)
                self.virtual_surf.blit(self.font_small.render(line, True, color), (100, weapon_row_y + 70 + idx * 22))

            if self.plasma_preview and self.selected_super == 0:
                self.virtual_surf.blit(self.plasma_preview, (620, weapon_row_y + 10))
                preview_label = self.font_small.render("Preview: Muzzle Mega Ion", True, (180, 180, 180))
                self.virtual_surf.blit(preview_label, (620, weapon_row_y + 80))
            
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

            hint_controls = self.font_small.render("Use UP/DOWN to move rows, LEFT/RIGHT to change values or select weapons, ENTER to confirm", True, (180, 180, 180))
            self.virtual_surf.blit(hint_controls, (100, 560))
            
            self._update_display()
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if event.type == KEYDOWN:
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
    
    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
