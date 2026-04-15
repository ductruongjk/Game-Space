"""
Obstacles - Asteroids and Black Holes
"""
import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distance(A, B):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)


class Asteroid:
    """Floating asteroid obstacle"""
    
    def __init__(self, x=None, y=None, vx=None, vy=None, radius=None):
        self.x = x or random.randint(50, SCREEN_WIDTH - 50)
        self.y = y or random.randint(50, SCREEN_HEIGHT - 50)
        self.vx = vx or random.uniform(-1, 1)
        self.vy = vy or random.uniform(-1, 1)
        self.radius = radius or random.randint(15, 25)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        
        # Asteroid appearance
        self.color_base = (139, 125, 107)  # Brown-gray
        self.color_dark = (100, 90, 80)
        self.color_crater = (80, 70, 60)
    
    def update(self, black_hole_x=None, black_hole_y=None, gravity=0):
        """Move asteroid, optionally affected by gravity"""
        # Move
        self.x += self.vx
        self.y += self.vy
        self.angle += self.rotation_speed
        
        # Apply gravity if near black hole
        if black_hole_x is not None and gravity > 0:
            dx = black_hole_x - self.x
            dy = black_hole_y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                self.vx += (dx/dist) * gravity
                self.vy += (dy/dist) * gravity
        
        # Wrap around screen
        if self.x > SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT
    
    def draw(self, display):
        """Draw asteroid"""
        x, y = int(self.x), int(self.y)
        r = self.radius
        
        # Main body
        pygame.draw.circle(display, self.color_base, (x, y), r)
        pygame.draw.circle(display, self.color_dark, (x, y), r - 3)
        
        # Crater details
        pygame.draw.circle(display, self.color_crater, 
                         (x - r//3, y - r//3), r//4)
        pygame.draw.circle(display, self.color_crater, 
                         (x + r//4, y + r//4), r//5)
    
    def check_collision(self, ship_x, ship_y, ship_radius=15):
        """Check collision with ship"""
        center = Point(self.x, self.y)
        ship = Point(ship_x, ship_y)
        return distance(center, ship) < self.radius + ship_radius
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)


class BlackHole:
    """Black hole that pulls ships in with gravity"""
    
    def __init__(self, x=None, y=None, radius=50):
        self.x = x or SCREEN_WIDTH // 2
        self.y = y or SCREEN_HEIGHT // 2
        self.radius = radius
        self.frame_count = 0
        self.gravity_strength = 0.3
        self.direction = 1  # 1 = pull, -1 = push
        
        # Visual properties
        self.glow_color = (100, 0, 150)  # Purple
        self.core_color = (0, 0, 0)  # Black
        self.ring_color = (150, 50, 200)  # Purple-pink
    
    def update(self):
        """Update animation"""
        self.frame_count += 1
    
    def apply_gravity(self, ship):
        """Apply gravity force to ship"""
        dx = self.x - ship.x
        dy = self.y - ship.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < 10:
            dist = 10  # Prevent division by zero
        
        # F = k / distance^2
        force = self.gravity_strength * 10000 / (dist * dist)
        if force > 3:
            force = 3
        
        # Apply in direction of black hole (or away if reversed)
        nx = dx / dist
        ny = dy / dist
        
        ship.x += nx * force * self.direction
        ship.y += ny * force * self.direction
        
        return dist < self.radius + 20  # Return True if ship is being consumed
    
    def draw(self, display):
        """Draw animated black hole"""
        rotation = (self.frame_count * 2) % 360
        
        # Draw glow rings
        for i in range(5, 0, -1):
            radius = self.radius + i * 15
            alpha_color = (50 + i*20, 0, 100 + i*30)
            pygame.draw.circle(display, alpha_color, 
                             (int(self.x), int(self.y)), radius)
        
        # Draw center black hole
        pygame.draw.circle(display, self.core_color, 
                         (int(self.x), int(self.y)), self.radius)
        
        # Draw event horizon ring
        pygame.draw.circle(display, self.ring_color, 
                         (int(self.x), int(self.y)), self.radius, 3)
        
        # Draw spiral arms
        for arm in range(4):
            arm_angle = math.radians(rotation + arm * 90)
            start_x = self.x + math.cos(arm_angle) * 30
            start_y = self.y + math.sin(arm_angle) * 30
            end_x = self.x + math.cos(arm_angle) * 60
            end_y = self.y + math.sin(arm_angle) * 60
            pygame.draw.line(display, (150, 50, 200), 
                           (start_x, start_y), (end_x, end_y), 3)
    
    def draw_direction_indicator(self, display, font):
        """Draw gravity direction indicator (for reverse gravity map)"""
        arrow_color = (100, 255, 100) if self.direction == 1 else (255, 100, 100)
        arrow_text = "PULL" if self.direction == 1 else "PUSH"
        text = font.render(arrow_text, True, arrow_color)
        display.blit(text, (self.x - 20, self.y - 70))
