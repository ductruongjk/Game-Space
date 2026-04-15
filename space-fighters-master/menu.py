"""
Menu system - Main menu, mode selection, map selection
"""
import pygame
import sys
from pygame.locals import *
from settings import *

class MainMenu:
    """Main menu with mode selection"""
    
    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.options = [
            ("Player vs AI (PvE)", GAME_MODE_PVE),
            ("Player vs Player (PvP)", GAME_MODE_PVP),
            ("Quit", None)
        ]
        self.selected = 0
        
    def show(self):
        """Display main menu and return selected mode"""
        clock = pygame.time.Clock()
        
        while True:
            self.virtual_surf.fill(BLACK)
            
            # Title
            title = FONT_TITLE.render("SPACE FIGHTERS", True, CYAN)
            title_glow = FONT_TITLE.render("SPACE FIGHTERS", True, (0, 100, 150))
            
            title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
            title_y = 100
            
            # Glow effect
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                self.virtual_surf.blit(title_glow, (title_x + offset[0], title_y + offset[1]))
            self.virtual_surf.blit(title, (title_x, title_y))
            
            # Subtitle
            subtitle = FONT_SMALL.render("Select Game Mode", True, (200, 200, 200))
            self.virtual_surf.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 180))
            
            # Menu options
            for i, (text, mode) in enumerate(self.options):
                y_pos = 280 + i * 70
                
                if i == self.selected:
                    # Highlight box
                    pygame.draw.rect(self.virtual_surf, (0, 100, 100), 
                                   (SCREEN_WIDTH//2 - 160, y_pos - 10, 320, 50), border_radius=5)
                    pygame.draw.rect(self.virtual_surf, CYAN, 
                                   (SCREEN_WIDTH//2 - 160, y_pos - 10, 320, 50), 2, border_radius=5)
                    color = WHITE
                else:
                    color = (150, 150, 150)
                    
                option_text = FONT_MED.render(text, True, color)
                self.virtual_surf.blit(option_text, 
                                     (SCREEN_WIDTH//2 - option_text.get_width()//2, y_pos))
            
            # Controls hint
            hint = FONT_TINY.render("UP/DOWN: Navigate  |  ENTER: Select  |  ESC: Quit", True, (100, 100, 100))
            self.virtual_surf.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 60))
            
            self._update_display()
            
            # Event handling
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
                        if mode is None:
                            pygame.quit()
                            sys.exit()
                        return mode
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            clock.tick(FPS)
            
    def _update_display(self):
        """Scale and update display"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()


class MapSelect:
    """Map selection screen"""
    
    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.maps = [
            ("Deep Space Arena", MAP_DEEP_SPACE, "Open space combat"),
            ("Gravity Chaos Zone", MAP_GRAVITY_CHAOS, "Black hole & asteroids"),
            ("Reverse Gravity Zone", MAP_REVERSE_GRAVITY, "Controls reverse every 15s")
        ]
        self.selected = 0
        
    def show(self):
        """Display map selection and return selected map name"""
        clock = pygame.time.Clock()
        
        while True:
            self.virtual_surf.fill(BLACK)
            
            # Title
            title = FONT_TITLE.render("SELECT MAP", True, CYAN)
            self.virtual_surf.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
            
            # Map options
            for i, (name, key, desc) in enumerate(self.maps):
                y_pos = 180 + i * 120
                is_selected = i == self.selected
                
                # Box
                box_color = (0, 100, 100) if is_selected else DARK_GRAY
                border_color = CYAN if is_selected else GRAY
                pygame.draw.rect(self.virtual_surf, box_color, 
                               (100, y_pos, SCREEN_WIDTH - 200, 100), border_radius=10)
                pygame.draw.rect(self.virtual_surf, border_color, 
                               (100, y_pos, SCREEN_WIDTH - 200, 100), 2, border_radius=10)
                
                # Map name
                name_text = FONT_MED.render(name, True, WHITE)
                self.virtual_surf.blit(name_text, (120, y_pos + 20))
                
                # Description
                desc_text = FONT_SMALL.render(desc, True, (200, 200, 200))
                self.virtual_surf.blit(desc_text, (120, y_pos + 55))
                
            # Controls hint
            hint = FONT_TINY.render("UP/DOWN: Navigate  |  ENTER: Select  |  ESC: Back", True, GRAY)
            self.virtual_surf.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 50))
            
            self._update_display()
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.maps)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.maps)
                    elif event.key == K_RETURN:
                        return self.maps[self.selected][1]
                    elif event.key == K_ESCAPE:
                        return "back"
                        
            clock.tick(FPS)
            
    def _update_display(self):
        """Scale and update display"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()


class WinnerScreen:
    """Show winner and rewards"""
    
    def __init__(self, window, virtual_surf, winner, p1_score, p2_score, is_pve, money_earned):
        self.window = window
        self.virtual_surf = virtual_surf
        self.winner = winner  # 1 = P1/Blue, 2 = P2/Red
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.is_pve = is_pve
        self.money_earned = money_earned
        
    def show(self):
        """Display winner screen"""
        clock = pygame.time.Clock()
        
        # Determine winner text
        if self.winner == 1:
            winner_text = f"BLUE (Player 1) WINS!"
            winner_color = CYAN
        else:
            if self.is_pve:
                winner_text = "RED (AI BOT) WINS!"
            else:
                winner_text = "RED (Player 2) WINS!"
            winner_color = RED
            
        wait_time = 3  # seconds before allowing continue
        start_time = pygame.time.get_ticks()
        
        while True:
            self.virtual_surf.fill(BLACK)
            
            # Winner text
            title = FONT_TITLE.render("GAME OVER", True, WHITE)
            self.virtual_surf.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
            
            winner = FONT_BIG.render(winner_text, True, winner_color)
            self.virtual_surf.blit(winner, (SCREEN_WIDTH//2 - winner.get_width()//2, 160))
            
            # Scores
            p1_text = FONT_MED.render(f"Blue Score: {self.p1_score}", True, CYAN)
            p2_text = FONT_MED.render(f"Red Score: {self.p2_score}", True, RED)
            self.virtual_surf.blit(p1_text, (200, 250))
            self.virtual_surf.blit(p2_text, (450, 250))
            
            # Money earned
            money_text = FONT_MED.render(f"Money Earned: ${self.money_earned}", True, GOLD)
            self.virtual_surf.blit(money_text, (SCREEN_WIDTH//2 - money_text.get_width()//2, 320))
            
            # Continue prompt (after delay)
            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            if elapsed > wait_time:
                prompt = FONT_SMALL.render("Press ENTER to continue...", True, WHITE)
                self.virtual_surf.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 400))
            else:
                countdown = FONT_SMALL.render(f"Continuing in {int(wait_time - elapsed) + 1}...", True, GRAY)
                self.virtual_surf.blit(countdown, (SCREEN_WIDTH//2 - countdown.get_width()//2, 400))
                
            self._update_display()
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == KEYDOWN:
                    if elapsed > wait_time:
                        if event.key == K_RETURN or event.key == K_ESCAPE:
                            return
                            
            clock.tick(FPS)
            
    def _update_display(self):
        """Scale and update display"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
