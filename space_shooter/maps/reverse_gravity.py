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
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, YELLOW, RED, CYAN

class ReverseGravityMap(BaseMap):
    """
    Reverse Gravity Zone - Tense and rhythmic
    - Gravity reverses every 15 seconds
    - 2-3 second warning before reversal
    - Strategy: shoot when opponent loses control during reversal
    """
    
    def __init__(self):
        super().__init__("Reverse Gravity Zone", 'resources/backgroundmap3.png')
        
        # Black hole at center
        self.black_hole = BlackHole(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50)
        
        # Reverse gravity timer
        self.reverse_interval = 15 * 60  # 15 seconds at 60 FPS
        self.reverse_timer = self.reverse_interval
        self.warning_time = 3 * 60  # 3 second warning
        
        # Asteroids (same as chaos but behave differently with reverse gravity)
        self.asteroids = []
        for i in range(6):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(180, 300)
            self.asteroids.append(Asteroid(
                x=self.black_hole.x + math.cos(angle) * dist,
                y=self.black_hole.y + math.sin(angle) * dist,
                vx=random.uniform(-0.5, 0.5),
                vy=random.uniform(-0.5, 0.5),
                radius=random.randint(20, 30)
            ))
    
    def update(self):
        """Update gravity reversal timer"""
        super().update()
        
        # Update timer
        self.reverse_timer -= 1
        
        # Reverse gravity when timer expires
        if self.reverse_timer <= 0:
            self.black_hole.direction *= -1  # Flip gravity
            self.reverse_timer = self.reverse_interval
        
        # Update black hole and asteroids
        self.black_hole.update()
        for asteroid in self.asteroids:
            asteroid.update(self.black_hole.x, self.black_hole.y, gravity=0.015)
    
    def draw(self, display, font=None):
        """Draw map with countdown timer"""
        super().draw(display)
        
        # Draw black hole with direction indicator
        self.black_hole.draw(display)
        
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
            next_state = "PUSH (Pull In)" if self.black_hole.direction == 1 else "PUSH AWAY"
            next_color = GREEN if self.black_hole.direction == 1 else (100, 255, 255)
            next_text = font.render(f"Next: {next_state}", True, next_color)
            display.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 130))
            
            # Draw current state
            current = "PULLING IN" if self.black_hole.direction == 1 else "PUSHING OUT"
            curr_color = RED if self.black_hole.direction == 1 else CYAN
            curr_text = font.render(f"Current: {current}", True, curr_color)
            display.blit(curr_text, (SCREEN_WIDTH//2 - curr_text.get_width()//2, 30))
        
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(display)
    
    def apply_physics(self, ship):
        """Apply reversing gravity to ship"""
        being_consumed = self.black_hole.apply_gravity(ship)
        
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
    
    def get_info_text(self):
        return "Reverse Gravity - Watch for the Flip!"
