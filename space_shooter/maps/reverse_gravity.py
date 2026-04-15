"""
Map 3 - Reverse Gravity Zone
Gravity reverses every 15 seconds - ships being pulled down suddenly get pulled up
Warning given 2-3 seconds before reversal
"""
import pygame
import math
import random
from .base_map import BaseMap
from entities.obstacle import Asteroid, BlackHole
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, YELLOW, RED, CYAN, ASSET_BACKGROUND_MAP3

class ReverseGravityMap(BaseMap):
    """
    Reverse Gravity Zone - Tense and rhythmic
    - Gravity reverses every 15 seconds
    - 2-3 second warning before reversal
    - Strategy: shoot when opponent loses control during reversal
    """
    
    def __init__(self):
        super().__init__("Reverse Gravity Zone", ASSET_BACKGROUND_MAP3)
        
        # Multiple moderate-sized black holes (smaller than original 50)
        self.black_holes = [
            BlackHole(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 35),  # Center
            BlackHole(SCREEN_WIDTH // 3, SCREEN_HEIGHT * 2 // 3, 30),  # Bottom left
            BlackHole(SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 3, 30),   # Top right
        ]
        
        # All black holes share the same direction (for simultaneous reversal)
        self.shared_direction = 1
        for bh in self.black_holes:
            bh.direction = self.shared_direction
        
        # Reverse gravity timer
        self.reverse_interval = 15 * 60  # 15 seconds at 60 FPS
        self.reverse_timer = self.reverse_interval
        self.warning_time = 3 * 60  # 3 second warning
        
        # Asteroids scattered around
        self.asteroids = []
        for i in range(10):
            self.asteroids.append(Asteroid(
                x=random.randint(50, SCREEN_WIDTH - 50),
                y=random.randint(50, SCREEN_HEIGHT - 50),
                vx=random.uniform(-0.5, 0.5),
                vy=random.uniform(-0.5, 0.5),
                radius=random.randint(16, 24)
            ))
    
    def update(self):
        """Update gravity reversal timer"""
        super().update()
        
        # Update timer
        self.reverse_timer -= 1
        
        # Reverse gravity when timer expires
        if self.reverse_timer <= 0:
            self.shared_direction *= -1  # Flip shared direction
            for bh in self.black_holes:
                bh.direction = self.shared_direction
            self.reverse_timer = self.reverse_interval
        
        # Update all black holes and asteroids
        for bh in self.black_holes:
            bh.update()
        for asteroid in self.asteroids:
            # Find nearest black hole for gravity
            nearest_bh = min(self.black_holes, 
                           key=lambda bh: math.hypot(bh.x - asteroid.x, bh.y - asteroid.y))
            asteroid.update(nearest_bh.x, nearest_bh.y, gravity=0.015)
    
    def draw(self, display, font=None):
        """Draw map with countdown timer"""
        super().draw(display)
        
        # Draw all black holes with direction indicator
        for bh in self.black_holes:
            bh.draw(display)
        
        # Draw countdown
        if font:
            seconds_left = self.reverse_timer // 60 + 1
            
            # Color based on time remaining
            if seconds_left <= 3:
                color = RED
                text = f"GRAVITY REVERSING IN: {seconds_left}!"
            elif seconds_left <= 7:
                color = YELLOW
                text = f"Gravity reversing in: {seconds_left}"
            else:
                color = GREEN
                text = f"Next reversal: {seconds_left}s"
            
            # Draw timer
            timer_text = font.render(text, True, color)
            display.blit(timer_text, (SCREEN_WIDTH//2 - timer_text.get_width()//2, 100))
            
            # Draw next state
            next_state = "PUSH (Pull In)" if self.shared_direction == 1 else "PUSH AWAY"
            next_color = GREEN if self.shared_direction == 1 else (100, 255, 255)
            next_text = font.render(f"Next: {next_state}", True, next_color)
            display.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 130))
            
            # Draw current state
            current = "PULLING IN" if self.shared_direction == 1 else "PUSHING OUT"
            curr_color = RED if self.shared_direction == 1 else CYAN
            curr_text = font.render(f"Current: {current}", True, curr_color)
            display.blit(curr_text, (SCREEN_WIDTH//2 - curr_text.get_width()//2, 30))
        
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(display)
    
    def apply_physics(self, ship):
        """Apply reversing gravity from all black holes to ship"""
        for bh in self.black_holes:
            being_consumed = bh.apply_gravity(ship)
            if being_consumed:
                return True
        return False
    
    def check_collision(self, ship):
        """Check collision with asteroids"""
        for asteroid in self.asteroids:
            if asteroid.check_collision(ship.x, ship.y):
                return True
        return False
    
    def is_reversing_soon(self):
        """Check if gravity is about to reverse (for AI timing)"""
        return self.reverse_timer < self.warning_time
    
    @property
    def gravity_reversed(self):
        """Property for compatibility with reverse_gravity check"""
        return self.shared_direction == -1
    
    def get_info_text(self):
        return "Reverse Gravity - Watch for the Flip!"
