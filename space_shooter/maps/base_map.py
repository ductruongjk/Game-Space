"""
Base Map class - Foundation for all game maps
"""
import pygame
import math
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

class BaseMap:
    """Base class for all game maps"""
    
    def __init__(self, name, background_path):
        self.name = name
        self.frame_count = 0
        
        # Load background
        try:
            self.background = pygame.image.load(background_path)
        except:
            # Create default background if image not found
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)
            
            # Add some stars
            for _ in range(100):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                brightness = random.randint(100, 255)
                pygame.draw.circle(self.background, (brightness, brightness, brightness), (x, y), 1)
    
    def update(self):
        """Update map mechanics - called every frame"""
        self.frame_count += 1
    
    def draw(self, display, font=None):
        """Draw map background and elements"""
        # Draw background
        display.blit(self.background, (0, 0))
    
    def apply_physics(self, ship):
        """Apply map-specific physics to ship - override in subclasses"""
        pass
    
    def check_collision(self, ship):
        """Check ship collision with map elements - override in subclasses"""
        return False
    
    def get_info_text(self):
        """Get map information text"""
        return self.name
