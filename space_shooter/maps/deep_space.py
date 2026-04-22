"""
Map 1 - Deep Space Arena
Classic space duel with scrolling starfield background
No obstacles - pure skill-based combat
"""
import pygame
import random
from .base_map import BaseMap
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE

class DeepSpaceMap(BaseMap):
    """
    Deep Space Arena - The classic tutorial map
    - Clean, balanced environment
    - Slow scrolling starfield creates space flying sensation
    - No obstacles - pure 1v1 skill combat
    """
    
    def __init__(self):
        super().__init__("Deep Space Arena", 'resources/background1600.png')
        
        # Starfield for parallax effect
        self.stars = []
        for _ in range(150):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.1, 0.5),  # Slow scroll
                'brightness': random.randint(150, 255),
                'size': random.choice([1, 1, 2])  # Mostly small stars
            })
        
        self.star_scroll = 0
    
    def update(self):
        """Update starfield animation"""
        super().update()
        
        # Scroll stars slowly
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, display, font=None):
        """Draw starfield background"""
        # Draw base background
        super().draw(display, font)

        # Draw scrolling stars on top for depth effect
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(display, color, 
                             (int(star['x']), int(star['y'])), 
                             star['size'])
    
    def get_info_text(self):
        """Map description"""
        return "Deep Space Arena - Pure Combat"
