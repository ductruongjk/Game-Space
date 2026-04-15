"""
Game Mode Selection Screen
"""
import pygame
import sys
from pygame.locals import *
from settings import *

class ModeSelect:
    """Select between PvP and PvE modes"""
    
    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.font_large = pygame.font.Font(FONT_SPACE, 36)
        self.font_medium = pygame.font.Font(FONT_MAIN, 22)
        self.font_small = pygame.font.Font(FONT_MAIN, 14)
        
        self.modes = [
            {
                "name": "2 PLAYERS (PvP)",
                "subtitle": "Local multiplayer battle",
                "p1_controls": "Arrow Keys: Move | UP: Shoot | DOWN: Super",
                "p2_controls": "WASD: Move | W: Shoot | S: Super",
                "mode": GAME_MODE_PVP,
                "color": BLUE
            },
            {
                "name": "VS AI BOT (PvE)",
                "subtitle": "Battle against computer",
                "p1_controls": "Arrow Keys: Move | UP: Shoot | DOWN: Super",
                "p2_controls": "AI Bot: Auto-controlled opponent",
                "mode": GAME_MODE_PVE,
                "color": RED
            }
        ]
        self.selected = 0
    
    def show(self):
        """Display mode selection"""
        clock = pygame.time.Clock()
        pygame.key.set_repeat(0)  # Disable key repeat
        
        while True:
            self.virtual_surf.fill(BLACK)
            
            # Title
            title = self.font_large.render("CHOOSE GAME MODE", True, CYAN)
            self.virtual_surf.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 60))
            
            # Mode cards
            for i, mode in enumerate(self.modes):
                x_pos = 80 if i == 0 else SCREEN_WIDTH // 2 + 20
                y_pos = 160
                width = SCREEN_WIDTH // 2 - 100
                height = 280
                
                is_selected = i == self.selected
                
                # Card background
                bg_color = (40, 40, 60) if is_selected else (25, 25, 35)
                border_color = mode["color"] if is_selected else (80, 80, 80)
                
                pygame.draw.rect(self.virtual_surf, bg_color, 
                               (x_pos, y_pos, width, height), border_radius=10)
                pygame.draw.rect(self.virtual_surf, border_color, 
                               (x_pos, y_pos, width, height), 3 if is_selected else 1, border_radius=10)
                
                # Mode name
                name = self.font_medium.render(mode["name"], True, 
                                              WHITE if is_selected else (180, 180, 180))
                self.virtual_surf.blit(name, (x_pos + 20, y_pos + 20))
                
                # Subtitle
                subtitle = self.font_small.render(mode["subtitle"], True, (150, 150, 150))
                self.virtual_surf.blit(subtitle, (x_pos + 20, y_pos + 55))
                
                # Separator
                pygame.draw.line(self.virtual_surf, (80, 80, 80), 
                               (x_pos + 20, y_pos + 85), (x_pos + width - 20, y_pos + 85), 1)
                
                # Controls info
                p1 = self.font_small.render("P1: " + mode["p1_controls"], True, (200, 200, 200))
                self.virtual_surf.blit(p1, (x_pos + 20, y_pos + 105))
                
                p2 = self.font_small.render(mode["p2_controls"], True, (200, 200, 200))
                self.virtual_surf.blit(p2, (x_pos + 20, y_pos + 130))
                
                # Selection indicator
                if is_selected:
                    indicator = self.font_small.render("> SELECTED <", True, mode["color"])
                    self.virtual_surf.blit(indicator, 
                                         (x_pos + width//2 - indicator.get_width()//2, y_pos + 230))
            
            # Navigation hints
            left_right = self.font_small.render("LEFT/RIGHT: Switch  |  ENTER: Confirm  |  ESC: Back", 
                                              True, (100, 100, 100))
            self.virtual_surf.blit(left_right, (SCREEN_WIDTH//2 - left_right.get_width()//2, 
                                             SCREEN_HEIGHT - 50))
            
            self._update_display()
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == K_a:
                        self.selected = max(0, self.selected - 1)
                    elif event.key == K_RIGHT or event.key == K_d:
                        self.selected = min(len(self.modes) - 1, self.selected + 1)
                    elif event.key == K_RETURN or event.key == K_SPACE:
                        return self.modes[self.selected]["mode"]
                    elif event.key == K_ESCAPE or event.key == K_BACKSPACE:
                        return None
            
            clock.tick(FPS)
    
    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
