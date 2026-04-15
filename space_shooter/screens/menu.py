"""
Main Menu Screen
"""
import pygame
import sys
from pygame.locals import *
from settings import *

class MainMenu:
    """Main menu with game mode selection"""
    
    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.font_large = pygame.font.Font(FONT_SPACE, 48)
        self.font_medium = pygame.font.Font(FONT_MAIN, 28)
        self.font_small = pygame.font.Font(FONT_MAIN, 14)
        
        self.options = [
            ("2 Players (PvP)", GAME_MODE_PVP),
            ("vs AI Bot (PvE)", GAME_MODE_PVE),
            ("Quit", None)
        ]
        self.selected = 0
    
    def show(self):
        """Display menu and return selected mode"""
        clock = pygame.time.Clock()
        
        while True:
            self.virtual_surf.fill(BLACK)
            
            # Draw title with glow effect
            title = self.font_large.render("SPACE SHOOTER", True, CYAN)
            title_glow = self.font_large.render("SPACE SHOOTER", True, (0, 100, 150))
            
            title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
            title_y = 100
            
            # Glow
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                self.virtual_surf.blit(title_glow, (title_x + offset[0], title_y + offset[1]))
            self.virtual_surf.blit(title, (title_x, title_y))
            
            # Draw subtitle
            subtitle = self.font_small.render("Select Game Mode", True, (200, 200, 200))
            self.virtual_surf.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 170))
            
            # Draw options
            for i, (text, mode) in enumerate(self.options):
                y_pos = 280 + i * 70
                
                # Selection indicator
                if i == self.selected:
                    # Glow box
                    pygame.draw.rect(self.virtual_surf, (0, 100, 100), 
                                   (SCREEN_WIDTH//2 - 160, y_pos - 10, 320, 50), border_radius=5)
                    pygame.draw.rect(self.virtual_surf, CYAN, 
                                   (SCREEN_WIDTH//2 - 160, y_pos - 10, 320, 50), 2, border_radius=5)
                    color = WHITE
                else:
                    color = (150, 150, 150)
                
                option_text = self.font_medium.render(text, True, color)
                self.virtual_surf.blit(option_text, 
                                     (SCREEN_WIDTH//2 - option_text.get_width()//2, y_pos))
            
            # Controls hint
            hint = self.font_small.render("UP/DOWN: Navigate  |  ENTER: Select", True, (100, 100, 100))
            self.virtual_surf.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 60))
            
            # Scale and display
            self._update_display()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == K_RETURN:
                        mode = self.options[self.selected][1]
                        if mode is None:  # Quit
                            return None
                        return mode
                    elif event.key == K_ESCAPE:
                        return None
            
            clock.tick(FPS)
    
    def _update_display(self):
        """Scale virtual surface to window"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
