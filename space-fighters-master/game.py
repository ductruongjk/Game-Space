"""
Game module - Main gameplay loop
"""
import pygame
import math
import random
from pygame.locals import *
from settings import *
from player import Ship, Rocket, AIController
from maps import DeepSpaceMap, GravityChaosMap, ReverseGravityMap

class Game:
    """Main game controller"""
    
    def __init__(self, window, virtual_surf, game_mode, map_name, stats1, stats2):
        self.window = window
        self.virtual_surf = virtual_surf
        self.game_mode = game_mode
        self.map_name = map_name
        
        # Load images
        self.ship1_img = pygame.image.load(ASSET_SHIP1)
        self.ship2_img = pygame.image.load(ASSET_SHIP2)
        self.ship1_ls_img = pygame.image.load(ASSET_SHIP1_LS)
        self.ship2_ls_img = pygame.image.load(ASSET_SHIP2_LS)
        self.rocket1_img = pygame.image.load(ASSET_ROCKET1)
        self.rocket2_img = pygame.image.load(ASSET_ROCKET2)
        self.bg = pygame.image.load(ASSET_BG)
        
        try:
            self.respawn_gif = pygame.image.load('resources/respawn_anim_900x900_test.png')
        except:
            self.respawn_gif = pygame.Surface((100, 100))
            self.respawn_gif.fill(GREEN)
            
        # Load music
        try:
            pygame.mixer.music.load(AUDIO_BG_MUSIC)
        except:
            pass
            
        # Load sounds
        try:
            self.missile_snd = pygame.mixer.Sound(AUDIO_MISSILE)
            self.explosion_snd = pygame.mixer.Sound(AUDIO_EXPLOSION)
        except:
            self.missile_snd = None
            self.explosion_snd = None
            
        # Create map
        if map_name == MAP_DEEP_SPACE:
            self.map = DeepSpaceMap()
        elif map_name == MAP_GRAVITY_CHAOS:
            self.map = GravityChaosMap()
        elif map_name == MAP_REVERSE_GRAVITY:
            self.map = ReverseGravityMap()
        else:
            self.map = DeepSpaceMap()
            
        # Create ships
        x, y = SCREEN_WIDTH, SCREEN_HEIGHT
        self.ship1 = Ship(x * 0.8, y * 0.8, 1, stats1, self.ship1_img, self.ship1_ls_img)
        self.ship2 = Ship(x * 0.2, y * 0.8, 2, stats2, self.ship2_img, self.ship2_ls_img)
        
        # Create rockets
        self.rocket1 = Rocket(999, 999, 0, False, 1, stats1[2])
        self.rocket2 = Rocket(999, 999, 0, False, 2, stats2[2])
        
        # AI controller
        self.ai = AIController(self.ship2, self.ship1) if game_mode == GAME_MODE_PVE else None
        
        # Game state
        self.p1_score = 0
        self.p2_score = 0
        self.frame_nr = 0
        self.frame_cd1 = 0
        self.frame_cd2 = 0
        self.running = True
        self.winner = None
        
        # Reverse gravity state (for map 3)
        self.controls_reversed = False
        self.reverse_timer = REVERSE_INTERVAL
        
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.play(-1, 0)
        except:
            pass
        
        while self.running:
            self.frame_nr += 1
            
            # Clear screen
            self.virtual_surf.fill(BLACK)
            self.map.draw(self.virtual_surf)
            
            # Update map physics
            self.map.update()
            self.map.apply_physics(self.ship1)
            self.map.apply_physics(self.ship2)
            
            # Handle reverse gravity controls
            if isinstance(self.map, ReverseGravityMap):
                if self.map.gravity_reversed != self.controls_reversed:
                    self.controls_reversed = self.map.gravity_reversed
            
            # Update ships
            self.ship1.move(self.virtual_surf, self.respawn_gif)
            self.ship2.move(self.virtual_surf, self.respawn_gif)
            
            # Draw HP bars
            self.ship1.draw_hp_bar(self.virtual_surf, int(self.ship1.x), int(self.ship1.y) - 15)
            self.ship2.draw_hp_bar(self.virtual_surf, int(self.ship2.x), int(self.ship2.y) - 15)
            
            # Update rockets
            self.rocket1.move(self.virtual_surf, self.rocket1_img)
            self.rocket2.move(self.virtual_surf, self.rocket2_img)
            
            # AI update
            if self.ai and self.game_mode == GAME_MODE_PVE:
                self.rocket2, self.frame_cd2, _ = self.ai.update(
                    self.frame_nr, self.rocket2, self.frame_cd2, self.ship2.superweapon)
            
            # Check collisions
            self._check_collisions()
            
            # Check win condition
            if self._check_win():
                return self._get_result()
            
            # Draw UI
            self._draw_ui()
            
            # Update display
            self._update_display()
            
            # Event handling
            self._handle_events()
            
            clock.tick(FPS)
            
    def _check_collisions(self):
        """Check all collision types"""
        # Ship-ship collision
        if abs(self.ship1.x - self.ship2.x) < 30 and abs(self.ship1.y - self.ship2.y) < 30:
            if self.ship1.alive and self.ship2.alive:
                self.ship1.take_damage(DAMAGE_PER_HIT)
                self.ship2.take_damage(DAMAGE_PER_HIT)
                if self.explosion_snd:
                    self.explosion_snd.play()
        
        # Rocket 1 hits Ship 2
        if self.rocket1.exists and self.ship2.alive:
            if abs(self.rocket1.x - self.ship2.x) < 25 and abs(self.rocket1.y - self.ship2.y) < 25:
                if not self.map.check_asteroid_collision(self.rocket1.x, self.rocket1.y, 10):
                    if self.ship2.take_damage(DAMAGE_PER_HIT):
                        self.p1_score += 1
                    self.p2_score += 10  # Points for hits
                    self.rocket1.exists = False
                    if self.explosion_snd:
                        self.explosion_snd.play()
        
        # Rocket 2 hits Ship 1
        if self.rocket2.exists and self.ship1.alive:
            if abs(self.rocket2.x - self.ship1.x) < 25 and abs(self.rocket2.y - self.ship1.y) < 25:
                if not self.map.check_asteroid_collision(self.rocket2.x, self.rocket2.y, 10):
                    if self.ship1.take_damage(DAMAGE_PER_HIT):
                        self.p2_score += 1
                    self.p1_score += 10
                    self.rocket2.exists = False
                    if self.explosion_snd:
                        self.explosion_snd.play()
        
        # Check asteroid collisions for ships
        if self.map.check_asteroid_collision(self.ship1.x, self.ship1.y, 20):
            self.ship1.take_damage(DAMAGE_PER_HIT)
            if self.explosion_snd:
                self.explosion_snd.play()
        if self.map.check_asteroid_collision(self.ship2.x, self.ship2.y, 20):
            self.ship2.take_damage(DAMAGE_PER_HIT)
            if self.explosion_snd:
                self.explosion_snd.play()
                
    def _check_win(self):
        """Check if game should end"""
        if self.ship1.hp <= 0:
            self.winner = 2
            return True
        if self.ship2.hp <= 0:
            self.winner = 1
            return True
        return False
        
    def _get_result(self):
        """Return game result"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
        return {
            'winner': self.winner,
            'p1_score': self.p1_score,
            'p2_score': self.p2_score,
            'p1_hp': self.ship1.hp,
            'p2_hp': self.ship2.hp
        }
        
    def _draw_ui(self):
        """Draw in-game UI"""
        # HP bars at top
        # P1 (Blue)
        pygame.draw.rect(self.virtual_surf, DARK_GRAY, (20, 20, 200, 20))
        hp1_width = int(200 * (self.ship1.hp / MAX_HP))
        color1 = GREEN if self.ship1.hp > 50 else YELLOW if self.ship1.hp > 25 else RED
        pygame.draw.rect(self.virtual_surf, color1, (20, 20, hp1_width, 20))
        pygame.draw.rect(self.virtual_surf, CYAN, (20, 20, 200, 20), 2)
        hp1_text = FONT_SMALL.render(f"Blue: {self.ship1.hp} HP", True, WHITE)
        self.virtual_surf.blit(hp1_text, (25, 22))
        
        # P2 (Red)
        pygame.draw.rect(self.virtual_surf, DARK_GRAY, (SCREEN_WIDTH - 220, 20, 200, 20))
        hp2_width = int(200 * (self.ship2.hp / MAX_HP))
        color2 = GREEN if self.ship2.hp > 50 else YELLOW if self.ship2.hp > 25 else RED
        pygame.draw.rect(self.virtual_surf, color2, (SCREEN_WIDTH - 220, 20, hp2_width, 20))
        pygame.draw.rect(self.virtual_surf, RED, (SCREEN_WIDTH - 220, 20, 200, 20), 2)
        hp2_text = FONT_SMALL.render(f"Red: {self.ship2.hp} HP", True, WHITE)
        self.virtual_surf.blit(hp2_text, (SCREEN_WIDTH - 215, 22))
        
        # Map info
        map_text = FONT_SMALL.render(self.map.get_info(), True, WHITE)
        self.virtual_surf.blit(map_text, (SCREEN_WIDTH//2 - map_text.get_width()//2, 20))
        
        # Controls hint
        if self.game_mode == GAME_MODE_PVP:
            hint = FONT_TINY.render("P1: WASD+F  |  P2: Arrows+LShift", True, GRAY)
        else:
            hint = FONT_TINY.render("P1: WASD+F  |  AI Controls Red", True, GRAY)
        self.virtual_surf.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 30))
        
    def _handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == VIDEORESIZE:
                self.window = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    return
                
                # Handle control reversal
                reverse = -1 if self.controls_reversed else 1
                
                # P1 Controls (Blue) - WASD
                if event.key == K_a:
                    self.ship1.change_angle("LEFT" if reverse == 1 else "RIGHT")
                elif event.key == K_d:
                    self.ship1.change_angle("RIGHT" if reverse == 1 else "LEFT")
                elif event.key == K_w:
                    # Forward thrust (not implemented in current Ship class)
                    pass
                elif event.key == K_f:
                    # Shoot
                    if not self.rocket1.exists and self.ship1.alive:
                        self.rocket1 = Rocket(self.ship1.x, self.ship1.y, 
                                            self.ship1.direction, True, 1, 
                                            self.ship1.rocket_speed)
                        if self.missile_snd:
                            self.missile_snd.play()
                
                # P2 Controls (Red) - Arrow keys
                if self.game_mode == GAME_MODE_PVP:
                    if event.key == K_LEFT:
                        self.ship2.change_angle("LEFT" if reverse == 1 else "RIGHT")
                    elif event.key == K_RIGHT:
                        self.ship2.change_angle("RIGHT" if reverse == 1 else "LEFT")
                    elif event.key == K_LSHIFT:
                        # P2 Shoot
                        if not self.rocket2.exists and self.ship2.alive:
                            self.rocket2 = Rocket(self.ship2.x, self.ship2.y,
                                                self.ship2.direction, True, 2,
                                                self.ship2.rocket_speed)
                            if self.missile_snd:
                                self.missile_snd.play()
                            
            if event.type == KEYUP:
                reverse = -1 if self.controls_reversed else 1
                
                if event.key == K_a:
                    self.ship1.change_angle("LEFT2" if reverse == 1 else "RIGHT2")
                elif event.key == K_d:
                    self.ship1.change_angle("RIGHT2" if reverse == 1 else "LEFT2")
                    
                if self.game_mode == GAME_MODE_PVP:
                    if event.key == K_LEFT:
                        self.ship2.change_angle("LEFT2" if reverse == 1 else "RIGHT2")
                    elif event.key == K_RIGHT:
                        self.ship2.change_angle("RIGHT2" if reverse == 1 else "LEFT2")
                        
    def _update_display(self):
        """Scale and update display"""
        window_size = self.window.get_size()
        scaled = pygame.transform.smoothscale(self.virtual_surf, window_size)
        self.window.blit(scaled, (0, 0))
        pygame.display.update()
