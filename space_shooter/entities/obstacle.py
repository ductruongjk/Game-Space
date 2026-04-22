"""
Obstacles - Asteroids and Black Holes
"""
import pygame
import math
import random
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSET_BLACKHOLE, ASSET_ASTEROIDS_FOLDER

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def distance(A, B):
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)


class Asteroid:
    """Floating asteroid obstacle with image"""
    
    # Load asteroid images from the asteroids folder recursively
    asteroid_images = []
    try:
        if os.path.exists(ASSET_ASTEROIDS_FOLDER):
            for root, _, files in os.walk(ASSET_ASTEROIDS_FOLDER):
                for f in files:
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        try:
                            img = pygame.image.load(os.path.join(root, f))
                            asteroid_images.append(img)
                        except Exception:
                            pass
    except Exception as e:
        print(f"Warning: Could not load asteroid images: {e}")
    
    def __init__(self, x=None, y=None, vx=None, vy=None, radius=None):
        self.x = x or random.randint(50, SCREEN_WIDTH - 50)
        self.y = y or random.randint(50, SCREEN_HEIGHT - 50)
        self.vx = vx or random.uniform(-0.6, 0.6)  # Giảm tốc độ asteroid
        self.vy = vy or random.uniform(-0.6, 0.6)
        self.radius = radius or random.randint(15, 22)
        self.angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        
        # Select random asteroid image
        self.image = None
        self.mask = None
        if Asteroid.asteroid_images:
            orig_img = random.choice(Asteroid.asteroid_images)
            # Scale to radius
            size = self.radius * 2
            self.image = pygame.transform.scale(orig_img, (size, size))
            self.mask = pygame.mask.from_surface(self.image)
        
        # Fallback colors if no image
        self.color_base = (139, 125, 107)
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
        """Draw asteroid using image or fallback circle"""
        x, y = int(self.x), int(self.y)
        
        if self.image:
            # Rotate image
            rotated = pygame.transform.rotate(self.image, -self.angle)
            rect = rotated.get_rect(center=(x, y))
            display.blit(rotated, rect)
        else:
            # Fallback: draw circle
            r = self.radius
            pygame.draw.circle(display, self.color_base, (x, y), r)
            pygame.draw.circle(display, self.color_dark, (x, y), r - 3)
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
    """Black hole that pulls ships in with gravity - uses blackhole.png"""
    
    def __init__(self, x=None, y=None, radius=35):
        self.x = x or SCREEN_WIDTH // 2
        self.y = y or SCREEN_HEIGHT // 2
        self.radius = radius  # Moderate size (35-40 instead of 50)
        self.frame_count = 0
        self.gravity_strength = 0.3
        self.direction = 1  # 1 = pull, -1 = push
        
        # Load blackhole image
        self.image = None
        self.mask = None
        try:
            self.image = pygame.image.load(ASSET_BLACKHOLE)
            # Scale to radius
            size = self.radius * 2
            self.image = pygame.transform.scale(self.image, (size, size))
            self.mask = pygame.mask.from_surface(self.image)
        except:
            pass
        
        # Fallback colors if no image
        self.glow_color = (100, 0, 150)
        self.core_color = (0, 0, 0)
        self.ring_color = (150, 50, 200)
    
    def update(self):
        """Update animation"""
        self.frame_count += 1
    
    def apply_gravity(self, ship):
        """Apply gravity force to ship"""
        dx = self.x - ship.x
        dy = self.y - ship.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Chỉ hút trong phạm vi vòng tròn tím (radius * 2.5)
        gravity_range = self.radius * 2.5
        if dist > gravity_range:
            return False  # Ngoài phạm vi, không hút
        
        if dist < 10:
            dist = 10  # Prevent division by zero
        
        # F = k / distance^2, giảm hệ số để hút nhẹ hơn
        force = self.gravity_strength * 5000 / (dist * dist)
        if force > 2:
            force = 2
        
        # Apply in direction of black hole (or away if reversed)
        nx = dx / dist
        ny = dy / dist
        
        ship.x += nx * force * self.direction
        ship.y += ny * force * self.direction
        
        return dist < self.radius + 15  # Return True if ship is being consumed
    
    def draw(self, display):
        """Draw black hole using image or fallback circles"""
        if self.image:
            # Rotate image slowly
            rotation = (self.frame_count * 2) % 360
            rotated = pygame.transform.rotate(self.image, rotation)
            rect = rotated.get_rect(center=(int(self.x), int(self.y)))
            display.blit(rotated, rect)
        else:
            # Fallback: draw animated black hole with circles
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
