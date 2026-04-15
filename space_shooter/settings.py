"""
Settings - Game constants and configuration
"""
import pygame

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
SUPERWEAPON_GRAVITY = "Gravity Well"

# Font Paths
FONT_MAIN = 'resources/font.ttf'
FONT_SPACE = 'resources/space.ttf'
FONT_PRESSSTART = 'resources/pressstart.ttf'

# Asset Paths
ASSET_BACKGROUND = 'resources/background.png'
ASSET_BACKGROUND_1600 = 'resources/background1600.png'
ASSET_BACKGROUND_MAP2 = 'resources/background.png'  # Map 2 dùng background mặc định
ASSET_BACKGROUND_MAP3 = 'resources/backgroundmap3.png'
ASSET_SHIP1 = 'resources/ship1.png'
ASSET_SHIP2 = 'resources/ship2.png'
ASSET_ROCKET1 = 'resources/rocket1.png'
ASSET_ROCKET2 = 'resources/rocket2.png'
ASSET_EXPLOSION = 'resources/explosion.png'
ASSET_BLACKHOLE = 'resources/blackhole.png'
ASSET_POWERUP = 'resources/lukas_powerup.png'

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
