"""
Player/Ship entity
"""
import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Ship:
    """Player ship class with movement, weapons and abilities"""
    
    def __init__(self, x, y, player, shipspeed=1, maneuv=1):
        self.player = player
        self.x = random.choice(range(5, 9)) * x / 10
        self.y = random.choice(range(5, 9)) * y / 10
        self.speed = 0.7 * shipspeed
        self.direction = 0
        self.k_left = self.k_right = 0
        self.lukas = False  # Debuff status
        self.boolean = False
        self.direc = ""
        self.alive = True
        self.maneuv = maneuv
        
        # Lightspeed ability
        self.ls_start = [0, 0]
        self.ls_end = [0, 0]
        self.ls_alive = False
        self.last = pygame.time.get_ticks()
        
        # Respawn animation
        self.respawn_duration = 1600
        self.respawn_animation = 0
        self.respawn_running = True
        self.respawn_x = self.x
        self.respawn_y = self.y
        
        # AI attributes
        self.ai_target = None
        self.ai_last_shot = 0
        self.ai_shoot_cooldown = 60
        self.ai_move_timer = 0
        self.ai_avoiding = False
    
    def respawn(self, display, respawn_gif):
        """Handle respawn animation"""
        self.alive = False
        now = pygame.time.get_ticks()
        if now % 2 == 0:
            self.respawn_animation += 1
        if now - self.last <= self.respawn_duration:
            display.blit(respawn_gif, (self.respawn_x - 50, self.respawn_y - 50),
                        pygame.Rect((self.respawn_animation % 9) * 900 / 9,
                                    (self.respawn_animation // 9) * 900 / 9,
                                    900 / 9, 900 / 9))
        else:
            self.respawn_running = False
            self.alive = True
            self.x = self.respawn_x
            self.y = self.respawn_y
    
    def move(self, display, ship_img, ship_ls_img, respawn_gif):
        """Update ship position and render"""
        if self.respawn_running:
            self.respawn(display, respawn_gif)
            return
        
        if self.alive:
            self.direction = 0
            self.direction += (self.k_left + self.k_right)
            
            rad = self.direction * math.pi / 180
            self.x += -self.speed * math.sin(rad)
            self.y += -self.speed * math.cos(rad)
            
            # Wrap around screen
            if self.x > SCREEN_WIDTH:
                self.x = 0
            if self.x < 0:
                self.x = SCREEN_WIDTH
            if self.y > SCREEN_HEIGHT:
                self.y = 0
            if self.y < 0:
                self.y = SCREEN_HEIGHT
            
            # Render ship
            image = pygame.transform.rotate(ship_img, self.direction)
            self.image = image
            display.blit(image, (self.x, self.y))
        else:
            self.x = self.y = SCREEN_WIDTH * self.player
    
    def change_angle(self, direc, luka):
        """Start turning"""
        if direc == "LEFT":
            self.boolean = True
            self.direc = "LEFT"
        if direc == "RIGHT":
            self.boolean = True
            self.direc = "RIGHT"
        if direc == "LEFT2":
            self.boolean = False
            self.direc = "LEFT2"
        if direc == "RIGHT2":
            self.boolean = False
            self.direc = "RIGHT2"
    
    def change_angle2(self):
        """Update turning based on maneuverability"""
        m = 0.6 * self.maneuv
        if self.direc == "LEFT" and self.boolean:
            if not self.lukas:
                self.k_left += m
            else:
                self.k_right += -m
        if self.direc == "RIGHT" and self.boolean:
            if not self.lukas:
                self.k_right += -m
            else:
                self.k_left += m
    
    def start_lightspeed(self, others, ship_ls_img, display):
        """Activate lightspeed superweapon - dash forward killing enemies in path"""
        from entities.bullet import Point, lies_between, distance
        
        if self.alive:
            self.ls_alive = True
            self.ls_start = [self.x, self.y]
            rad = self.direction * math.pi / 180
            self.ls_end = [
                self.x + 50 * (-self.speed * math.sin(rad)),
                self.y + 50 * (-self.speed * math.cos(rad))
            ]
            
            # Show lightspeed ship
            image = pygame.transform.rotate(ship_ls_img, self.direction)
            display.blit(image, (self.x, self.y))
            
            # Check collisions with path
            p_start = Point(self.ls_start[0], self.ls_start[1])
            p_end = Point(self.ls_end[0], self.ls_end[1])
            
            bool_hits = []
            for other in others:
                if other is None:
                    bool_hits.append(False)
                    continue
                p_other = Point(other.x, other.y)
                hit = lies_between(p_other, p_start, p_end) and \
                      (distance(p_end, p_other) < 100 or distance(p_start, p_other) < 100)
                bool_hits.append(hit)
            
            while len(bool_hits) < 3:
                bool_hits.append(False)
            
            self.alive = False
            return bool_hits
        return [False, False, False]
    
    def stop_lightspeed(self):
        """Stop lightspeed and restore ship"""
        if not self.alive and self.ls_alive:
            self.ls_alive = False
            self.alive = True
            self.x = self.ls_end[0]
            self.y = self.ls_end[1]
    
    def start_spacemine(self, frame_nr):
        """Create spacemine"""
        from entities.bullet import Spacemine
        return Spacemine(self.x, self.y, self.k_left, self.k_right, 
                        self.speed, self.player, frame_nr, True)
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, 30, 30)
