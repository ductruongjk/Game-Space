"""
Visual effects - Explosions and Powerups
"""
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Explode:
    """Explosion animation effect"""
    
    def __init__(self, x, y, explosion_sound=None, explosion_gif=None):
        self.x = x
        self.y = y
        self.last = pygame.time.get_ticks()
        self.duration = 1600  # 1.6 seconds
        self.animation = 0
        self.explosion_gif = explosion_gif
        
        # Play sound if provided
        if explosion_sound:
            explosion_sound.play()
    
    def update(self, display):
        """Update and draw explosion animation"""
        now = pygame.time.get_ticks()
        if now % 2 == 0:
            self.animation += 1
        if self.animation > 810:
            self.animation = 0
        
        if now - self.last <= self.duration:
            if self.x < SCREEN_WIDTH and self.y < SCREEN_HEIGHT and self.explosion_gif:
                frame_x = (self.animation % 9) * 1200 / 9
                frame_y = (self.animation // 9) * 1200 / 9
                display.blit(self.explosion_gif, (self.x - 50, self.y - 50),
                            pygame.Rect(frame_x, frame_y, 1200 / 9, 1200 / 9))
            return True  # Still active
        return False  # Finished
    
    def is_active(self):
        """Check if explosion is still running"""
        now = pygame.time.get_ticks()
        return now - self.last <= self.duration


class LukPowerup:
    """Lukas powerup - debuffs enemy ships when collected"""
    
    def __init__(self, x=None, y=None, powerup_img=None):
        self.x = x or 400
        self.y = y or 400
        self.alive = True
        self.powerup_img = powerup_img
    
    def update(self, display, frame):
        """Move powerup across screen"""
        if not self.alive:
            return
            
        if self.x > SCREEN_WIDTH:
            self.x = 0
        self.x += 0.8
        
        if self.powerup_img:
            display.blit(self.powerup_img, (self.x, self.y))
    
    def check_collision(self, ship_x, ship_y, ship_radius=20):
        """Check if ship collected powerup"""
        dx = self.x - ship_x
        dy = self.y - ship_y
        return (dx*dx + dy*dy) < (ship_radius + 20)**2
    
    def respawn(self):
        """Respawn powerup at random position"""
        import random
        self.x = random.choice(range(0, 10)) * 80
        self.y = random.choice(range(0, 10)) * 60
        self.alive = True
