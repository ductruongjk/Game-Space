#!/usr/bin/env python
"""
Space Fighters - PvP and PvE Mode
- PvP: Player vs Player (2 players)
- PvE: Player vs AI (1 player vs computer)
"""
import sys
import pygame
import math
import random
import time
from pygame.locals import *

# INITIALIZE
SCREENWIDTH = 800
SCREENHEIGHT = 600

pygame.init()
WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("SpaceFighters")
pygame.display.set_icon(pygame.image.load('resources/ship1big.png'))
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(0)
pygame.key.set_repeat(1, 10)

# Virtual surface for scaling
VIRTUAL_SURF = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
DISPLAY = VIRTUAL_SURF  # All drawing goes to virtual surface
WINDOW_WIDTH = SCREENWIDTH
WINDOW_HEIGHT = SCREENHEIGHT

def scale_display():
    """Scale virtual surface to window size"""
    global WINDOW, VIRTUAL_SURF, WINDOW_WIDTH, WINDOW_HEIGHT
    scaled = pygame.transform.smoothscale(VIRTUAL_SURF, (WINDOW_WIDTH, WINDOW_HEIGHT))
    WINDOW.blit(scaled, (0, 0))
    pygame.display.update()

def handle_resize(event):
    """Handle window resize event"""
    global WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

# SOUNDS
pygame.mixer.music.load("resources/bg_music.mp3")
missileSound = pygame.mixer.Sound('resources/missile.wav')
explosionSound = pygame.mixer.Sound('resources/explosion.wav')

# CONSTANTS
PLAYERS = 2
GAME_MODE = "PVP"  # "PVP" or "PVE"
SELECTED_MAP = "Deep Space Arena"  # Default map
PLAYER1_NAME = "Player 1"  # Default player 1 name
PLAYER2_NAME = "Player 2"  # Default player 2 name (or "AI")

# MAP MECHANICS
class MapManager:
    """Manages map-specific mechanics"""
    def __init__(self, map_name):
        self.name = map_name
        self.frame_count = 0
        self.black_hole_x = SCREENWIDTH // 2
        self.black_hole_y = SCREENHEIGHT // 2
        self.black_hole_radius = 50
        self.gravity_strength = 0.3  # Base gravity strength
        self.gravity_direction = 1  # 1 = pull (hút), -1 = push (đẩy)
        self.reverse_timer = 0
        self.reverse_interval = 14 * 60  # 14 seconds at 60 FPS
        self.asteroids = []
        
        if map_name == "Gravity Chaos Zone":
            self.init_gravity_chaos()
        elif map_name == "Reverse Gravity Zone":
            self.init_reverse_gravity()
    
    def init_gravity_chaos(self):
        """Initialize Gravity Chaos Zone with asteroids"""
        # Create random asteroids
        for i in range(8):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.randint(150, 250)
            self.asteroids.append({
                'x': self.black_hole_x + math.cos(angle) * dist,
                'y': self.black_hole_y + math.sin(angle) * dist,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'radius': random.randint(15, 25),
                'angle': random.uniform(0, 360)
            })
    
    def init_reverse_gravity(self):
        """Initialize Reverse Gravity Zone"""
        # Same as chaos but with reverse mechanic
        self.init_gravity_chaos()
        self.reverse_timer = self.reverse_interval
    
    def apply_gravity(self, ship):
        """Apply gravity force to ship"""
        if self.name == "Deep Space Arena":
            return  # No gravity in map 1
        
        dx = self.black_hole_x - ship.x
        dy = self.black_hole_y - ship.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 10:
            distance = 10  # Prevent division by zero
        
        # Calculate gravity force: F = k / distance²
        force = self.gravity_strength * 10000 / (distance * distance)
        
        # Cap max force
        if force > 3:
            force = 3
        
        # Apply direction based on gravity_direction
        # gravity_direction = 1: pull toward center
        # gravity_direction = -1: push away from center
        direction_multiplier = self.gravity_direction
        
        # Normalize direction vector
        nx = dx / distance
        ny = dy / distance
        
        # Apply force
        ship.x += nx * force * direction_multiplier
        ship.y += ny * force * direction_multiplier
    
    def update(self):
        """Update map mechanics each frame"""
        self.frame_count += 1
        
        # Update reverse gravity timer
        if self.name == "Reverse Gravity Zone":
            self.reverse_timer -= 1
            if self.reverse_timer <= 0:
                # Reverse gravity
                self.gravity_direction *= -1
                self.reverse_timer = self.reverse_interval
        
        # Update asteroids
        if self.name in ["Gravity Chaos Zone", "Reverse Gravity Zone"]:
            for asteroid in self.asteroids:
                # Move asteroid
                asteroid['x'] += asteroid['vx']
                asteroid['y'] += asteroid['vy']
                asteroid['angle'] += 1
                
                # Apply slight gravity to asteroids
                dx = self.black_hole_x - asteroid['x']
                dy = self.black_hole_y - asteroid['y']
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    asteroid['vx'] += (dx/dist) * 0.05
                    asteroid['vy'] += (dy/dist) * 0.05
                
                # Wrap around screen
                if asteroid['x'] > SCREENWIDTH:
                    asteroid['x'] = 0
                elif asteroid['x'] < 0:
                    asteroid['x'] = SCREENWIDTH
                if asteroid['y'] > SCREENHEIGHT:
                    asteroid['y'] = 0
                elif asteroid['y'] < 0:
                    asteroid['y'] = SCREENHEIGHT
    
    def draw(self, display):
        """Draw map-specific elements"""
        if self.name == "Deep Space Arena":
            return  # No special elements
        
        # Draw black hole for Map 2 and 3
        if self.name in ["Gravity Chaos Zone", "Reverse Gravity Zone"]:
            self.draw_black_hole(display)
            self.draw_asteroids(display)
            
            # Draw reverse gravity timer for Map 3
            if self.name == "Reverse Gravity Zone":
                self.draw_reverse_timer(display)
    
    def draw_black_hole(self, display):
        """Draw animated black hole"""
        # Animation rotation
        rotation = (self.frame_count * 2) % 360
        
        # Draw swirling effect (multiple circles)
        for i in range(5, 0, -1):
            radius = self.black_hole_radius + i * 15
            alpha = int(100 / i)
            color = (50 + i*20, 0, 100 + i*30)  # Purple glow
            
            # Draw glow circle
            pygame.draw.circle(display, color, 
                             (int(self.black_hole_x), int(self.black_hole_y)), 
                             radius)
        
        # Draw center black hole
        pygame.draw.circle(display, (0, 0, 0), 
                         (int(self.black_hole_x), int(self.black_hole_y)), 
                         self.black_hole_radius)
        
        # Draw event horizon ring
        pygame.draw.circle(display, (100, 0, 150), 
                         (int(self.black_hole_x), int(self.black_hole_y)), 
                         self.black_hole_radius, 3)
        
        # Draw spiral arms
        for arm in range(4):
            arm_angle = math.radians(rotation + arm * 90)
            start_x = self.black_hole_x + math.cos(arm_angle) * 30
            start_y = self.black_hole_y + math.sin(arm_angle) * 30
            end_x = self.black_hole_x + math.cos(arm_angle) * 60
            end_y = self.black_hole_y + math.sin(arm_angle) * 60
            pygame.draw.line(display, (150, 50, 200), 
                           (start_x, start_y), (end_x, end_y), 3)
        
        # Draw gravity direction indicator
        if self.name == "Reverse Gravity Zone":
            # Draw arrows showing current gravity direction
            arrow_color = (100, 255, 100) if self.gravity_direction == 1 else (255, 100, 100)
            arrow_text = "PULL" if self.gravity_direction == 1 else "PUSH"
            font = pygame.font.Font('font.ttf', 12)
            text = font.render(arrow_text, True, arrow_color)
            display.blit(text, (self.black_hole_x - 20, self.black_hole_y - 70))
    
    def draw_asteroids(self, display):
        """Draw asteroids"""
        for asteroid in self.asteroids:
            x, y = int(asteroid['x']), int(asteroid['y'])
            radius = asteroid['radius']
            
            # Draw asteroid body
            pygame.draw.circle(display, (139, 125, 107), (x, y), radius)
            pygame.draw.circle(display, (100, 90, 80), (x, y), radius - 3)
            
            # Draw crater details
            pygame.draw.circle(display, (80, 70, 60), 
                             (x - radius//3, y - radius//3), radius//4)
    
    def draw_reverse_timer(self, display):
        """Draw reverse gravity countdown timer"""
        seconds_left = self.reverse_timer // 60 + 1
        
        # Warning color if time is running low
        if seconds_left <= 3:
            color = (255, 50, 50)  # Red warning
        elif seconds_left <= 7:
            color = (255, 200, 50)  # Yellow caution
        else:
            color = (100, 255, 100)  # Green normal
        
        font = pygame.font.Font('font.ttf', 20)
        text = font.render(f"GRAVITY REVERSING IN: {seconds_left}s", True, color)
        display.blit(text, (SCREENWIDTH//2 - text.get_width()//2, 100))
        
        # Draw next gravity indicator
        next_state = "PUSH" if self.gravity_direction == 1 else "PULL"
        next_text = font.render(f"Next: {next_state}", True, color)
        display.blit(next_text, (SCREENWIDTH//2 - next_text.get_width()//2, 130))


# Global map manager (initialized in main)
map_manager = None

# Fonts
SPACEFONT = pygame.font.Font('resources/space.ttf', 34)
BIGFONT = pygame.font.Font('font.ttf', 30)
FONT = pygame.font.Font('font.ttf', 16)
SMALLFONT = pygame.font.Font('font.ttf', 9)

# TEXTURES
BACKGROUND = pygame.image.load('resources/background1600.png')
SHIP1 = pygame.image.load('resources/ship1.png')
SHIP2 = pygame.image.load('resources/ship2.png')
ROCKET1 = pygame.image.load('resources/rocket1.png')
ROCKET2 = pygame.image.load('resources/rocket2.png')
ENDGAME = pygame.image.load('resources/endgamescreen1600.png')
LUKASPOWERUP = pygame.image.load('resources/lukas_powerup.png')
EXPLOSION_GIF_BIG = pygame.image.load('resources/explosion_anim_1200x1200.png')
RESPAWN_GIF = pygame.image.load('resources/respawn_anim_900x900_test.png')

# TEXTURES SUPERWEAPONS
SHIP1_LS = pygame.image.load('resources/ship1_lightspeed.png')
SHIP1_SM = pygame.image.load('resources/spacemine1.png')
SHIP2_LS = pygame.image.load('resources/ship2_lightspeed.png')
SHIP2_SM = pygame.image.load('resources/spacemine2.png')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 115, 175)
RED = (176, 52, 52)
GREEN = (84, 155, 70)
ORANGE = (255, 150, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
CYAN_DARK = (0, 150, 200)
BLUE_GLOW = (0, 150, 255)
RED_GLOW = (255, 100, 100)

# Global stats arrays (initialized in main)
shipspeed = [1, 1]
maneuv = [1, 1]
rocketspeed = [1, 1]
superweapon = [1, 1]


def load_stats(player_nr):
    """Load player stats from file"""
    try:
        high_score_file = open(f"stats{player_nr}.txt", "r")
        stats = high_score_file.read()
        high_score_file.close()
        return stats
    except (IOError, ValueError):
        return "[1,1,1,1000,1]"


def save_stats(player_nr, stats_list):
    """Save player stats to file"""
    try:
        high_score_file = open(f"stats{player_nr}.txt", "w")
        high_score_file.write(str(stats_list))
        high_score_file.close()
    except IOError:
        print("Unable to save stats.")


def lies_between(x, y, z):
    """Check if point x lies between points y and z"""
    a = distance(y, z)
    b = distance(z, x)
    c = distance(x, y)
    return a**2 + b**2 >= c**2 and a**2 + c**2 >= b**2


def distance(A, B):
    """Calculate distance between two points"""
    return math.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ship:
    """Player ship class"""
    def __init__(self, x, y, player):
        self.player = player
        self.x = random.choice(range(5, 9)) * x / 10
        self.y = random.choice(range(5, 9)) * y / 10
        self.speed = 0.7 * shipspeed[player - 1]
        self.direction = 0
        self.k_left = self.k_right = 0
        self.lukas = False
        self.boolean = False
        self.direc = ""
        self.alive = True
        self.ls_start = [0, 0]
        self.ls_end = [0, 0]
        self.ls_alive = False
        self.last = pygame.time.get_ticks()
        self.respawn_duration = 1600
        self.respawn_animation = 0
        self.respawn_running = True
        self.respawn_x = self.x
        self.respawn_y = self.y
        # AI-specific attributes
        self.ai_target = None
        self.ai_last_shot = 0
        self.ai_shoot_cooldown = 60  # Frames between shots
        self.ai_move_timer = 0
        self.ai_avoiding = False

    def respawn(self):
        """Handle respawn animation"""
        self.alive = False
        now = pygame.time.get_ticks()
        if now % 2 == 0:
            self.respawn_animation += 1
        if now - self.last <= self.respawn_duration:
            DISPLAY.blit(RESPAWN_GIF, (self.respawn_x - 50, self.respawn_y - 50),
                         pygame.Rect((self.respawn_animation % 9) * 900 / 9,
                                     (self.respawn_animation // 9) * 900 / 9,
                                     900 / 9, 900 / 9))
        else:
            self.respawn_running = False
            self.alive = True
            self.x = self.respawn_x
            self.y = self.respawn_y

    def move(self):
        """Update ship position and render"""
        if self.respawn_running and self.player <= PLAYERS:
            self.respawn()

        if self.alive:
            self.direction = 0
            self.direction += (self.k_left + self.k_right)

            rad = self.direction * math.pi / 180
            self.x += -self.speed * math.sin(rad)
            self.y += -self.speed * math.cos(rad)

            # Wrap around screen
            if self.x > SCREENWIDTH:
                self.x = 0
            if self.x < 0:
                self.x = SCREENWIDTH
            if self.y > SCREENHEIGHT:
                self.y = 0
            if self.y < 0:
                self.y = SCREENHEIGHT

            # Render ship
            if self.player == 1:
                image = pygame.transform.rotate(SHIP1, self.direction)
            else:
                image = pygame.transform.rotate(SHIP2, self.direction)
            self.image = image
            DISPLAY.blit(image, (self.x, self.y))
            rad = 0
        else:
            self.x = self.y = SCREENWIDTH * self.player

    def change_angle(self, direc, luka):
        """Start turning"""
        if direc == "LEFT":
            self.boolean = True
            self.direc = "LEFT"
        if direc == "RIGHT":
            self.boolean = True
            self.direc = "RIGHT"
        if direc == "LEFT2":
            self.boolean = False
            self.direc = "LEFT2"
        if direc == "RIGHT2":
            self.boolean = False
            self.direc = "RIGHT2"

    def change_angle2(self):
        """Update turning"""
        m = 0.6 * maneuv[self.player - 1]
        if self.direc == "LEFT" and self.boolean:
            if not self.lukas:
                self.k_left += m
            else:
                self.k_right += -m
        if self.direc == "RIGHT" and self.boolean:
            if not self.lukas:
                self.k_right += -m
            else:
                self.k_left += m

    def start_lightspeed(self, other1, other2=None, other3=None) -> list:
        """Activate lightspeed superweapon"""
        if self.alive:
            self.ls_alive = True
            self.ls_start = [self.x, self.y]
            rad = self.direction * math.pi / 180
            self.ls_end = [
                self.x + 50 * (-self.speed * math.sin(rad)),
                self.y + 50 * (-self.speed * math.cos(rad))
            ]
            
            if self.player == 1:
                image = pygame.transform.rotate(SHIP1_LS, self.direction)
            else:
                image = pygame.transform.rotate(SHIP2_LS, self.direction)
            DISPLAY.blit(image, (self.x, self.y))

            # Check collisions
            p_start = Point(self.ls_start[0], self.ls_start[1])
            p_end = Point(self.ls_end[0], self.ls_end[1])
            
            bool_hits = []
            others = [o for o in [other1, other2, other3] if o is not None]
            
            for other in others:
                p_other = Point(other.x, other.y)
                hit = lies_between(p_other, p_start, p_end) and \
                      (distance(p_end, p_other) < 100 or distance(p_start, p_other) < 100)
                bool_hits.append(hit)
            
            # Pad with False to ensure 3 elements
            while len(bool_hits) < 3:
                bool_hits.append(False)
                
            self.alive = False
            return bool_hits
        return [False, False, False]

    def stop_lightspeed(self):
        """Stop lightspeed"""
        if not self.alive and self.ls_alive:
            self.ls_alive = False
            self.alive = True
            self.x = self.ls_end[0]
            self.y = self.ls_end[1]
            if self.player == 1:
                image = pygame.transform.rotate(SHIP1_LS, self.direction)
            else:
                image = pygame.transform.rotate(SHIP2_LS, self.direction)
            DISPLAY.blit(image, (self.x, self.y))

    def start_spacemine(self, frame_nr):
        """Create spacemine"""
        return Spacemine(self.x, self.y, self.k_left, self.k_right, self.speed, self.player, frame_nr, True)


class Spacemine:
    """Spacemine projectile"""
    def __init__(self, x, y, left, right, speed, player, now, alive):
        self.x = x
        self.y = y
        self.direction = left + right
        self.alive = alive
        self.speed = 0.2 * speed
        self.player = player
        self.radius = 20
        self.last = pygame.time.get_ticks()
        self.duration = 16000
        self.hasexploded = False

    def update(self):
        """Update spacemine"""
        if self.alive:
            now = pygame.time.get_ticks()
            rad = self.direction * math.pi / 180
            self.x += -self.speed * math.sin(rad)
            self.y += -self.speed * math.cos(rad)
            
            # Wrap around
            if self.x > SCREENWIDTH:
                self.x = 0
            if self.x < 0:
                self.x = SCREENWIDTH
            if self.y > SCREENHEIGHT:
                self.y = 0
            if self.y < 0:
                self.y = SCREENHEIGHT
                
            if self.player == 1:
                m_color = SHIP1_SM
            else:
                m_color = SHIP2_SM

            elapsed = now - self.last
            if elapsed <= self.duration - 6000:
                DISPLAY.blit(pygame.transform.scale(m_color, (40, 40)), (self.x, self.y))
                self.radius = 30
            elif elapsed <= self.duration - 5000:
                DISPLAY.blit(pygame.transform.scale(m_color, (43, 43)), (self.x, self.y))
                self.radius = 33
            elif elapsed <= self.duration - 4000:
                DISPLAY.blit(pygame.transform.scale(m_color, (46, 46)), (self.x, self.y))
                self.radius = 36
            elif elapsed <= self.duration - 3000:
                DISPLAY.blit(pygame.transform.scale(m_color, (49, 49)), (self.x, self.y))
                self.radius = 39
            elif elapsed <= self.duration - 2000:
                DISPLAY.blit(pygame.transform.scale(m_color, (52, 52)), (self.x, self.y))
                self.radius = 42
            elif elapsed <= self.duration - 1000:
                DISPLAY.blit(pygame.transform.scale(m_color, (57, 57)), (self.x, self.y))
                self.radius = 46
            elif elapsed <= self.duration:
                DISPLAY.blit(pygame.transform.scale(m_color, (63, 63)), (self.x, self.y))
                self.radius = 52
            else:
                self.alive = False


class Rocket:
    """Rocket projectile"""
    def __init__(self, x, y, direction, exists, player):
        self.x = x
        self.y = y
        self.direction = direction
        self.exists = exists
        self.player = player
        self.speed = 0.2 * rocketspeed[player - 1] + 0.5
        self.maxspeed = rocketspeed[player - 1] * 1.5

    def move(self):
        """Update rocket position"""
        if self.exists:
            if self.speed < self.maxspeed:
                self.speed = self.speed * 1.01 + 0.01 * rocketspeed[self.player - 1]
            # Wrap around
            if self.x > SCREENWIDTH:
                self.x = 0
            if self.x < 0:
                self.x = SCREENWIDTH
            if self.y > SCREENHEIGHT:
                self.y = 0
            if self.y < 0:
                self.y = SCREENHEIGHT
        else:
            self.x = self.y = SCREENWIDTH + 500
            self.speed = 0
            
        rad = self.direction * math.pi / 180
        self.x += -self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)
        
        if self.player == 1:
            image = pygame.transform.rotate(ROCKET1, self.direction)
        else:
            image = pygame.transform.rotate(ROCKET2, self.direction)
            
        if self.exists:
            DISPLAY.blit(image, (self.x, self.y))


class Explode:
    """Explosion effect"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last = pygame.time.get_ticks()
        self.duration = 1600
        self.animation = 0
        explosionSound.play()

    def update(self):
        """Update explosion animation"""
        now = pygame.time.get_ticks()
        if now % 2 == 0:
            self.animation += 1
        if self.animation > 810:
            self.animation = 0
        if now - self.last <= self.duration:
            if self.x < SCREENWIDTH and self.y < SCREENHEIGHT:
                DISPLAY.blit(EXPLOSION_GIF_BIG, (self.x - 50, self.y - 50),
                             pygame.Rect((self.animation % 9) * 1200 / 9, (self.animation // 9) * 1200 / 9,
                                         1200 / 9, 1200 / 9))


class LukPowerup:
    """Lukas powerup"""
    def __init__(self, x=400, y=400):
        self.x = x
        self.y = y
        self.alive = True

    def update(self, frame):
        """Update powerup"""
        if self.alive:
            if self.x > SCREENWIDTH:
                self.x = 0
            self.x += 0.8
            DISPLAY.blit(LUKASPOWERUP, (self.x, self.y))


def ai_update(ai_ship, player_ship, rocket, frame_nr, superweapon_type, frame_cd):
    """
    AI controller for computer player
    Returns: (new_rocket, new_frame_cd, shoot_fired)
    """
    if not ai_ship.alive or not player_ship.alive:
        return rocket, frame_cd, False
    
    # Calculate angle to target
    dx = player_ship.x - ai_ship.x
    dy = player_ship.y - ai_ship.y
    target_angle = math.atan2(-dx, -dy) * 180 / math.pi
    
    # Normalize angles to -180 to 180
    current_angle = ai_ship.direction % 360
    if current_angle > 180:
        current_angle -= 360
    
    angle_diff = target_angle - current_angle
    while angle_diff > 180:
        angle_diff -= 360
    while angle_diff < -180:
        angle_diff += 360
    
    # Turn towards target
    if abs(angle_diff) > 5:
        if angle_diff > 0:
            ai_ship.change_angle("RIGHT", ai_ship.lukas)
            ai_ship.change_angle2()
            ai_ship.change_angle("RIGHT2", ai_ship.lukas)
        else:
            ai_ship.change_angle("LEFT", ai_ship.lukas)
            ai_ship.change_angle2()
            ai_ship.change_angle("LEFT2", ai_ship.lukas)
    
    # Calculate distance to target
    dist = math.sqrt(dx*dx + dy*dy)
    
    # Shooting decision
    should_shoot = False
    if abs(angle_diff) < 20 and dist < 400:  # Within firing arc and range
        if frame_nr - ai_ship.ai_last_shot > ai_ship.ai_shoot_cooldown:
            should_shoot = True
            ai_ship.ai_last_shot = frame_nr
    
    # Fire rocket if ready
    new_rocket = rocket
    if should_shoot and not rocket.exists:
        missileSound.play()
        new_rocket = Rocket(ai_ship.x, ai_ship.y, ai_ship.direction, True, 2)
    
    # Use superweapon decision
    new_frame_cd = frame_cd
    if superweapon_type == 1:  # Lightspeed
        if dist > 200 and dist < 350 and abs(angle_diff) < 15:
            if frame_nr > frame_cd + 200:
                # Check if lightspeed would hit
                rad = ai_ship.direction * math.pi / 180
                ls_end_x = ai_ship.x + 50 * (-ai_ship.speed * math.sin(rad))
                ls_end_y = ai_ship.y + 50 * (-ai_ship.speed * math.cos(rad))
                end_dist = math.sqrt((ls_end_x - player_ship.x)**2 + (ls_end_y - player_ship.y)**2)
                if end_dist < 100:
                    kill_bool = ai_ship.start_lightspeed(player_ship)
                    if kill_bool[0]:
                        new_frame_cd = frame_nr
    elif superweapon_type == 2:  # Spacemine
        if frame_nr > frame_cd + 200:
            if dist < 150:  # Drop mine when close
                new_frame_cd = frame_nr
                return ai_ship.start_spacemine(frame_nr), new_frame_cd, False
    
    return new_rocket, new_frame_cd, should_shoot


def endgame(p1_score, p2_score):
    """End game screen with sci-fi UI"""
    global GAME_MODE, PLAYER1_NAME, PLAYER2_NAME
    
    # Determine winner
    if p1_score > p2_score:
        winner = 1
        winner_text = f"BLUE ({PLAYER1_NAME}) has won with {p1_score} points!"
        winner_color = CYAN
    elif p2_score > p1_score:
        winner = 2
        if GAME_MODE == "PVE":
            winner_text = f"RED (AI BOT) has won with {p2_score} points!"
        else:
            winner_text = f"RED ({PLAYER2_NAME}) has won with {p2_score} points!"
        winner_color = RED
    else:
        winner = 0  # Draw
        winner_text = "DRAW GAME!"
        winner_color = WHITE
    
    # Button configuration
    buttons = [
        {"text": "RESTART GAME", "action": "restart", "color": CYAN, "y": 480},
        {"text": "Main Menu", "action": "menu", "color": RED, "y": 540},
        {"text": "Quit Game", "action": "quit", "color": (150, 0, 0), "y": 600}
    ]
    selected_button = 0
    
    # Animation variables
    alpha = 0
    fade_in = True
    particles = []
    for _ in range(50):
        particles.append({
            'x': random.randint(0, SCREENWIDTH),
            'y': random.randint(0, SCREENHEIGHT),
            'size': random.randint(1, 3),
            'speed': random.uniform(0.5, 1.5),
            'alpha': random.randint(50, 150)
        })
    
    while True:
        # Fade in animation
        if fade_in:
            alpha += 5
            if alpha >= 255:
                alpha = 255
                fade_in = False
        
        # Dark space background
        DISPLAY.fill((5, 10, 30))
        
        # Draw futuristic grid
        grid_alpha = int(alpha * 0.3)
        for x in range(0, SCREENWIDTH, 50):
            pygame.draw.line(DISPLAY, (0, 100, 150, grid_alpha), (x, 0), (x, SCREENHEIGHT), 1)
        for y in range(0, SCREENHEIGHT, 50):
            pygame.draw.line(DISPLAY, (0, 100, 150, grid_alpha), (0, y), (SCREENWIDTH, y), 1)
        
        # Draw particles
        for p in particles:
            p['y'] -= p['speed']
            if p['y'] < 0:
                p['y'] = SCREENHEIGHT
                p['x'] = random.randint(0, SCREENWIDTH)
            pygame.draw.circle(DISPLAY, (100, 200, 255, int(p['alpha'] * alpha / 255)), 
                             (int(p['x']), int(p['y'])), p['size'])
        
        # Corner tech patterns
        pygame.draw.line(DISPLAY, CYAN, (0, 0), (120, 0), 3)
        pygame.draw.line(DISPLAY, CYAN, (0, 0), (0, 120), 3)
        pygame.draw.line(DISPLAY, CYAN, (SCREENWIDTH-120, 0), (SCREENWIDTH, 0), 3)
        pygame.draw.line(DISPLAY, CYAN, (SCREENWIDTH, 0), (SCREENWIDTH, 120), 3)
        pygame.draw.line(DISPLAY, CYAN, (0, SCREENHEIGHT-120), (0, SCREENHEIGHT), 3)
        pygame.draw.line(DISPLAY, CYAN, (0, SCREENHEIGHT), (120, SCREENHEIGHT), 3)
        pygame.draw.line(DISPLAY, CYAN, (SCREENWIDTH-120, SCREENHEIGHT), (SCREENWIDTH, SCREENHEIGHT), 3)
        pygame.draw.line(DISPLAY, CYAN, (SCREENWIDTH, SCREENHEIGHT-120), (SCREENWIDTH, SCREENHEIGHT), 3)
        
        # Additional tech decorations
        pygame.draw.rect(DISPLAY, CYAN, (10, 10, 20, 20), 2)
        pygame.draw.rect(DISPLAY, CYAN, (SCREENWIDTH-30, 10, 20, 20), 2)
        pygame.draw.rect(DISPLAY, CYAN, (10, SCREENHEIGHT-30, 20, 20), 2)
        pygame.draw.rect(DISPLAY, CYAN, (SCREENWIDTH-30, SCREENHEIGHT-30, 20, 20), 2)
        
        # Title with glow
        title_font = pygame.font.Font('font.ttf', 48)
        title_text = title_font.render("SPACE FIGHTERS", True, CYAN)
        title_rect = title_text.get_rect(center=(SCREENWIDTH//2, 50))
        
        # Glow effect for title
        glow_surf = pygame.Surface((title_rect.width + 40, title_rect.height + 40), pygame.SRCALPHA)
        glow_surf.fill((0, 255, 255, 50))
        DISPLAY.blit(glow_surf, (title_rect.x - 20, title_rect.y - 20))
        DISPLAY.blit(title_text, title_rect)
        
        # Winner announcement
        winner_font = pygame.font.Font('font.ttf', 36)
        winner_render = winner_font.render(winner_text, True, winner_color)
        winner_rect = winner_render.get_rect(center=(SCREENWIDTH//2, 150))
        
        # Pulsing glow for winner text
        pulse_alpha = int(80 + 40 * math.sin(pygame.time.get_ticks() / 300))
        winner_glow = pygame.Surface((winner_rect.width + 40, winner_rect.height + 40), pygame.SRCALPHA)
        if winner == 1:
            winner_glow.fill((0, 255, 255, pulse_alpha))
        elif winner == 2:
            winner_glow.fill((255, 50, 50, pulse_alpha))
        else:
            winner_glow.fill((255, 255, 255, pulse_alpha))
        DISPLAY.blit(winner_glow, (winner_rect.x - 20, winner_rect.y - 20))
        DISPLAY.blit(winner_render, winner_rect)
        
        # Player score boxes
        box_width = 280
        box_height = 140
        box_y = 200
        
        # Player 1 box (Blue)
        p1_box_x = SCREENWIDTH//2 - box_width - 30
        if winner == 1:
            p1_glow_color = (0, 255, 255, 150)
            p1_border_width = 4
        else:
            p1_glow_color = (0, 150, 200, 80)
            p1_border_width = 2
        
        pygame.draw.rect(DISPLAY, (0, 50, 80), (p1_box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(DISPLAY, CYAN, (p1_box_x, box_y, box_width, box_height), 
                        p1_border_width, border_radius=15)
        
        # Glow for P1 box
        p1_glow = pygame.Surface((box_width + 20, box_height + 20), pygame.SRCALPHA)
        p1_glow.fill(p1_glow_color)
        DISPLAY.blit(p1_glow, (p1_box_x - 10, box_y - 10))
        
        # P1 content
        p1_name_text = FONT.render(f"Blue ({PLAYER1_NAME})", True, CYAN)
        p1_score_text = BIGFONT.render(str(p1_score), True, WHITE)
        DISPLAY.blit(p1_name_text, (p1_box_x + 90, box_y + 30))
        DISPLAY.blit(p1_score_text, (p1_box_x + 90, box_y + 75))
        
        # P1 icon (ship)
        ship1_scaled = pygame.transform.scale(SHIP1, (70, 70))
        DISPLAY.blit(ship1_scaled, (p1_box_x + 10, box_y + 35))
        
        # Player 2 box (Red)
        p2_box_x = SCREENWIDTH//2 + 30
        if winner == 2:
            p2_glow_color = (255, 50, 50, 150)
            p2_border_width = 4
        else:
            p2_glow_color = (150, 50, 50, 80)
            p2_border_width = 2
        
        pygame.draw.rect(DISPLAY, (80, 20, 20), (p2_box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(DISPLAY, RED, (p2_box_x, box_y, box_width, box_height), 
                        p2_border_width, border_radius=15)
        
        # Glow for P2 box
        p2_glow = pygame.Surface((box_width + 20, box_height + 20), pygame.SRCALPHA)
        p2_glow.fill(p2_glow_color)
        DISPLAY.blit(p2_glow, (p2_box_x - 10, box_y - 10))
        
        # P2 content
        if GAME_MODE == "PVE":
            p2_name_text = FONT.render("Red (AI BOT)", True, RED)
            # Draw robot icon for AI
            pygame.draw.circle(DISPLAY, (200, 50, 50), (p2_box_x + 40, box_y + 60), 25)
            pygame.draw.circle(DISPLAY, (255, 100, 100), (p2_box_x + 40, box_y + 60), 25, 2)
            # Robot eyes
            pygame.draw.circle(DISPLAY, WHITE, (p2_box_x + 32, box_y + 55), 5)
            pygame.draw.circle(DISPLAY, WHITE, (p2_box_x + 48, box_y + 55), 5)
            # Robot antenna
            pygame.draw.line(DISPLAY, (255, 100, 100), (p2_box_x + 40, box_y + 35), (p2_box_x + 40, box_y + 25), 2)
            pygame.draw.circle(DISPLAY, (255, 200, 0), (p2_box_x + 40, box_y + 22), 4)
        else:
            p2_name_text = FONT.render(f"Red ({PLAYER2_NAME})", True, RED)
            # P2 icon (ship)
            ship2_scaled = pygame.transform.scale(SHIP2, (60, 60))
            DISPLAY.blit(ship2_scaled, (p2_box_x + 10, box_y + 30))
        p2_score_text = BIGFONT.render(str(p2_score), True, WHITE)
        DISPLAY.blit(p2_name_text, (p2_box_x + 90, box_y + 30))
        DISPLAY.blit(p2_score_text, (p2_box_x + 90, box_y + 75))
        
        # Draw buttons
        for i, button in enumerate(buttons):
            btn_width = 300
            btn_height = 50
            btn_x = SCREENWIDTH//2 - btn_width//2
            btn_y = button['y']
            
            # Button hover effect
            if i == selected_button:
                btn_color = tuple(min(255, c + 50) for c in button['color'])
                btn_border = 3
            else:
                btn_color = button['color']
                btn_border = 2
            
            pygame.draw.rect(DISPLAY, btn_color, (btn_x, btn_y, btn_width, btn_height), 
                           btn_border, border_radius=10)
            
            # Button glow
            btn_glow = pygame.Surface((btn_width + 10, btn_height + 10), pygame.SRCALPHA)
            btn_glow.fill((*btn_color, 60))
            DISPLAY.blit(btn_glow, (btn_x - 5, btn_y - 5))
            
            # Button text
            btn_text = FONT.render(button['text'], True, WHITE)
            btn_rect = btn_text.get_rect(center=(SCREENWIDTH//2, btn_y + btn_height//2))
            DISPLAY.blit(btn_text, btn_rect)
            
            # Button icons (simple text icons)
            icon_font = pygame.font.Font('font.ttf', 16)
            if i == 0:  # Restart
                icon_text = icon_font.render("↻", True, WHITE)
            elif i == 1:  # Menu
                icon_text = icon_font.render("⌂", True, WHITE)
            else:  # Quit
                icon_text = icon_font.render("✖", True, WHITE)
            DISPLAY.blit(icon_text, (btn_x + 20, btn_y + btn_height//2 - 10))
        
        # Energy/smoke effect in bottom right corner
        smoke_alpha = int(100 + 50 * math.sin(pygame.time.get_ticks() / 500))
        for i in range(5):
            smoke_x = SCREENWIDTH - 50 - i * 30
            smoke_y = SCREENHEIGHT - 50 - i * 20
            smoke_size = 30 + i * 10
            smoke_alpha_i = max(0, smoke_alpha - i * 20)
            smoke_surf = pygame.Surface((smoke_size * 2, smoke_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(smoke_surf, (0, 200, 255, smoke_alpha_i), (smoke_size, smoke_size), smoke_size)
            DISPLAY.blit(smoke_surf, (smoke_x - smoke_size, smoke_y - smoke_size))
        
        # Control hints
        hint_font = pygame.font.Font('font.ttf', 12)
        hint_text = hint_font.render("[Enter] Restart  [ESC] Quit  [↑↓] Navigate  [Space] Select", True, (150, 200, 255))
        DISPLAY.blit(hint_text, (SCREENWIDTH//2 - hint_text.get_width()//2, SCREENHEIGHT - 30))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                handle_resize(event)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN or event.key == K_SPACE:
                    if selected_button == 0:  # Restart
                        main()
                        return
                    elif selected_button == 1:  # Menu
                        import main
                        main.main()
                        return
                    elif selected_button == 2:  # Quit
                        pygame.quit()
                        sys.exit()
                elif event.key == K_UP:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == K_DOWN:
                    selected_button = (selected_button + 1) % len(buttons)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Scale mouse coordinates to virtual surface
                    scale_x = SCREENWIDTH / WINDOW_WIDTH
                    scale_y = SCREENHEIGHT / WINDOW_HEIGHT
                    mouse_x = int(mouse_x * scale_x)
                    mouse_y = int(mouse_y * scale_y)
                    
                    for i, button in enumerate(buttons):
                        btn_width = 300
                        btn_height = 50
                        btn_x = SCREENWIDTH//2 - btn_width//2
                        btn_y = button['y']
                        if btn_x <= mouse_x <= btn_x + btn_width and btn_y <= mouse_y <= btn_y + btn_height:
                            if i == 0:  # Restart
                                main()
                                return
                            elif i == 1:  # Menu
                                import main
                                main.main()
                                return
                            elif i == 2:  # Quit
                                pygame.quit()
                                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scale_x = SCREENWIDTH / WINDOW_WIDTH
                scale_y = SCREENHEIGHT / WINDOW_HEIGHT
                mouse_x = int(mouse_x * scale_x)
                mouse_y = int(mouse_y * scale_y)
                
                for i, button in enumerate(buttons):
                    btn_width = 300
                    btn_height = 50
                    btn_x = SCREENWIDTH//2 - btn_width//2
                    btn_y = button['y']
                    if btn_x <= mouse_x <= btn_x + btn_width and btn_y <= mouse_y <= btn_y + btn_height:
                        selected_button = i
                        break
        
        scale_display()
        fpsClock.tick(60)


def intro(ships):
    """Game intro"""
    main_txt1 = "ready up"
    done = False
    i = SCREENHEIGHT
    j = i
    
    while not done:
        if i > 100:
            i -= 1
        DISPLAY.fill(BLACK)
        DISPLAY.blit(BACKGROUND, (0, 0))
        
        if i > 400:
            p1_txt = SPACEFONT.render(main_txt1, True, WHITE)
        elif i > 300:
            p1_txt = SPACEFONT.render(main_txt1, True, RED)
        elif i > 200:
            p1_txt = SPACEFONT.render(main_txt1, True, ORANGE)
        else:
            p1_txt = SPACEFONT.render(main_txt1, True, GREEN)

        if i > 200:
            j = i
        DISPLAY.blit(p1_txt, (250, j))

        for ship in ships:
            ship.move()

        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                handle_resize(event)
            if not hasattr(event, 'key'):
                continue
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    ships[0].change_angle("RIGHT", False)
                if event.key == K_LEFT:
                    ships[0].change_angle("LEFT", False)
                if event.key == K_d:
                    if len(ships) > 1 and GAME_MODE == "PVP":
                        ships[1].change_angle("RIGHT", False)

        scale_display()
        fpsClock.tick(60)

        if i < 110:
            done = True


def main():
    """Main game loop"""
    global GAME_MODE, shipspeed, maneuv, rocketspeed, superweapon, map_manager
    
    # Load stats
    stats1 = load_stats(1)
    stats2 = load_stats(2)
    
    # Parse stats
    try:
        STATS1 = eval(stats1) if isinstance(stats1, str) else [1, 1, 1, 1000, 1]
        STATS2 = eval(stats2) if isinstance(stats2, str) else [1, 1, 1, 1000, 1]
    except:
        STATS1 = [1, 1, 1, 1000, 1]
        STATS2 = [1, 1, 1, 1000, 1]
    
    shipspeed = [int(STATS1[1]), int(STATS2[1])]
    maneuv = [int(STATS1[4]), int(STATS2[4])]
    rocketspeed = [int(STATS1[7]) if len(STATS1) > 7 else 1, int(STATS2[7]) if len(STATS2) > 7 else 1]
    superweapon = [int(STATS1[-2]) if len(STATS1) >= 2 else 1, int(STATS2[-2]) if len(STATS2) >= 2 else 1]

    # Initialize map manager
    map_manager = MapManager(SELECTED_MAP)

    # Initialize entities
    pygame.mixer.music.play(0, 0)
    explosionSound.set_volume(0)
    missileSound.set_volume(0)
    
    x = SCREENWIDTH
    y = SCREENHEIGHT
    
    ship1 = Ship(x * 0.8, y * 0.8, 1)
    ship2 = Ship(x * 0.2, y * 0.8, 2)
    
    rocket1 = Rocket(999, 999, 0, False, 1)
    rocket2 = Rocket(999, 999, 0, False, 2)
    
    # Explosions
    explosions = [Explode(x + 500, y + 500) for _ in range(10)]
    explosion1 = Explode(x + 500, y + 500)
    explosion2 = Explode(x + 500, y + 500)
    explosion_super1 = Explode(x + 500, y + 500)
    explosion_super2 = Explode(x + 500, y + 500)
    
    explosionSound.set_volume(0.3)
    missileSound.set_volume(0.1)
    
    spaceminelist = []

    # Initialize powerup
    luk = LukPowerup()
    luk_initialized = False
    luk.alive = False

    # Scores
    p1_score = 0
    p2_score = 0

    frame_nr = 0
    frame_cd1 = 0
    frame_cd2 = 0

    intro_played = False
    frame_start = 0

    # MAIN LOOP
    while True:
        frame_nr += 1
        DISPLAY.fill(BLACK)
        DISPLAY.blit(BACKGROUND, (0, 0))
        
        # Update map mechanics
        if map_manager:
            map_manager.update()
            map_manager.draw(DISPLAY)
            
            # Flash effect when gravity reverses in Map 3
            if map_manager.name == "Reverse Gravity Zone" and map_manager.reverse_timer == map_manager.reverse_interval - 1:
                # Create flash surface
                flash_surf = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
                flash_color = (100, 255, 100) if map_manager.gravity_direction == 1 else (255, 100, 100)
                flash_surf.fill(flash_color)
                flash_surf.set_alpha(100)
                DISPLAY.blit(flash_surf, (0, 0))
        
        # Update ships
        ship1.move()
        ship2.move()
        ship1.change_angle2()
        ship2.change_angle2()
        
        # Apply gravity effects
        if map_manager:
            map_manager.apply_gravity(ship1)
            map_manager.apply_gravity(ship2)
        
        # Update rockets
        rocket1.move()
        rocket2.move()
        
        # AI Update (if PvE mode)
        if GAME_MODE == "PVE":
            rocket2, frame_cd2, _ = ai_update(ship2, ship1, rocket2, frame_nr, superweapon[1], frame_cd2)
            ship2.stop_lightspeed()  # Handle lightspeed end
        
        # Update spacemines
        if spaceminelist:
            for mine in spaceminelist[:]:
                if mine.alive:
                    mine.update()
                    minepoint = Point(mine.x, mine.y)
                    
                    # Check collision with ships
                    for ship, ship_idx in [(ship1, 1), (ship2, 2)]:
                        if ship.alive and mine.player != ship_idx:
                            entitypoint = Point(ship.x, ship.y)
                            if distance(minepoint, entitypoint) < mine.radius + 20:
                                if mine in spaceminelist:
                                    spaceminelist.remove(mine)
                                if ship_idx == 1:
                                    ship1 = Ship(x * 0.8, y * 0.8, 1)
                                    p1_score -= 1
                                    p2_score += 3
                                    explosion_super2 = Explode(ship.x, ship.y)
                                else:
                                    ship2 = Ship(x * 0.2, y * 0.8, 2)
                                    p2_score -= 1
                                    p1_score += 3
                                    explosion_super1 = Explode(ship.x, ship.y)
                                break
                elif not mine.alive and not mine.hasexploded:
                    mine.hasexploded = True
        
        # Update explosions
        for exp in [explosion1, explosion2, explosion_super1, explosion_super2]:
            exp.update()
        
        # Update powerup
        luk.update(frame_nr)
        if not luk.alive and frame_nr % 100 == 0:
            luk.x = random.choice(range(0, 10)) * 80
            luk.y = random.choice(range(0, 10)) * 60
        if frame_nr > 300 and not luk_initialized:
            luk.alive = True
            luk_initialized = True

        # Draw scores
        p1_txt = BIGFONT.render(f" {p1_score} ", True, WHITE, BLUE)
        DISPLAY.blit(p1_txt, (SCREENWIDTH - 50, 50))
        p2_txt = BIGFONT.render(f" {p2_score} ", True, WHITE, RED)
        DISPLAY.blit(p2_txt, (50, 50))
        
        # Mode indicator
        mode_text = SMALLFONT.render(f"Mode: {GAME_MODE}", True, WHITE)
        DISPLAY.blit(mode_text, (SCREENWIDTH//2 - mode_text.get_width()//2, 10))

        # Endgame check
        if p1_score > p2_score + 20:
            endgame(p1_score, p2_score)
            return
        if p2_score > p1_score + 20:
            endgame(p1_score, p2_score)
            return

        # Collision detection
        # Ship collisions
        collisionx12 = ship1.x < ship2.x + 30 and ship1.x > ship2.x - 30
        collisiony12 = ship1.y < ship2.y + 30 and ship1.y > ship2.y - 30
        collision12 = collisionx12 and collisiony12

        # Rocket collisions
        collisionx1r2 = ship2.x < rocket1.x + 25 and ship2.x > rocket1.x - 25
        collisiony1r2 = ship2.y < rocket1.y + 25 and ship2.y > rocket1.y - 25
        collision1r2 = collisionx1r2 and collisiony1r2

        collisionx2r1 = ship1.x < rocket2.x + 25 and ship1.x > rocket2.x - 25
        collisiony2r1 = ship1.y < rocket2.y + 25 and ship1.y > rocket2.y - 25
        collision2r1 = collisionx2r1 and collisiony2r1

        # Powerup collisions
        collision_xluk1 = ship1.x < luk.x + 30 and ship1.x > luk.x - 30
        collision_yluk1 = ship1.y < luk.y + 30 and ship1.y > luk.y - 30
        collisionluk1 = collision_xluk1 and collision_yluk1

        collision_xluk2 = ship2.x < luk.x + 30 and ship2.x > luk.x - 30
        collision_yluk2 = ship2.y < luk.y + 30 and ship2.y > luk.y - 30
        collisionluk2 = collision_xluk2 and collision_yluk2

        # Check asteroid collisions
        asteroid_collision1 = False
        asteroid_collision2 = False
        if map_manager and map_manager.name in ["Gravity Chaos Zone", "Reverse Gravity Zone"]:
            for asteroid in map_manager.asteroids:
                # Check ship1 vs asteroid
                dx1 = ship1.x - asteroid['x']
                dy1 = ship1.y - asteroid['y']
                dist1 = math.sqrt(dx1*dx1 + dy1*dy1)
                if dist1 < asteroid['radius'] + 20:  # Ship radius approx 20
                    asteroid_collision1 = True
                    explosion1 = Explode(ship1.x, ship1.y)
                    ship1 = Ship(x * 0.8, y * 0.8, 1)
                    p1_score -= 1
                    p2_score += 3
                    break
                
                # Check ship2 vs asteroid
                dx2 = ship2.x - asteroid['x']
                dy2 = ship2.y - asteroid['y']
                dist2 = math.sqrt(dx2*dx2 + dy2*dy2)
                if dist2 < asteroid['radius'] + 20:
                    asteroid_collision2 = True
                    explosion2 = Explode(ship2.x, ship2.y)
                    ship2 = Ship(x * 0.2, y * 0.8, 2)
                    p2_score -= 1
                    p1_score += 3
                    break

        # Handle collisions
        if collision12:
            explosion1 = Explode((ship1.x + ship2.x) / 2, (ship1.y + ship2.y) / 2)
            ship1 = Ship(x * 0.8, y * 0.8, 1)
            ship2 = Ship(x * 0.2, y * 0.8, 2)
            p1_score -= 1
            p2_score -= 1

        elif collision2r1:
            explosion2 = Explode(rocket2.x, rocket2.y)
            rocket2 = Rocket(999, 999, 0, False, 2)
            ship1 = Ship(x * 0.8, y * 0.8, 1)
            p1_score -= 1
            p2_score += 3

        elif collision1r2:
            explosion1 = Explode(rocket1.x, rocket1.y)
            rocket1 = Rocket(999, 999, 0, False, 1)
            ship2 = Ship(x * 0.2, y * 0.8, 2)
            p2_score -= 1
            p1_score += 3

        # Powerup effects
        if collisionluk1 and luk.alive:
            ship2.lukas = True
            luk.alive = False
            frame_start = frame_nr

        if collisionluk2 and luk.alive:
            ship1.lukas = True
            luk.alive = False
            frame_start = frame_nr

        # Reset powerup debuff
        if frame_nr > frame_start + 200:
            ship1.lukas = False
            ship2.lukas = False
        
        # Respawn powerup
        if frame_nr > frame_start + 750:
            luk.alive = True

        # Event handling
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                handle_resize(event)
            if not hasattr(event, 'key'):
                continue

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    import main
                    main.main()
                    return

                # Player 1 controls (always human)
                if event.key == K_RIGHT:
                    ship1.change_angle("RIGHT", ship1.lukas)
                if event.key == K_LEFT:
                    ship1.change_angle("LEFT", ship1.lukas)
                if event.key == K_UP:
                    missileSound.play()
                    rocket1 = Rocket(ship1.x, ship1.y, ship1.direction, True, 1)
                
                # Player 1 superweapon
                if event.key == K_DOWN:
                    if superweapon[0] == 1:  # Lightspeed
                        if frame_nr > frame_cd1 + 200 and ship1.alive:
                            kill_bool = ship1.start_lightspeed(ship2)
                            if kill_bool[0]:
                                explosion_super1 = Explode(ship2.x, ship2.y)
                                ship2 = Ship(x * 0.2, y * 0.8, 2)
                                p2_score -= 1
                                p1_score += 3
                            frame_cd1 = frame_nr
                        ship1.stop_lightspeed()
                    elif superweapon[0] == 2:  # Spacemine
                        if frame_nr > frame_cd1 + 200 and ship1.alive:
                            frame_cd1 = frame_nr
                            spaceminelist.append(ship1.start_spacemine(frame_nr))

                # Player 2 controls (only in PvP mode)
                if GAME_MODE == "PVP":
                    if event.key == K_d:
                        ship2.change_angle("RIGHT", ship2.lukas)
                    if event.key == K_a:
                        ship2.change_angle("LEFT", ship2.lukas)
                    if event.key == K_w:
                        missileSound.play()
                        rocket2 = Rocket(ship2.x, ship2.y, ship2.direction, True, 2)
                    
                    # Player 2 superweapon
                    if event.key == K_s:
                        if superweapon[1] == 1:  # Lightspeed
                            if frame_nr > frame_cd2 + 200 and ship2.alive:
                                kill_bool = ship2.start_lightspeed(ship1)
                                if kill_bool[0]:
                                    explosion_super2 = Explode(ship1.x, ship1.y)
                                    ship1 = Ship(x * 0.8, y * 0.8, 1)
                                    p1_score -= 1
                                    p2_score += 3
                                frame_cd2 = frame_nr
                            ship2.stop_lightspeed()
                        elif superweapon[1] == 2:  # Spacemine
                            if frame_nr > frame_cd2 + 200 and ship2.alive:
                                frame_cd2 = frame_nr
                                spaceminelist.append(ship2.start_spacemine(frame_nr))

            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    ship1.change_angle("RIGHT2", ship1.lukas)
                if event.key == K_LEFT:
                    ship1.change_angle("LEFT2", ship1.lukas)
                
                if GAME_MODE == "PVP":
                    if event.key == K_a:
                        ship2.change_angle("LEFT2", ship2.lukas)
                    if event.key == K_d:
                        ship2.change_angle("RIGHT2", ship2.lukas)

        scale_display()
        fpsClock.tick(60)

        if not intro_played:
            intro([ship1, ship2])
            intro_played = True


if __name__ == "__main__":
    main()
