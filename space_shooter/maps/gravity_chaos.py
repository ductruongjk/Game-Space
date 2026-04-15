"""
Map 2 - Gravity Chaos Zone
Features a central black hole that pulls both ships in
Floating asteroids orbit around, acting as obstacles and shields
"""
import pygame
import math
import random
from .base_map import BaseMap
from entities.obstacle import Asteroid, BlackHole
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED

class GravityChaosMap(BaseMap):
    """
    Gravity Chaos Zone - Chaotic and unpredictable
    - Black hole at center constantly pulls both ships in
    - Floating asteroids orbit around - obstacles and potential shields
    - Strategy: lure opponent into the pull while escaping
    """
    
    def __init__(self):
        super().__init__("Gravity Chaos Zone", 'resources/background.png')
        
        # Black hole at center
        self.black_hole = BlackHole(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50)
        
        # Create orbiting asteroids
        self.asteroids = []
        for i in range(8):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(150, 280)
            self.asteroids.append(Asteroid(
                x=self.black_hole.x + math.cos(angle) * dist,
                y=self.black_hole.y + math.sin(angle) * dist,
                vx=random.uniform(-0.8, 0.8),
                vy=random.uniform(-0.8, 0.8),
                radius=random.randint(18, 28)
            ))
        
        # Warning timer
        self.warning_active = False
        self.warning_timer = 0
    
    def update(self):
        """Update black hole and asteroids"""
        super().update()
        
        # Update black hole animation
        self.black_hole.update()
        
        # Update asteroids with slight gravity
        for asteroid in self.asteroids:
            asteroid.update(self.black_hole.x, self.black_hole.y, gravity=0.02)
    
    def draw(self, display, font=None):
        """Draw map with black hole and asteroids"""
        super().draw(display)
        
        # Draw black hole
        self.black_hole.draw(display)
        
        # Draw warning zone around black hole
        warning_radius = 120
        pygame.draw.circle(display, (255, 50, 50, 50), 
                         (int(self.black_hole.x), int(self.black_hole.y)), 
                         warning_radius, 2)
        
        # Draw danger text
        if font:
            warning = font.render("! DANGER ZONE !", True, RED)
            display.blit(warning, (SCREEN_WIDTH//2 - warning.get_width()//2, 80))
        
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(display)
    
    def apply_physics(self, ship):
        """Apply black hole gravity to ship"""
        being_consumed = self.black_hole.apply_gravity(ship)
        
        # If too close to black hole center, ship dies
        if being_consumed:
            return True  # Ship should die
        return False
    
    def check_collision(self, ship):
        """Check collision with asteroids"""
        for asteroid in self.asteroids:
            if asteroid.check_collision(ship.x, ship.y):
                return True
        return False
    
    def get_info_text(self):
        return "Gravity Chaos - Avoid the Black Hole!"
