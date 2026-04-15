"""
Settings - Game constants and configuration
"""
import pygame

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Initialize Pygame for font loading
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
DARK_GRAY = (50, 50, 50)
GRAY = (128, 128, 128)

# Game Modes
GAME_MODE_PVP = "PVP"
GAME_MODE_PVE = "PVE"

# Map Names
MAP_DEEP_SPACE = "Deep Space Arena"
MAP_GRAVITY_CHAOS = "Gravity Chaos Zone"
MAP_REVERSE_GRAVITY = "Reverse Gravity Zone"

# Player Settings
MAX_HP = 100
DAMAGE_PER_HIT = 10
WIN_SCORE_DIFF = 20  # Win when score diff > this

# Upgrade Settings
STARTING_MONEY = 1000
UPGRADE_COST = 200
MAX_UPGRADE_LEVEL = 5
UPGRADE_REWARD_WIN_PVE = 200
UPGRADE_REWARD_LOSS_PVE = 50
UPGRADE_REWARD_WIN_PVP = 150
UPGRADE_REWARD_LOSS_PVP = 0

# Map Physics
BLACK_HOLE_K = 0.8  # Gravity constant
BLACK_HOLE_MAX_DIST = 300  # Only affect within this distance
BLACK_HOLE_RADIUS = 50
REVERSE_INTERVAL = 15  # seconds

# Superweapons
SUPERWEAPON_LIGHTSPEED = 1
SUPERWEAPON_SPACEMINE = 2
SUPERWEAPON_PLASMA = 3

# Font Paths
FONT_MAIN = 'font.ttf'
FONT_SPACE = 'resources/space.ttf'

# Asset Paths (relative to game folder)
ASSET_BG = 'resources/background.png'
ASSET_BG_1600 = 'resources/background1600.png'
ASSET_SHIP1 = 'resources/ship1.png'
ASSET_SHIP2 = 'resources/ship2.png'
ASSET_SHIP1_LS = 'resources/ship1_lightspeed.png'
ASSET_SHIP2_LS = 'resources/ship2_lightspeed.png'
ASSET_SHIP1_SM = 'resources/spacemine.png'
ASSET_ROCKET1 = 'resources/rocket1.png'
ASSET_ROCKET2 = 'resources/rocket2.png'
ASSET_CURSOR = 'resources/cursor.png'

# Audio Paths
AUDIO_BG_MUSIC = 'resources/bg_music.mp3'
AUDIO_MISSILE = 'resources/missile.wav'
AUDIO_EXPLOSION = 'resources/explosion.wav'

# Load fonts
try:
    FONT_BIG = pygame.font.Font(FONT_MAIN, 34)
    FONT_MED = pygame.font.Font(FONT_MAIN, 28)
    FONT_SMALL = pygame.font.Font(FONT_MAIN, 16)
    FONT_TINY = pygame.font.Font(FONT_MAIN, 9)
    FONT_TITLE = pygame.font.Font(FONT_SPACE, 48)
except:
    FONT_BIG = FONT_MED = FONT_SMALL = FONT_TINY = FONT_TITLE = pygame.font.SysFont('arial', 20)
