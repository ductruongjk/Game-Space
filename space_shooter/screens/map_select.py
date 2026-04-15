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
    
    def show(self, mode_name="PLAYER vs ENVIRONMENT", p1_name=".........."):
        """Display map selection and return selected map class"""
        clock = pygame.time.Clock()
        
        while True:
            self.virtual_surf.fill(BLACK)
            # Futuristic border
            pygame.draw.rect(self.virtual_surf, (0, 150, 255), (20, 20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2, border_radius=10)
            
            # Title
            title = self.font_large.render(mode_name, True, CYAN)
            self.virtual_surf.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
            
            # Player Name
            p_text = self.font_medium.render(f"Player 1 : {p1_name}", True, WHITE)
            self.virtual_surf.blit(p_text, (100, 120))
            
            # Selection Prompt
            prompt = self.font_small.render("# Select Map... Show [E]keys...", True, WHITE)
            self.virtual_surf.blit(prompt, (100, 180))
            
            # Draw map options with radio buttons
            for i, map_data in enumerate(self.maps):
                y_pos = 220 + i * 50
                is_selected = i == self.selected
                
                # Radio button circle
                circle_center = (120, y_pos + 12)
                pygame.draw.circle(self.virtual_surf, WHITE, circle_center, 12, 2)
                if is_selected:
                    pygame.draw.circle(self.virtual_surf, CYAN, circle_center, 8)
                
                # Checkbox for Map 1 as in image
                if i == 0:
                    pygame.draw.rect(self.virtual_surf, WHITE, (108, y_pos, 24, 24), 2)
                    if is_selected:
                        # Draw checkmark
                        pygame.draw.line(self.virtual_surf, CYAN, (112, y_pos + 12), (118, y_pos + 20), 3)
                        pygame.draw.line(self.virtual_surf, CYAN, (118, y_pos + 20), (128, y_pos + 6), 3)
                    else:
                        # If not selected but it's Map 1, still draw the box
                        pass

                # Map name
                name_color = WHITE if is_selected else (180, 180, 180)
                name = self.font_medium.render(map_data["name"], True, name_color)
                self.virtual_surf.blit(name, (150, y_pos))
            
            # Buttons
            btn_start = self.font_medium.render("START GAME", True, CYAN)
            btn_rect = btn_start.get_rect(center=(SCREEN_WIDTH//2, 450))
            pygame.draw.rect(self.virtual_surf, (30, 60, 80), btn_rect.inflate(100, 10), border_radius=5)
            pygame.draw.rect(self.virtual_surf, CYAN, btn_rect.inflate(100, 10), 2, border_radius=5)
            self.virtual_surf.blit(btn_start, btn_rect)
            
            btn_back = self.font_medium.render("BACK", True, RED)
            back_rect = btn_back.get_rect(center=(SCREEN_WIDTH//2, 510))
            pygame.draw.rect(self.virtual_surf, (80, 30, 30), back_rect.inflate(100, 10), border_radius=5)
            pygame.draw.rect(self.virtual_surf, RED, back_rect.inflate(100, 10), 2, border_radius=5)
            self.virtual_surf.blit(btn_back, back_rect)
            
            self._update_display()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP: self.selected = (self.selected - 1) % len(self.maps)
                    if event.key == K_DOWN: self.selected = (self.selected + 1) % len(self.maps)
                    if event.key == K_RETURN: return self.maps[self.selected]["class"]()
                    if event.key == K_ESCAPE: return None
            
            clock.tick(FPS)
    
    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
