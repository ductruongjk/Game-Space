"""
Settings - Game constants and configuration
"""
import os
import pygame

BASE_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Initialize Pygame
pygame.init()

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
NEON_PURPLE = (180, 50, 255)
GOLD = (255, 215, 0)

# Game Modes
GAME_MODE_PVP = "PVP"
GAME_MODE_PVE = "PVE"

# Map Names
MAP_DEEP_SPACE = "Deep Space Arena"
MAP_GRAVITY_CHAOS = "Gravity Chaos Zone"
MAP_REVERSE_GRAVITY = "Reverse Gravity Zone"

# Player Settings
PLAYER_COUNT = 2
SHIP_BASE_SPEED = 3
SHIP_MAX_SPEED = 8
MANEUVERABILITY_DEFAULT = 3
ROCKET_BASE_SPEED = 10

# Map Mechanics
GRAVITY_STRENGTH = 0.3
BLACK_HOLE_RADIUS = 50
REVERSE_INTERVAL = 14  # seconds

# Superweapons
SUPERWEAPON_PLASMA = "Plasma Blast"
SUPERWEAPON_LIGHTSPEED = "Light Speed"
SUPERWEAPON_GRAVITY = "Naval Mine"

# Font Paths
FONT_MAIN = os.path.join(RESOURCES_DIR, 'font.ttf')
FONT_SPACE = os.path.join(RESOURCES_DIR, 'space.ttf')
FONT_PRESSSTART = os.path.join(RESOURCES_DIR, 'pressstart.ttf')

# Asset Paths
ASSET_SHIP1BIG = os.path.join(RESOURCES_DIR, 'ship1big.png')
ASSET_BACKGROUND = os.path.join(RESOURCES_DIR, 'background.png')
ASSET_BACKGROUND_1600 = os.path.join(RESOURCES_DIR, 'background1600.png')
ASSET_BACKGROUND_MAP2 = os.path.join(RESOURCES_DIR, 'backgroundmap2.png')
ASSET_BACKGROUND_MAP3 = os.path.join(RESOURCES_DIR, 'backgroundmap3.jpg')
ASSET_SHIP1 = os.path.join(RESOURCES_DIR, 'ship1.png')
ASSET_SHIP2 = os.path.join(RESOURCES_DIR, 'ship2.png')
ASSET_ROCKET1 = os.path.join(RESOURCES_DIR, 'rocket1.png')
ASSET_ROCKET2 = os.path.join(RESOURCES_DIR, 'rocket2.png')
ASSET_EXPLOSION = os.path.join(RESOURCES_DIR, 'explosion.png')
ASSET_EXPLOSION_ANIM = os.path.join(RESOURCES_DIR, 'explosion_anim_1200x1200.png')
ASSET_RESPAWN_ANIM = os.path.join(RESOURCES_DIR, 'respawn_anim_900x900_test.png')
ASSET_SHIP1_LS = os.path.join(RESOURCES_DIR, 'ship1_lightspeed.png')
ASSET_SHIP2_LS = os.path.join(RESOURCES_DIR, 'ship2_lightspeed.png')
ASSET_NAVALMINE1 = os.path.join(RESOURCES_DIR, 'navalmine1.webp')
ASSET_NAVALMINE2 = os.path.join(RESOURCES_DIR, 'navalmine2.jpg')
ASSET_PLASMA_BLAST = os.path.join(RESOURCES_DIR, 'Muzzle Mega Ion', 'Muzzle Mega Ion_1.png')
ASSET_BLACKHOLE = os.path.join(RESOURCES_DIR, 'blackhole.png')
ASSET_ASTEROIDS_FOLDER = os.path.join(RESOURCES_DIR, 'asteroids')
ASSET_POWERUP = os.path.join(RESOURCES_DIR, 'lukas_powerup.png')

# Audio Paths
AUDIO_BG_MUSIC = 'resources/bg_music.mp3'
AUDIO_MISSILE = 'resources/missile.wav'
AUDIO_EXPLOSION = 'resources/explosion.wav'

# Upgrade Settings
STARTING_BUDGET = 1000
UPGRADE_COST = 50
UPGRADE_INCREMENT = 0.5

# Win Condition
WIN_SCORE = 20
