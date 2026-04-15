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
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, ASSET_BACKGROUND_MAP2

class GravityChaosMap(BaseMap):
    """
    Gravity Chaos Zone - Chaotic and unpredictable
    - Black hole at center constantly pulls both ships in
    - Floating asteroids orbit around - obstacles and potential shields
    - Strategy: lure opponent into the pull while escaping
    """
    
    def __init__(self):
        super().__init__("Gravity Chaos Zone", ASSET_BACKGROUND_MAP2)
        
        # Multiple moderate-sized black holes (not too big)
        self.black_holes = [
            BlackHole(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 35),  # Center - medium
            BlackHole(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, 30),   # Top left - smaller
            BlackHole(SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT * 2 // 3, 30),  # Bottom right - smaller
        ]
        
        # Create asteroids scattered around the map
        self.asteroids = []
        for i in range(12):
            self.asteroids.append(Asteroid(
                x=random.randint(50, SCREEN_WIDTH - 50),
                y=random.randint(50, SCREEN_HEIGHT - 50),
                vx=random.uniform(-0.8, 0.8),
                vy=random.uniform(-0.8, 0.8),
                radius=random.randint(16, 24)
            ))
        
        # Warning timer
        self.warning_active = False
        self.warning_timer = 0
    
    def update(self):
        """Update black holes and asteroids"""
        super().update()
        
        # Update all black holes animation
        for bh in self.black_holes:
            bh.update()
        
        # Update asteroids with slight gravity from nearest black hole
        for asteroid in self.asteroids:
            # Find nearest black hole
            nearest_bh = min(self.black_holes, 
                           key=lambda bh: math.hypot(bh.x - asteroid.x, bh.y - asteroid.y))
            asteroid.update(nearest_bh.x, nearest_bh.y, gravity=0.02)
    
    def draw(self, display, font=None):
        """Draw map with black holes and asteroids"""
        super().draw(display)
        
        # Draw all black holes
        for bh in self.black_holes:
            bh.draw(display)
            # Draw warning zone around each black hole
            warning_radius = 80
            pygame.draw.circle(display, (255, 50, 50), 
                             (int(bh.x), int(bh.y)), 
                             warning_radius, 2)
        
        # Draw danger text
        if font:
            warning = font.render("! GRAVITY CHAOS !", True, RED)
            display.blit(warning, (SCREEN_WIDTH//2 - warning.get_width()//2, 80))
        
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(display)
    
    def apply_physics(self, ship):
        """Apply gravity from all black holes to ship"""
        for bh in self.black_holes:
            being_consumed = bh.apply_gravity(ship)
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
