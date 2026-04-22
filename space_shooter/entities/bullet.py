"""
Bullet/Rocket and Spacemine entities
"""
import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Point:
    """Point for collision calculations"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distance(A, B):
    """Calculate distance between two points"""
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

def lies_between(x, y, z):
    """Check if point x lies between points y and z"""
    a = distance(y, z)
    b = distance(z, x)
    c = distance(x, y)
    return a**2 + b**2 >= c**2 and a**2 + c**2 >= b**2


class Rocket:
    """Rocket projectile fired by ships"""
    
    def __init__(self, x, y, direction, exists, player, rocketspeed=1):
        self.x = x
        self.y = y
        self.direction = direction
        self.exists = exists
        self.player = player
        self.rocketspeed = rocketspeed
        self.speed = 0.2 * rocketspeed + 0.5
        self.maxspeed = rocketspeed * 1.5
    
    def move(self, display, rocket_img):
        """Update rocket position"""
        if self.exists:
            if self.speed < self.maxspeed:
                self.speed = self.speed * 1.01 + 0.01 * self.rocketspeed
            
            # Wrap around screen
            if self.x > SCREEN_WIDTH:
                self.x = 0
            if self.x < 0:
                self.x = SCREEN_WIDTH
            if self.y > SCREEN_HEIGHT:
                self.y = 0
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


class Spacemine:
    """Spacemine projectile - grows over time then explodes"""
    
    def __init__(self, x, y, left, right, speed, player, now, alive):
        self.x = x
        self.y = y
        self.direction = left + right
        self.alive = alive
        self.speed = 0.2 * speed
        self.player = player
        self.radius = 20
        self.last = pygame.time.get_ticks()
        self.duration = 16000  # 16 seconds
        self.hasexploded = False
    
    def update(self, display, ship_sm_img):
        """Update spacemine - moves slowly and grows"""
        if not self.alive:
            return
            
        now = pygame.time.get_ticks()
        rad = self.direction * math.pi / 180
        self.x += -self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)
        
        # Wrap around
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = SCREEN_WIDTH
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        
        # Draw mine with growing animation
        elapsed = now - self.last
        stages = [
            (self.duration - 6000, 40, 30),
            (self.duration - 5000, 43, 33),
            (self.duration - 4000, 46, 36),
            (self.duration - 3000, 49, 39),
            (self.duration - 2000, 52, 42),
            (self.duration - 1000, 57, 46),
            (self.duration, 63, 52)
        ]
        
        for threshold, size, radius in stages:
            if elapsed <= threshold:
                display.blit(pygame.transform.scale(ship_sm_img, (size, size)), (self.x, self.y))
                self.radius = radius
                return
        
        # Time expired
        self.alive = False
    
    def get_center(self):
        """Get center point for collision"""
        return Point(self.x + self.radius, self.y + self.radius)
    
    def check_collision(self, target_x, target_y):
        """Check if mine collides with target point"""
        center = self.get_center()
        target = Point(target_x, target_y)
        return distance(center, target) < self.radius + 20
