"""
Main Menu Screen
"""
import pygame
import sys
import random
import math
from pygame.locals import *
from settings import *

class MainMenu:
    """Main menu with game mode selection"""
    
    def __init__(self, window, virtual_surf):
        self.window = window
        self.virtual_surf = virtual_surf
        self.font_large = pygame.font.Font(FONT_SPACE, 48)
        self.font_medium = pygame.font.Font(FONT_MAIN, 28)
        self.font_small = pygame.font.Font(FONT_MAIN, 18)
        self.font_tiny = pygame.font.Font(FONT_MAIN, 14)
        
        # Load Assets
        self.title_img = self._load_img(ASSET_TITLE, (320, 110))
        self.robot_img = self._load_img(ASSET_ROBOT, (140, 140))
        self.people_img = self._load_img(ASSET_PEOPLE, (140, 140))
        self.border_img = self._load_img(ASSET_VIEN, (340, 210))  # Use vien.png
        self.play_btn_img = self._load_img(ASSET_PLAY_BTN, (200, 50))
        
        self.selected = 0  # 0: PVP, 1: PVE
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.5),
                'size': random.randint(1, 3)
            })
        self.frame = 0

    def _load_img(self, path, size=None):
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                return pygame.transform.smoothscale(img, size)
            return img
        except:
            return None

    def show(self):
        """Display menu and return selected mode"""
        clock = pygame.time.Clock()
        pygame.key.set_repeat(0)
        
        while True:
            self.frame += 1
            self.virtual_surf.fill((5, 10, 30)) # Dark Blue/Space
            
            # 1. Background Grid and Particles
            self._draw_background()
            
            # 1.5 Screen Border (vien.png around entire screen)
            self._draw_screen_border()
            
            # 2. Title
            if self.title_img:
                rect = self.title_img.get_rect(center=(SCREEN_WIDTH//2, 80))
                # Title Glow
                glow_surf = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (0, 100, 255, 50), glow_surf.get_rect())
                self.virtual_surf.blit(glow_surf, (rect.x - 10, rect.y - 10))
                self.virtual_surf.blit(self.title_img, rect)
            
            # 3. Subtitles
            sub1 = self.font_medium.render("Which mode would you like to play?", True, WHITE)
            self.virtual_surf.blit(sub1, (SCREEN_WIDTH//2 - sub1.get_width()//2, 150))
            sub2 = self.font_small.render("Shau [I]jeys . . .", True, (180, 220, 255))
            self.virtual_surf.blit(sub2, (SCREEN_WIDTH//2 - sub2.get_width()//2, 190))
            
            # 4. Mode Selection Boxes
            self._draw_mode_boxes()
            
            # 5. Buttons
            start_mode = "PVP" if self.selected == 0 else "PVE"
            quit_btn_clicked = self._draw_buttons()
            
            # 6. Controls hint (Simplified as per image focus)
            
            self._update_display()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit(); sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_p or event.key == K_LEFT:
                        self.selected = 0
                    elif event.key == K_e or event.key == K_RIGHT:
                        self.selected = 1
                    elif event.key == K_RETURN:
                        return "PVP" if self.selected == 0 else "PVE"
                    elif event.key == K_ESCAPE:
                        return None
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = self._get_mouse_pos()
                    # Check box clicks
                    if 50 < mx < 390 and 240 < my < 440:
                        self.selected = 0
                    elif 410 < mx < 750 and 240 < my < 440:
                        self.selected = 1
                    # Check button clicks (Start)
                    start_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 430, 200, 50)
                    if start_rect.collidepoint(mx, my):
                        return "PVP" if self.selected == 0 else "PVE"
                    # Check button clicks (Quit)
                    quit_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, 490, 200, 40)
                    if quit_rect.collidepoint(mx, my):
                        return None

            clock.tick(FPS)

    def _draw_background(self):
        # Fill with dark space color
        self.virtual_surf.fill((5, 10, 25))
        
        # Grid with Perspective effect (matching the image)
        grid_color = (20, 60, 120)
        
        # Horizontal lines with perspective (closer at bottom, farther at top)
        for i in range(20):
            # Normalized position 0 to 1 (bottom to top)
            t = i / 20.0
            # Perspective curve: lines get closer together as they go up
            y = SCREEN_HEIGHT - (t ** 0.7) * (SCREEN_HEIGHT * 0.7)
            alpha = int(255 * (1 - t * 0.5))  # Fade out at top
            pygame.draw.line(self.virtual_surf, grid_color + (alpha,), (0, int(y)), (SCREEN_WIDTH, int(y)))
        
        # Vertical lines converging to center vanishing point
        vanishing_y = -100  # Above the screen
        vanishing_x = SCREEN_WIDTH // 2
        
        for i in range(-10, 30, 2):
            # Bottom spread
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

    def _draw_mode_boxes(self):
        # PVP Box (Left) - smaller and centered
        pvp_rect = pygame.Rect(60, 230, 340, 200)
        self._draw_box(pvp_rect, "[P]", "PvP", "Player vs Player", self.people_img, self.selected == 0)
        
        # PVE Box (Right)
        pve_rect = pygame.Rect(400, 230, 340, 200)
        self._draw_box(pve_rect, "[E]", "PvE", "Player vs Environment", self.robot_img, self.selected == 1)

    def _remove_white_bg(self, img):
        """Convert white background to transparent"""
        if img is None:
            return None
        # Create a copy with per-pixel alpha
        img_rgba = img.convert_alpha()
        pixels = pygame.surfarray.pixels3d(img_rgba)
        alpha = pygame.surfarray.pixels_alpha(img_rgba)
        
        # White pixels become transparent
        white_mask = (pixels[:,:,0] > 240) & (pixels[:,:,1] > 240) & (pixels[:,:,2] > 240)
        alpha[white_mask] = 0
        
        del pixels, alpha
        return img_rgba

    def _draw_screen_border(self):
        """Draw vien.png as border around entire screen"""
        if self.border_img:
            # Scale to fit entire screen
            border_scaled = pygame.transform.smoothscale(self.border_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # Remove white background
            border_clean = self._remove_white_bg(border_scaled)
            if border_clean:
                self.virtual_surf.blit(border_clean, (0, 0))

    def _draw_box(self, rect, key_label, short_title, full_title, img, is_selected):
        # Draw semi-transparent background for the box
        bg_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        if is_selected:
            # Stronger glow when selected
            pygame.draw.rect(bg_surf, (0, 150, 200, 80), bg_surf.get_rect(), border_radius=15)
            pygame.draw.rect(bg_surf, (0, 220, 255, 150), bg_surf.get_rect(), 3, border_radius=15)
        else:
            # Subtle border when not selected
            pygame.draw.rect(bg_surf, (50, 80, 120, 60), bg_surf.get_rect(), border_radius=15)
            pygame.draw.rect(bg_surf, (100, 150, 200, 100), bg_surf.get_rect(), 2, border_radius=15)
        
        self.virtual_surf.blit(bg_surf, rect)
        
        # Key label [P] or [E] - positioned at top left
        key_txt = self.font_medium.render(key_label, True, CYAN if is_selected else (150, 200, 255))
        self.virtual_surf.blit(key_txt, (rect.x + 20, rect.y + 15))
        
        # Short title (PvP / PvE) - big and cyan
        short_txt = self.font_medium.render(short_title, True, CYAN if is_selected else (200, 230, 255))
        self.virtual_surf.blit(short_txt, (rect.x + 20, rect.y + 50))
        
        # Full title - smaller font, wrapped
        words = full_title.replace(" vs ", "\nvs ").split("\n")
        small_font = pygame.font.Font(FONT_MAIN, 20)
        for i, line in enumerate(words):
            color = WHITE if i == 0 else (180, 200, 220)
            t = small_font.render(line, True, color)
            # Position text on the right side, centered vertically
            text_x = rect.x + 180
            text_y = rect.y + 90 + i * 28
            self.virtual_surf.blit(t, (text_x, text_y))
        
        # Image - positioned at left center
        if img:
            img_clean = self._remove_white_bg(img)
            if img_clean:
                img_rect = img_clean.get_rect(center=(rect.x + 100, rect.y + 120))
                if is_selected: # Pulse effect
                    scale = 1.0 + math.sin(self.frame * 0.08) * 0.05
                    w, h = img_rect.width, img_rect.height
                    s_img = pygame.transform.smoothscale(img_clean, (int(w*scale), int(h*scale)))
                    self.virtual_surf.blit(s_img, s_img.get_rect(center=img_rect.center))
                else:
                    self.virtual_surf.blit(img_clean, img_rect)

    def _draw_buttons(self):
        mx, my = self._get_mouse_pos()
        
        # Start Game Button - Blue style like in the image
        start_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, 440, 240, 50)
        is_hover = start_rect.collidepoint(mx, my)
        
        # Draw button background
        btn_surf = pygame.Surface((start_rect.width, start_rect.height), pygame.SRCALPHA)
        if is_hover:
            pygame.draw.rect(btn_surf, (0, 120, 180, 200), btn_surf.get_rect(), border_radius=8)
            pygame.draw.rect(btn_surf, (0, 200, 255, 255), btn_surf.get_rect(), 3, border_radius=8)
            # Glow effect
            glow = pygame.Surface((start_rect.width + 20, start_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (0, 200, 255, 60), glow.get_rect(), border_radius=12)
            self.virtual_surf.blit(glow, (start_rect.x - 10, start_rect.y - 10))
        else:
            pygame.draw.rect(btn_surf, (30, 80, 120, 180), btn_surf.get_rect(), border_radius=8)
            pygame.draw.rect(btn_surf, (100, 180, 220, 200), btn_surf.get_rect(), 2, border_radius=8)
        
        self.virtual_surf.blit(btn_surf, start_rect)
        
        # Button text
        txt_color = WHITE if is_hover else (200, 230, 255)
        txt = self.font_small.render("Start Game", True, txt_color)
        self.virtual_surf.blit(txt, txt.get_rect(center=start_rect.center))

        # Quit Game Button - Red style
        quit_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, 500, 240, 45)
        is_q_hover = quit_rect.collidepoint(mx, my)
        
        quit_surf = pygame.Surface((quit_rect.width, quit_rect.height), pygame.SRCALPHA)
        if is_q_hover:
            pygame.draw.rect(quit_surf, (180, 40, 40, 200), quit_surf.get_rect(), border_radius=8)
            pygame.draw.rect(quit_surf, (255, 100, 100, 255), quit_surf.get_rect(), 3, border_radius=8)
        else:
            pygame.draw.rect(quit_surf, (100, 30, 30, 180), quit_surf.get_rect(), border_radius=8)
            pygame.draw.rect(quit_surf, (180, 80, 80, 200), quit_surf.get_rect(), 2, border_radius=8)
        
        self.virtual_surf.blit(quit_surf, quit_rect)
        q_txt = self.font_small.render("Quit Game", True, WHITE)
        self.virtual_surf.blit(q_txt, q_txt.get_rect(center=quit_rect.center))

    def _get_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        win_w, win_h = self.window.get_size()
        return mx * SCREEN_WIDTH / win_w, my * SCREEN_HEIGHT / win_h

    def _update_display(self):
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
