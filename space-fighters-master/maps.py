"""
Maps module - Different game arenas with physics
"""
import pygame
import math
import random
from settings import *

class BaseMap:
    """Base class for all game maps"""
    def __init__(self, name, background_path):
        self.name = name
        self.frame_count = 0
        self.asteroids = []
        
        # Load background
        try:
            self.background = pygame.image.load(background_path)
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)
            # Add stars
            for _ in range(100):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                brightness = random.randint(100, 255)
                pygame.draw.circle(self.background, (brightness, brightness, brightness), (x, y), 1)
                
    def update(self):
        """Update map mechanics"""
        self.frame_count += 1
        
    def draw(self, display):
        """Draw map background"""
        display.blit(self.background, (0, 0))
        
    def apply_physics(self, ship):
        """Apply map physics to ship - override in subclasses"""
        pass
        
    def check_asteroid_collision(self, obj_x, obj_y, obj_radius=15):
        """Check collision with asteroids"""
        return False
        
    def draw_asteroids(self, display):
        """Draw asteroid obstacles"""
        for asteroid in self.asteroids:
            x, y = int(asteroid['x']), int(asteroid['y'])
            r = asteroid['radius']
            pygame.draw.circle(display, (139, 125, 107), (x, y), r)
            pygame.draw.circle(display, (100, 90, 80), (x, y), r - 3)


class DeepSpaceMap(BaseMap):
    """Map 1: Simple open space, no obstacles"""
    def __init__(self):
        super().__init__(MAP_DEEP_SPACE, ASSET_BG_1600)
        
    def get_info(self):
        return "Deep Space Arena - Pure Combat"


class GravityChaosMap(BaseMap):
    """Map 2: Black hole gravity + asteroids"""
    def __init__(self):
        super().__init__(MAP_GRAVITY_CHAOS, ASSET_BG)
        self.black_hole_x = SCREEN_WIDTH // 2
        self.black_hole_y = SCREEN_HEIGHT // 2
        self.black_hole_radius = BLACK_HOLE_RADIUS
        
        # Create asteroids
        for i in range(6):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(150, 250)
            self.asteroids.append({
                'x': self.black_hole_x + math.cos(angle) * dist,
                'y': self.black_hole_y + math.sin(angle) * dist,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'radius': random.randint(20, 35)
            })
            
    def update(self):
        """Update asteroids"""
        super().update()
        for a in self.asteroids:
            a['x'] += a['vx']
            a['y'] += a['vy']
            # Wrap around
            if a['x'] > SCREEN_WIDTH: a['x'] = 0
            elif a['x'] < 0: a['x'] = SCREEN_WIDTH
            if a['y'] > SCREEN_HEIGHT: a['y'] = 0
            elif a['y'] < 0: a['y'] = SCREEN_HEIGHT
            
    def apply_physics(self, ship):
        """Apply black hole gravity (only within range)"""
        dx = self.black_hole_x - ship.x
        dy = self.black_hole_y - ship.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        # Only affect if within range
        if dist < BLACK_HOLE_MAX_DIST and dist > 10:
            force = BLACK_HOLE_K * 100 / dist
            force = min(force, 3.0)  # Cap max force
            nx = dx / dist
            ny = dy / dist
            ship.x += nx * force
            ship.y += ny * force
            
    def check_asteroid_collision(self, obj_x, obj_y, obj_radius=15):
        """Check if object hits asteroid"""
        for a in self.asteroids:
            dx = obj_x - a['x']
            dy = obj_y - a['y']
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < a['radius'] + obj_radius:
                return True
        return False
        
    def draw(self, display):
        """Draw map with black hole and asteroids"""
        super().draw(display)
        
        # Draw black hole
        rotation = (self.frame_count * 2) % 360
        for i in range(5, 0, -1):
            radius = self.black_hole_radius + i * 15
            color = (50 + i*20, 0, 100 + i*30)
            pygame.draw.circle(display, color, 
                             (int(self.black_hole_x), int(self.black_hole_y)), radius)
        pygame.draw.circle(display, BLACK, 
                         (int(self.black_hole_x), int(self.black_hole_y)), 
                         self.black_hole_radius)
        pygame.draw.circle(display, (100, 0, 150), 
                         (int(self.black_hole_x), int(self.black_hole_y)), 
                         self.black_hole_radius, 3)
        
        # Draw danger zone indicator
        pygame.draw.circle(display, (255, 50, 50), 
                         (int(self.black_hole_x), int(self.black_hole_y)), 
                         BLACK_HOLE_MAX_DIST, 1)
        
        # Warning text
        text = FONT_SMALL.render("DANGER ZONE", True, RED)
        display.blit(text, (self.black_hole_x - 40, self.black_hole_y - BLACK_HOLE_MAX_DIST - 20))
        
        self.draw_asteroids(display)
        
    def get_info(self):
        return "Gravity Chaos - Avoid the Black Hole!"


class ReverseGravityMap(BaseMap):
    """Map 3: Controls reverse every 15 seconds"""
    def __init__(self):
        super().__init__(MAP_REVERSE_GRAVITY, ASSET_BG)
        self.reverse_timer = REVERSE_INTERVAL
        self.gravity_reversed = False
        self.black_hole_x = SCREEN_WIDTH // 2
        self.black_hole_y = SCREEN_HEIGHT // 2
        
    def update(self):
        """Update reverse timer"""
        super().update()
        self.reverse_timer -= 1/FPS
        if self.reverse_timer <= 0:
            self.reverse_timer = REVERSE_INTERVAL
            self.gravity_reversed = not self.gravity_reversed
            
    def apply_physics(self, ship):
        """Pull toward center (weaker than chaos map)"""
        dx = self.black_hole_x - ship.x
        dy = self.black_hole_y - ship.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 200 and dist > 10:
            force = 0.3 * 100 / dist
            force = min(force, 1.5)
            nx = dx / dist
            ny = dy / dist
            ship.x += nx * force
            ship.y += ny * force
            
    def draw(self, display):
        """Draw with reverse timer"""
        super().draw(display)
        
        # Draw center indicator
        color = RED if self.gravity_reversed else GREEN
        pygame.draw.circle(display, color, 
                         (int(self.black_hole_x), int(self.black_hole_y)), 30)
        
        # Timer text
        seconds_left = int(self.reverse_timer)
        state = "REVERSED" if self.gravity_reversed else "NORMAL"
        timer_text = FONT_MED.render(f"Controls: {state} ({seconds_left}s)", True, color)
        display.blit(timer_text, (SCREEN_WIDTH//2 - timer_text.get_width()//2, 50))
        
    def get_info(self):
        return "Reverse Gravity - Watch for the Flip!"
