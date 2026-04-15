"""
Player module - Ships, rockets, bullets, and AI
"""
import pygame
import math
import random
from settings import *

class Rocket:
    """Rocket projectile fired by ships"""
    def __init__(self, x, y, direction, exists, player, rocket_speed=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.exists = exists
        self.player = player
        self.rocket_speed = rocket_speed
        self.speed = 0.2 * rocket_speed + 0.5
        self.maxspeed = rocket_speed * 1.5
        
    def move(self, display, rocket_img):
        """Update rocket position"""
        if self.exists:
            if self.speed < self.maxspeed:
                self.speed = self.speed * 1.01 + 0.01 * self.rocket_speed
            # Wrap around screen
            if self.x > SCREEN_WIDTH:
                self.x = 0
            if self.x < 0:
                self.x = SCREEN_WIDTH
            if self.y > SCREEN_HEIGHT:
                self.y = 0
            if self.y < SCREEN_HEIGHT:
                pass
            if self.y < 0:
                self.y = SCREEN_HEIGHT
        else:
            self.x = self.y = SCREEN_WIDTH + 500
            self.speed = 0
            
        rad = self.direction * math.pi / 180
        self.x += -self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)
        
        if self.exists:
            image = pygame.transform.rotate(rocket_img, self.direction)
            display.blit(image, (self.x, self.y))
            
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, 25, 25)


class Ship:
    """Player/AI ship with movement, weapons and abilities"""
    def __init__(self, x, y, player, stats, ship_img, ship_ls_img):
        self.player = player
        self.x = random.choice(range(5, 9)) * x / 10
        self.y = random.choice(range(5, 9)) * y / 10
        
        # Stats from upgrade system [speed, maneuver, rocket_speed, money, superweapon]
        self.stats = stats
        self.speed = 0.7 * stats[0]
        self.maneuver = stats[1]
        self.rocket_speed = stats[2]
        self.superweapon = stats[4] if len(stats) > 4 else 1
        
        self.direction = 0
        self.k_left = self.k_right = 0
        self.hp = MAX_HP
        self.max_hp = MAX_HP
        self.alive = True
        
        # Images
        self.ship_img = ship_img
        self.ship_ls_img = ship_ls_img
        self.image = None
        
        # Lightspeed ability
        self.ls_start = [0, 0]
        self.ls_end = [0, 0]
        self.ls_alive = False
        self.ls_cooldown = 0
        
        # Respawn
        self.last = pygame.time.get_ticks()
        self.respawn_duration = 1600
        self.respawn_animation = 0
        self.respawn_running = True
        self.respawn_x = self.x
        self.respawn_y = self.y
        
        # AI attributes
        self.ai_last_shot = 0
        self.ai_shoot_cooldown = 60
        self.ai_target = None
        
    def respawn(self, display, respawn_gif):
        """Handle respawn animation"""
        self.alive = False
        now = pygame.time.get_ticks()
        if now % 2 == 0:
            self.respawn_animation += 1
        if now - self.last <= self.respawn_duration:
            frame_x = (self.respawn_animation % 9) * 100
            frame_y = (self.respawn_animation // 9) * 100
            display.blit(respawn_gif, (self.respawn_x - 50, self.respawn_y - 50),
                        pygame.Rect(frame_x, frame_y, 100, 100))
        else:
            self.respawn_running = False
            self.alive = True
            self.x = self.respawn_x
            self.y = self.respawn_y
            self.hp = self.max_hp
            
    def move(self, display, respawn_gif):
        """Update ship position and render"""
        if self.respawn_running:
            self.respawn(display, respawn_gif)
            return
            
        if self.alive and self.hp > 0:
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
            image = pygame.transform.rotate(self.ship_img, self.direction)
            self.image = image
            display.blit(image, (self.x, self.y))
        else:
            self.x = self.y = SCREEN_WIDTH * self.player
            
    def change_angle(self, direction):
        """Start/stop turning"""
        m = 0.6 * self.maneuver
        if direction == "LEFT":
            self.k_left += m
        elif direction == "RIGHT":
            self.k_right += -m
        elif direction == "LEFT2":
            self.k_left = max(0, self.k_left - m)
        elif direction == "RIGHT2":
            self.k_right = min(0, self.k_right + m)
            
    def take_damage(self, damage):
        """Take damage and check death"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return True
        return False
        
    def draw_hp_bar(self, display, x, y, width=60, height=8):
        """Draw health bar above ship"""
        # Background
        pygame.draw.rect(display, DARK_GRAY, (x, y, width, height))
        # Health
        hp_percent = self.hp / self.max_hp
        color = GREEN if hp_percent > 0.5 else YELLOW if hp_percent > 0.25 else RED
        pygame.draw.rect(display, color, (x, y, int(width * hp_percent), height))
        # Border
        pygame.draw.rect(display, WHITE, (x, y, width, height), 1)


class AIController:
    """AI logic for controlling enemy ship"""
    def __init__(self, ai_ship, player_ship):
        self.ai = ai_ship
        self.player = player_ship
        
    def update(self, frame_nr, rocket, frame_cd, sw_type):
        """Update AI decisions"""
        dx = self.player.x - self.ai.x
        dy = self.player.y - self.ai.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        angle_to_player = math.atan2(-dx, -dy) * 180 / math.pi
        if angle_to_player < 0:
            angle_to_player += 360
        angle_diff = (self.ai.direction - angle_to_player + 180) % 360 - 180
        
        # Turning logic
        should_turn_left = angle_diff > 10 and not (90 < angle_diff < 270)
        should_turn_right = angle_diff < -10 or (90 < angle_diff < 270)
        
        if should_turn_left:
            self.ai.change_angle("LEFT")
        elif should_turn_right:
            self.ai.change_angle("RIGHT")
            
        # Shooting
        new_rocket = rocket
        should_shoot = False
        if abs(angle_diff) < 20 and dist > 50:
            if frame_nr - self.ai.ai_last_shot > self.ai.ai_shoot_cooldown:
                should_shoot = True
                self.ai.ai_last_shot = frame_nr
                
        if should_shoot and not rocket.exists:
            new_rocket = Rocket(self.ai.x, self.ai.y, self.ai.direction, True, 
                              self.ai.player, self.ai.rocket_speed)
                              
        # Superweapon usage
        new_frame_cd = frame_cd
        if sw_type == SUPERWEAPON_LIGHTSPEED:
            if 100 < dist < 300 and abs(angle_diff) < 15:
                if frame_nr > frame_cd + 300 and self.ai.alive:
                    # Lightspeed attack
                    new_frame_cd = frame_nr
        elif sw_type == SUPERWEAPON_SPACEMINE:
            if frame_nr > frame_cd + 300:
                if dist < 150:
                    new_frame_cd = frame_nr
                    
        return new_rocket, new_frame_cd, should_shoot
