#!/usr/bin/env python3
"""Space Shooter - Based on space-fighters-master original rules"""
import sys
import os
import pygame
import math
import random
from pygame.locals import *

sys.path.insert(0, '.')
from settings import *
from entities import Ship, Rocket, Spacemine, Explode, LukPowerup
from maps import DeepSpaceMap, GravityChaosMap, ReverseGravityMap
from screens import MainMenu, MapSelect, UpgradeScreen

# ==================== INITIALIZE ====================
pygame.init()
SW, SH = 800, 600
WINDOW = pygame.display.set_mode((SW, SH), pygame.RESIZABLE)
pygame.display.set_caption("Space Shooter")
try:
    pygame.display.set_icon(pygame.image.load(ASSET_SHIP1BIG))
except:
    pass
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(0)
pygame.key.set_repeat(0)  # Disable by default, enable only during gameplay

VS = pygame.Surface((SW, SH))
DISPLAY = VS
WW, WH = SW, SH

def scale_display():
    global WINDOW, VS, WW, WH
    scaled = pygame.transform.smoothscale(VS, (WW, WH))
    WINDOW.blit(scaled, (0, 0))
    pygame.display.update()

def handle_resize(e):
    global WINDOW, WW, WH
    WW, WH = e.w, e.h
    WINDOW = pygame.display.set_mode((WW, WH), pygame.RESIZABLE)

# ==================== SOUNDS ====================
try:
    pygame.mixer.music.load(AUDIO_BG_MUSIC)
    missileSnd = pygame.mixer.Sound(AUDIO_MISSILE)
    explosionSnd = pygame.mixer.Sound(AUDIO_EXPLOSION)
except:
    missileSnd = None
    explosionSnd = None

# ==================== FONTS ====================
try:
    SF = pygame.font.Font('resources/space.ttf', 34)
    BF = pygame.font.Font('resources/font.ttf', 30)
    F = pygame.font.Font('resources/font.ttf', 16)
    SF2 = pygame.font.Font('resources/font.ttf', 9)
except:
    SF = BF = F = SF2 = pygame.font.SysFont('arial', 20)

# ==================== TEXTURES ====================
try:
    BG = pygame.image.load(ASSET_BACKGROUND_1600)
    S1 = pygame.image.load(ASSET_SHIP1)
    S2 = pygame.image.load(ASSET_SHIP2)
    R1 = pygame.image.load(ASSET_ROCKET1)
    R2 = pygame.image.load(ASSET_ROCKET2)
    EG = pygame.image.load(os.path.join(RESOURCES_DIR, 'endgamescreen1600.png'))
    LP = pygame.image.load(ASSET_POWERUP)
    EXG = pygame.image.load(ASSET_EXPLOSION_ANIM)
    RG = pygame.image.load(ASSET_RESPAWN_ANIM)
    S1LS = pygame.image.load(ASSET_SHIP1_LS)
    S2LS = pygame.image.load(ASSET_SHIP2_LS)
    NAVALMINE1_IMG = pygame.image.load(ASSET_NAVALMINE1).convert_alpha()
    NAVALMINE2_IMG = pygame.image.load(ASSET_NAVALMINE2).convert_alpha()
    PLASMA_IMG = pygame.image.load(ASSET_PLASMA_BLAST).convert_alpha()
except Exception as e:
    print(f"Error loading assets: {e}")
    sys.exit(1)

# ==================== COLORS ====================
BLACK=(0,0,0); WHITE=(255,255,255); BLUE=(100,115,175); RED=(176,52,52)
GREEN=(84,155,70); ORANGE=(255,150,0); YELLOW=(255,255,0); CYAN=(0,255,255)
CYAN_D=(0,150,200); GOLD=(255,215,0)

# ==================== GAME STATE ====================
GAME_MODE = "PVP"
SELECTED_MAP = "Deep Space Arena"
PLAYER1_NAME = "Player 1"
PLAYER2_NAME = "Player 2"
PLAYERS = 2

shipspeed = [1, 1]
maneuv = [1, 1]
rocketspeed = [1, 1]
superweapon = [1, 1]  # 1=lightspeed, 2=spacemine


# ==================== POINT / DISTANCE ====================
class Point:
    def __init__(s,x,y): s.x=x; s.y=y
def dist(a,b): return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
def lies_btwn(x,y,z):
    a=dist(y,z); b=dist(z,x); c=dist(x,y)
    return a*a+b*b>=c*c and a*a+c*c>=b*b


# ==================== LOAD/SAVE STATS ====================
def load_stats(p):
    try:
        with open(f"stats{p}.txt","r") as f: return f.read()
    except: return "[1,1,1,1000,1]"

def save_stats(p, stats):
    try:
        with open(f"stats{p}.txt","w") as f: f.write(str(stats))
    except: pass


# ==================== SHIP CLASS (from original) ====================
class Ship:
    def __init__(s,x,y,p):
        s.player=p
        s.x=random.choice(range(5,9))*x/10
        s.y=random.choice(range(5,9))*y/10
        s.speed=0.7*shipspeed[p-1]
        s.direction=0
        s.k_left=s.k_right=0
        s.lukas=False
        s.boolean=False
        s.direc=""
        s.alive=True
        s.ls_start=[0,0]
        s.ls_end=[0,0]
        s.ls_alive=False
        s.speed_boost=1.0
        s.boost_until=0
        s.control_reversed=False
        s.last=pygame.time.get_ticks()
        s.resp_dur=1600
        s.resp_anim=0
        s.resp_run=True
        s.resp_x=s.x
        s.resp_y=s.y
        # AI
        s.ai_last_shot=0
        s.ai_shoot_cooldown=60

    def respawn(s):
        s.alive=False
        now=pygame.time.get_ticks()
        if now%2==0: s.resp_anim+=1
        if now-s.last<=s.resp_dur:
            DISPLAY.blit(RG,(s.resp_x-50,s.resp_y-50),
                pygame.Rect((s.resp_anim%9)*100,(s.resp_anim//9)*100,100,100))
        else:
            s.resp_run=False
            s.alive=True
            s.x=s.resp_x
            s.y=s.resp_y

    def move(s):
        if s.resp_run and s.player<=PLAYERS:
            s.respawn()
        if s.alive:
            s.direction=0
            s.direction+=(s.k_left+s.k_right)
            rad=s.direction*math.pi/180
            speed_multiplier = s.speed_boost
            if s.control_reversed:
                s.x-=s.speed*speed_multiplier*math.sin(rad)
                s.y-=s.speed*speed_multiplier*math.cos(rad)
            else:
                s.x+=-s.speed*speed_multiplier*math.sin(rad)
                s.y+=-s.speed*speed_multiplier*math.cos(rad)
            if s.x>SW: s.x=0
            if s.x<0: s.x=SW
            if s.y>SH: s.y=0
            if s.y<0: s.y=SH
            img=pygame.transform.rotate(S1 if s.player==1 else S2, s.direction)
            s.image=img
            DISPLAY.blit(img,(s.x,s.y))
            if s.speed_boost>1.0 and pygame.time.get_ticks()>=s.boost_until:
                s.speed_boost=1.0
            if s.control_reversed and pygame.time.get_ticks()>=s.boost_until:
                s.control_reversed=False
        else:
            s.x=s.y=SW*s.player

    def change_angle(s,d,luka):
        if d=="LEFT": s.boolean=True; s.direc="LEFT"
        if d=="RIGHT": s.boolean=True; s.direc="RIGHT"
        if d=="LEFT2": s.boolean=False; s.direc="LEFT2"
        if d=="RIGHT2": s.boolean=False; s.direc="RIGHT2"

    def change_angle2(s):
        m=0.6*maneuv[s.player-1]
        if s.direc=="LEFT" and s.boolean:
            if not s.lukas: s.k_left+=m
            else: s.k_right+=-m
        if s.direc=="RIGHT" and s.boolean:
            if not s.lukas: s.k_right+=-m
            else: s.k_left+=m

    def start_lightspeed(s,other):
        if s.alive:
            now = pygame.time.get_ticks()
            s.speed_boost = 2.5
            s.boost_until = now + 5000
            return [False, False, False]
        return [False, False, False]

    def stop_lightspeed(s):
        if s.ls_alive:
            s.ls_alive = False
            s.speed_boost = 1.0
            s.boost_until = 0

    def start_plasma_blast(s, other, beams):
        if s.alive:
            beam = PlasmaBeam(s.x, s.y, s.direction, s.player, other)
            beams.append(beam)
            return False
        return False

    def start_spacemine(s,frame_nr):
        mines = []
        now = pygame.time.get_ticks()
        side = random.choice(['top','bottom','left','right'])
        for _ in range(2):
            if side == 'top':
                cx = random.randint(0, SW)
                cy = -30
                angle = random.uniform(20, 160)
            elif side == 'bottom':
                cx = random.randint(0, SW)
                cy = SH + 30
                angle = random.uniform(200, 340)
            elif side == 'left':
                cx = -30
                cy = random.randint(0, SH)
                angle = random.uniform(-70, 70)
            else:
                cx = SW + 30
                cy = random.randint(0, SH)
                angle = random.uniform(110, 250)
            mine = Spacemine(
                cx,
                cy,
                s.player,
                now,
                True,
                angle
            )
            mine.image = NAVALMINE1_IMG if s.player == 1 else NAVALMINE2_IMG
            mines.append(mine)
        return mines


# ==================== ROCKET CLASS (from original) ====================
class Rocket:
    def __init__(s,x,y,dir,exists,p):
        s.x=x; s.y=y; s.direction=dir; s.exists=exists; s.player=p
        s.speed=0.2*rocketspeed[p-1]+0.5
        s.maxspeed=rocketspeed[p-1]*1.5

    def move(s):
        if s.exists:
            if s.speed<s.maxspeed:
                s.speed=s.speed*1.01+0.01*rocketspeed[s.player-1]
            if s.x>SW: s.x=0
            if s.x<0: s.x=SW
            if s.y>SH: s.y=0
            if s.y<0: s.y=SH
        else:
            s.x=s.y=SW+500
            s.speed=0
        rad=s.direction*math.pi/180
        s.x+=-s.speed*math.sin(rad)
        s.y+=-s.speed*math.cos(rad)
        if s.exists:
            img=pygame.transform.rotate(R1 if s.player==1 else R2, s.direction)
            DISPLAY.blit(img,(s.x,s.y))


# ==================== SPACEMINE CLASS (from original) ====================
class Spacemine:
    def __init__(s,x,y,player,now,alive, angle=None):
        s.x=x; s.y=y; s.player=player; s.alive=alive
        s.radius=22
        s.angle=angle if angle is not None else random.uniform(0,360)
        rad=s.angle*math.pi/180
        speed=random.uniform(0.4,1.1)
        s.vx=-math.sin(rad)*speed
        s.vy=-math.cos(rad)*speed
        s.last=now
        s.duration=16000
        s.hasexploded=False
        s.image=None

    def update(s):
        if not s.alive: return
        now=pygame.time.get_ticks()
        s.x+=s.vx
        s.y+=s.vy
        if s.x>SW: s.x=0
        if s.x<0: s.x=SW
        if s.y>SH: s.y=0
        if s.y<0: s.y=SH
        elapsed=now-s.last
        stages=[(s.duration-6000,40,30),(s.duration-5000,43,33),(s.duration-4000,46,36),
                (s.duration-3000,49,39),(s.duration-2000,52,42),(s.duration-1000,57,46),(s.duration,63,52)]
        for thresh,size,radius in stages:
            if elapsed<=thresh:
                if s.image:
                    image = pygame.transform.smoothscale(s.image, (size, size))
                    DISPLAY.blit(image, (s.x, s.y))
                else:
                    m_color=S1SM if s.player==1 else S2SM
                    DISPLAY.blit(pygame.transform.scale(m_color, (size, size)), (s.x, s.y))
                s.radius=radius
                return
        s.alive=False


# ==================== PLASMA BEAM CLASS ====================
class PlasmaBeam:
    def __init__(s, x, y, direction, player, target):
        s.x = x
        s.y = y
        s.direction = direction
        s.player = player
        s.target = target
        s.speed = 12
        s.vx = -s.speed * math.sin(math.radians(direction))
        s.vy = -s.speed * math.cos(math.radians(direction))
        s.distance = 0
        s.max_distance = 700
        s.alive = True
        s.hit_applied = False
        s.hit = False
        s.image = pygame.transform.smoothscale(PLASMA_IMG, (48, 48))

    def update(s):
        if not s.alive:
            return False
        s.x += s.vx
        s.y += s.vy
        s.distance += s.speed
        if s.x < -50 or s.x > SW + 50 or s.y < -50 or s.y > SH + 50 or s.distance >= s.max_distance:
            s.alive = False
            return False
        if s.target.alive and s.target.player != s.player:
            dx = s.x - s.target.x
            dy = s.y - s.target.y
            if dx*dx + dy*dy < 30*30:
                s.hit = True
                s.alive = False
        beam = pygame.transform.rotate(s.image, s.direction)
        DISPLAY.blit(beam, (s.x - beam.get_width()//2, s.y - beam.get_height()//2))
        return s.hit


# ==================== EXPLOSION CLASS ====================
class Explode:
    def __init__(s,x,y):
        s.x=x; s.y=y; s.last=pygame.time.get_ticks(); s.dur=1600; s.anim=0
    def update(s):
        now=pygame.time.get_ticks()
        if now%2==0: s.anim+=1
        if s.anim>810: s.anim=0
        if now-s.last<=s.dur:
            DISPLAY.blit(EXG,(s.x-50,s.y-50),
                pygame.Rect((s.anim%9)*133.3,(s.anim//9)*133.3,133.3,133.3))
            return True
        return False


# ==================== LUKAS POWERUP ====================
class LukPowerup:
    def __init__(s):
        s.x=400; s.y=400; s.alive=False
    def update(s,frame):
        if not s.alive: return
        if s.x>SW: s.x=0
        s.x+=0.8
        DISPLAY.blit(LP,(s.x,s.y))
    def check_collision(s,sx,sy,r=20):
        dx=s.x-sx; dy=s.y-sy
        return (dx*dx+dy*dy)<(r+20)**2


# ==================== AI LOGIC (from original) ====================
def ai_update(ai_ship, player_ship, rocket, frame_nr, sw_type, frame_cd, beams):
    """AI control logic matching original exactly"""
    dx = player_ship.x - ai_ship.x
    dy = player_ship.y - ai_ship.y
    dist_to_player = math.sqrt(dx*dx + dy*dy)
    angle_to_player = math.atan2(-dx, -dy) * 180 / math.pi
    if angle_to_player < 0: angle_to_player += 360
    angle_diff = (ai_ship.direction - angle_to_player + 180) % 360 - 180

    should_turn_left = angle_diff > 10 and not (90 < angle_diff < 270)
    should_turn_right = angle_diff < -10 or (90 < angle_diff < 270)
    should_shoot = False

    if should_turn_left:
        ai_ship.change_angle("LEFT", ai_ship.lukas)
    elif should_turn_right:
        ai_ship.change_angle("RIGHT", ai_ship.lukas)
    else:
        ai_ship.boolean = False

    if abs(angle_diff) < 20 and dist_to_player > 100:
        if frame_nr - ai_ship.ai_last_shot > ai_ship.ai_shoot_cooldown:
            should_shoot = True
            ai_ship.ai_last_shot = frame_nr

    new_rocket = rocket
    if should_shoot and not rocket.exists:
        if missileSnd: missileSnd.play()
        new_rocket = Rocket(ai_ship.x, ai_ship.y, ai_ship.direction, True, 2)

    new_frame_cd = frame_cd
    if sw_type == 1:  # Lightspeed
        if 200 < dist_to_player < 350 and abs(angle_diff) < 15:
            if frame_nr > frame_cd + 200:
                kill_bool = ai_ship.start_lightspeed(player_ship)
                if kill_bool[0]:
                    new_frame_cd = frame_nr
    elif sw_type == 2:  # Spacemine
        if frame_nr > frame_cd + 200:
            if dist_to_player < 150:
                new_frame_cd = frame_nr
                return ai_ship.start_spacemine(frame_nr), new_frame_cd, False
    elif sw_type == 3:  # Plasma Blast
        if 150 < dist_to_player < 400 and abs(angle_diff) < 20:
            if frame_nr > frame_cd + 200:
                ai_ship.start_plasma_blast(player_ship, beams)
                new_frame_cd = frame_nr

    return new_rocket, new_frame_cd, should_shoot


# ==================== MAP MANAGER (from original) ====================
class MapManager:
    def __init__(s, name):
        s.name = name
        s.frame_count = 0
        s.gravity_strength = 0.3
        s.gravity_direction = 1
        s.reverse_interval = 15 * 60
        s.reverse_timer = s.reverse_interval

        s.asteroid_images = s._load_asteroid_images()
        s.blackhole_image = s._load_blackhole_image()
        s.background = None
        s.bg_scroll = 0
        s.bg_speed = 0.2
        s.black_holes = []
        s.asteroids = []
        s.reverse_active = False

        if name == "Deep Space Arena":
            s.background = pygame.image.load(ASSET_BACKGROUND_1600).convert()
            s.bg_width = s.background.get_width()
            s.bg_height = s.background.get_height()
            s.stars = []
            for _ in range(140):
                s.stars.append({
                    'x': random.randint(0, SW),
                    'y': random.randint(0, SH),
                    'speed': random.uniform(0.2, 0.6),
                    'brightness': random.randint(150, 255),
                    'size': random.choice([1, 1, 2])
                })
        elif name == "Gravity Chaos Zone":
            s.background = pygame.image.load(ASSET_BACKGROUND_MAP2).convert()
            s.black_holes = [
                {'x': SW // 3, 'y': SH // 3, 'radius': 28},
                {'x': SW * 2 // 3, 'y': SH // 3, 'radius': 28},
                {'x': SW // 2, 'y': SH * 2 // 3, 'radius': 32},
                {'x': SW // 4, 'y': SH * 3 // 4, 'radius': 24},
                {'x': SW * 3 // 4, 'y': SH * 3 // 4, 'radius': 24}
            ]
            s._create_asteroids(14, 18, 26)
        elif name == "Reverse Gravity Zone":
            s.background = pygame.image.load(ASSET_BACKGROUND_MAP3).convert()
            s.black_holes = []
            s._create_asteroids(10, 18, 24)

    def _load_asteroid_images(s):
        images = []
        try:
            if os.path.exists(ASSET_ASTEROIDS_FOLDER):
                for root, _, files in os.walk(ASSET_ASTEROIDS_FOLDER):
                    for f in files:
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                            try:
                                img = pygame.image.load(os.path.join(root, f)).convert_alpha()
                                images.append(img)
                            except Exception:
                                pass
        except Exception:
            pass
        return images

    def _load_blackhole_image(s):
        try:
            img = pygame.image.load(ASSET_BLACKHOLE).convert_alpha()
            return img
        except Exception:
            return None

    def _create_asteroids(s, count, min_radius, max_radius):
        for i in range(count):
            x = random.randint(50, SW - 50)
            y = random.randint(50, SH - 50)
            radius = random.randint(min_radius, max_radius)
            image = None
            mask = None
            if s.asteroid_images:
                orig = random.choice(s.asteroid_images)
                try:
                    image = pygame.transform.smoothscale(orig, (radius * 2, radius * 2))
                    mask = pygame.mask.from_surface(image)
                except Exception:
                    image = None
                    mask = None
            s.asteroids.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-0.8, 0.8),
                'vy': random.uniform(-0.8, 0.8),
                'radius': radius,
                'angle': random.uniform(0, 360),
                'rotation_speed': random.uniform(-2, 2),
                'image': image,
                'mask': mask
            })

    def apply_gravity(s, ship):
        if s.name == "Deep Space Arena":
            return False

        ship_pos = pygame.math.Vector2(ship.x, ship.y)
        total_force = pygame.math.Vector2(0, 0)
        being_consumed = False

        for hole in s.black_holes:
            hole_pos = pygame.math.Vector2(hole['x'], hole['y'])
            direction = hole_pos - ship_pos
            distance = direction.length()
            if distance < 10:
                distance = 10
            if distance > 0:
                direction.normalize_ip()
            force = s.gravity_strength * 10000 / (distance * distance)
            force = min(force, 3)
            total_force += direction * force * s.gravity_direction
            if distance < hole['radius'] + 20:
                being_consumed = True

        ship.x += total_force.x
        ship.y += total_force.y
        return being_consumed

    def update(s):
        s.frame_count += 1
        if s.name == "Deep Space Arena":
            s.bg_scroll -= s.bg_speed
            if s.bg_scroll <= -s.bg_width:
                s.bg_scroll = 0
            for star in s.stars:
                star['y'] += star['speed']
                if star['y'] > SH:
                    star['y'] = 0
                    star['x'] = random.randint(0, SW)
            return

        if s.name == "Reverse Gravity Zone":
            s.reverse_timer -= 1
            if s.reverse_timer <= 0:
                s.reverse_active = not s.reverse_active
                s.reverse_timer = s.reverse_interval

        for a in s.asteroids:
            a['x'] += a['vx']
            a['y'] += a['vy']
            a['angle'] += a['rotation_speed']
            nearest = min(s.black_holes, key=lambda bh: math.hypot(bh['x'] - a['x'], bh['y'] - a['y']))
            dx = nearest['x'] - a['x']
            dy = nearest['y'] - a['y']
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                a['vx'] += (dx / dist) * 0.05
                a['vy'] += (dy / dist) * 0.05
            if a['x'] > SW:
                a['x'] = 0
            elif a['x'] < 0:
                a['x'] = SW
            if a['y'] > SH:
                a['y'] = 0
            elif a['y'] < 0:
                a['y'] = SH

    def draw(s, display):
        if s.background:
            if s.name == "Deep Space Arena":
                display.blit(s.background, (s.bg_scroll, 0))
                display.blit(s.background, (s.bg_scroll + s.bg_width, 0))
            else:
                display.blit(s.background, (0, 0))

        if s.name == "Deep Space Arena":
            for star in s.stars:
                color = (star['brightness'], star['brightness'], star['brightness'])
                pygame.draw.circle(display, color, (int(star['x']), int(star['y'])), star['size'])
            return

        rot = (s.frame_count * 2) % 360
        for hole in s.black_holes:
            if s.blackhole_image:
                size = hole['radius'] * 2
                try:
                    hole_img = pygame.transform.smoothscale(s.blackhole_image, (size, size))
                    rect = hole_img.get_rect(center=(int(hole['x']), int(hole['y'])))
                    display.blit(hole_img, rect)
                except Exception:
                    pygame.draw.circle(display, (0, 0, 0), (int(hole['x']), int(hole['y'])), hole['radius'])
            else:
                pygame.draw.circle(display, (0, 0, 0), (int(hole['x']), int(hole['y'])), hole['radius'])
            pygame.draw.circle(display, (100, 0, 150), (int(hole['x']), int(hole['y'])), hole['radius'], 3)

        if s.name == "Reverse Gravity Zone":
            col = (100, 255, 100) if not s.reverse_active else (255, 100, 100)
            txt = "NORMAL" if not s.reverse_active else "REVERSED"
            text = F.render(txt, True, col)
            display.blit(text, (SW // 2 - text.get_width() // 2, 40))
            timer_text = F.render(f"Next flip in: {max(0, s.reverse_timer // 60)}s", True, WHITE)
            display.blit(timer_text, (SW // 2 - timer_text.get_width() // 2, 70))

        for a in s.asteroids:
            if a['image']:
                rotated = pygame.transform.rotate(a['image'], -a['angle'])
                rect = rotated.get_rect(center=(int(a['x']), int(a['y'])))
                display.blit(rotated, rect)
            else:
                x, y, r = int(a['x']), int(a['y']), a['radius']
                pygame.draw.circle(display, (139, 125, 107), (x, y), r)
                pygame.draw.circle(display, (100, 90, 80), (x, y), r - 3)
                pygame.draw.circle(display, (80, 70, 60), (x - r // 3, y - r // 3), r // 4)


# ==================== INTRO ====================
def intro(ships):
    txt="ready up"
    i=SH
    while True:
        if i>100: i-=1
        DISPLAY.fill(BLACK)
        DISPLAY.blit(BG,(0,0))
        if i>400: c=WHITE
        elif i>300: c=RED
        elif i>200: c=ORANGE
        else: c=GREEN
        p1_txt=SF.render(txt,True,c)
        if i>200: j=i
        DISPLAY.blit(p1_txt,(250,j))
        for s in ships: s.move()
        scale_display()
        fpsClock.tick(60)
        if i<110: break


# ==================== ENDGAME SCREEN ====================
def endgame(p1s,p2s):
    global GAME_MODE, PLAYER1_NAME, PLAYER2_NAME
    if p1s>p2s:
        winner=1; wt=f"BLUE ({PLAYER1_NAME}) WON!"; wc=CYAN
    elif p2s>p1s:
        winner=2
        if GAME_MODE=="PVE": wt="RED (AI BOT) WON!"
        else: wt=f"RED ({PLAYER2_NAME}) WON!"
        wc=RED
    else:
        winner=0; wt="DRAW!"; wc=WHITE

    buttons=[("RESTART","restart"),("MENU","menu"),("QUIT","quit")]
    sel=0

    while True:
        DISPLAY.fill((5,10,30))

        # Grid
        for x in range(0,SW,50): pygame.draw.line(DISPLAY,(0,100,150),(x,0),(x,SH),1)
        for y in range(0,SH,50): pygame.draw.line(DISPLAY,(0,100,150),(0,y),(SW,y),1)

        # Title
        title=SF.render("GAME OVER",True,CYAN)
        DISPLAY.blit(title,(SW//2-title.get_width()//2,50))

        # Winner
        wt_render=BF.render(wt,True,wc)
        DISPLAY.blit(wt_render,(SW//2-wt_render.get_width()//2,120))

        # Scores
        pygame.draw.rect(DISPLAY,(0,50,80),(150,200,200,100),border_radius=15)
        pygame.draw.rect(DISPLAY,CYAN,(150,200,200,100),2,border_radius=15)
        DISPLAY.blit(F.render(f"P1: {p1s}",True,WHITE),(200,240))

        pygame.draw.rect(DISPLAY,(80,20,20),(450,200,200,100),border_radius=15)
        pygame.draw.rect(DISPLAY,RED,(450,200,200,100),2,border_radius=15)
        DISPLAY.blit(F.render(f"P2: {p2s}",True,WHITE),(500,240))

        # Buttons
        for i,(txt,act) in enumerate(buttons):
            y=350+i*60
            col=(0,200,200) if i==sel else (100,100,100)
            pygame.draw.rect(DISPLAY,col,(SW//2-100,y,200,40),border_radius=5)
            t=F.render(txt,True,WHITE)
            DISPLAY.blit(t,(SW//2-t.get_width()//2,y+10))

        scale_display()

        for e in pygame.event.get():
            if e.type==QUIT: pygame.quit(); sys.exit()
            if e.type==VIDEORESIZE: handle_resize(e)
            if e.type==KEYDOWN:
                if e.key==K_ESCAPE: pygame.quit(); sys.exit()
                if e.key==K_UP: sel=(sel-1)%3
                if e.key==K_DOWN: sel=(sel+1)%3
                if e.key==K_RETURN:
                    if sel==0: main(); return
                    if sel==1: run_menu(); return
                    if sel==2: pygame.quit(); sys.exit()


# ==================== MENU SCREENS ====================
def enter_player_names(mode):
    global PLAYER1_NAME, PLAYER2_NAME
    clock = pygame.time.Clock()
    pygame.key.set_repeat(0)
    active = 1
    name1 = PLAYER1_NAME if PLAYER1_NAME != "Player 1" else ""
    name2 = PLAYER2_NAME if PLAYER2_NAME != "Player 2" else ""
    if mode == "PVE":
        name2 = "AI BOT"
    while True:
        DISPLAY.fill(BLACK)
        prompt = "Enter Player 1 Name:" if active == 1 else "Enter Player 2 Name:"
        text_prompt = BF.render(prompt, True, WHITE)
        DISPLAY.blit(text_prompt, (100, 150))
        current = name1 if active == 1 else name2
        input_box = BF.render(current + "_", True, CYAN)
        DISPLAY.blit(input_box, (100, 200))
        hint = F.render("Type name, ENTER to continue, BACKSPACE to erase", True, (180, 180, 180))
        DISPLAY.blit(hint, (100, 260))
        if mode == "PVE":
            info = F.render("Player 2 will be AI BOT", True, (180, 180, 180))
            DISPLAY.blit(info, (100, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == VIDEORESIZE:
                handle_resize(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return PLAYER1_NAME, PLAYER2_NAME
                if event.key in (K_RETURN, K_KP_ENTER):
                    if active == 1:
                        if not name1.strip():
                            name1 = "Player 1"
                        if mode == "PVP":
                            active = 2
                        else:
                            PLAYER1_NAME = name1.strip()
                            PLAYER2_NAME = "AI BOT"
                            return PLAYER1_NAME, PLAYER2_NAME
                    elif active == 2:
                        if not name2.strip():
                            name2 = "Player 2"
                        PLAYER1_NAME = name1.strip() if name1.strip() else "Player 1"
                        PLAYER2_NAME = name2.strip()
                        return PLAYER1_NAME, PLAYER2_NAME
                elif event.key == K_BACKSPACE:
                    if active == 1:
                        name1 = name1[:-1]
                    else:
                        name2 = name2[:-1]
                elif event.unicode.isprintable() and len(event.unicode) == 1:
                    if active == 1 and len(name1) < 12:
                        name1 += event.unicode
                    elif active == 2 and len(name2) < 12:
                        name2 += event.unicode
        clock.tick(FPS)

def normalize_stats(s):
    """Convert stats to list format [?,speed,?,money,maneuver,?,?,rocket,?,super]"""
    if isinstance(s, dict):
        # Convert dict to list format
        sw_val = 3 if s.get("super") == "Plasma Blast" else 1 if s.get("super") == "Light Speed" else 2 if s.get("super") in ("Naval Mine", "Spacemine") else 1
        return [1, int(s.get("speed",1)), 1, 1000, int(s.get("maneuver",1)), 1, 1, int(s.get("rocket",1)), 1, sw_val]
    elif isinstance(s, list):
        return s
    return [1,1,1,1000,1,1,1,1,1,1]

def run_menu():
    global GAME_MODE, SELECTED_MAP, PLAYER1_NAME, PLAYER2_NAME
    global shipspeed, maneuv, rocketspeed, superweapon

    while True:
        # Main Menu - select PvP or PvE
        menu=MainMenu(WINDOW,VS)
        mode=menu.show()
        if mode is None: pygame.quit(); sys.exit()
        GAME_MODE=mode

        # Player name entry
        PLAYER1_NAME, PLAYER2_NAME = enter_player_names(GAME_MODE)
        # Map Select - show mode name in title
        mode_name = "PLAYER VS PLAYER" if GAME_MODE=="PVP" else "PLAYER VS ENVIRONMENT"
        map_sel=MapSelect(WINDOW,VS)
        mresult=map_sel.show(mode_name=mode_name, p1_name=PLAYER1_NAME, p2_name=PLAYER2_NAME)
        if mresult is None: continue
        if mresult=="back": continue
        SELECTED_MAP=mresult

        # Load stats
        stats1=load_stats(1); stats2=load_stats(2)
        try:
            S1_raw=eval(stats1) if isinstance(stats1,str) else [1,1,1,1000,1]
            S2_raw=eval(stats2) if isinstance(stats2,str) else [1,1,1,1000,1]
        except: S1_raw=S2_raw=[1,1,1,1000,1]
        S1=normalize_stats(S1_raw)
        S2=normalize_stats(S2_raw)

        # Upgrade Screen flow per spec:
        # PvP: Both players get upgrade screen
        # PvE: Only Player 1 gets upgrade, AI auto-generates
        
        # Player 1 Upgrade (always)
        up1=UpgradeScreen(WINDOW,VS,1)
        u1=up1.show()
        if u1 is None: continue  # ESC pressed - back to menu
        save_stats(1,u1)

        if GAME_MODE=="PVP":
            # PvP: Player 2 also gets upgrade screen
            up2=UpgradeScreen(WINDOW,VS,2)
            u2=up2.show()
            if u2 is None: continue
            save_stats(2,u2)
        else:
            # PvE: AI auto-generates stats
            up2=UpgradeScreen(WINDOW,VS,2,is_ai=True)
            u2=up2.show()
            save_stats(2,u2)

        # Re-load and normalize after saving
        stats1=load_stats(1); stats2=load_stats(2)
        try:
            S1_raw=eval(stats1) if isinstance(stats1,str) else [1,1,1,1000,1]
            S2_raw=eval(stats2) if isinstance(stats2,str) else [1,1,1,1000,1]
        except: S1_raw=S2_raw=[1,1,1,1000,1]
        S1=normalize_stats(S1_raw)
        S2=normalize_stats(S2_raw)

        shipspeed=[int(S1[1]),int(S2[1])]
        maneuv=[int(S1[4]),int(S2[4])]
        rocketspeed=[int(S1[7]) if len(S1)>7 else 1,int(S2[7]) if len(S2)>7 else 1]
        superweapon=[int(S1[-1]) if len(S1)>9 else 1,int(S2[-1]) if len(S2)>9 else 1]

        main()


# ==================== MAIN GAME LOOP ====================
def main():
    global GAME_MODE, shipspeed, maneuv, rocketspeed, superweapon

    # Load stats
    stats1=load_stats(1); stats2=load_stats(2)
    try:
        S1_raw=eval(stats1) if isinstance(stats1,str) else [1,1,1,1000,1]
        S2_raw=eval(stats2) if isinstance(stats2,str) else [1,1,1,1000,1]
    except: S1_raw=S2_raw=[1,1,1,1000,1]
    
    S1=normalize_stats(S1_raw)
    S2=normalize_stats(S2_raw)

    shipspeed=[int(S1[1]),int(S2[1])]
    maneuv=[int(S1[4]),int(S2[4])]
    rocketspeed=[int(S1[7]) if len(S1)>7 else 1,int(S2[7]) if len(S2)>7 else 1]
    superweapon=[int(S1[-1]) if len(S1)>9 else 1,int(S2[-1]) if len(S2)>9 else 1]

    # Init map
    map_mgr=MapManager(SELECTED_MAP)

    # Init entities
    if missileSnd: missileSnd.set_volume(0.1)
    if explosionSnd: explosionSnd.set_volume(0.3)
    try:
        pygame.mixer.music.play(0,0)
    except:
        pass
    
    # Enable key repeat for gameplay (delay=100ms, interval=50ms)
    pygame.key.set_repeat(100, 50)

    x,y=SW,SH
    ship1=Ship(x*0.8,y*0.8,1)
    ship2=Ship(x*0.2,y*0.8,2)

    rocket1=Rocket(999,999,0,False,1)
    rocket2=Rocket(999,999,0,False,2)

    explosions=[]
    explosion1=Explode(x+500,y+500)
    explosion2=Explode(x+500,y+500)
    explosion_super1=Explode(x+500,y+500)
    explosion_super2=Explode(x+500,y+500)

    spacemines=[]
    plasma_beams=[]
    luk=LukPowerup()
    luk_init=False; luk.alive=False

    p1_score=0; p2_score=0
    frame_nr=0; frame_cd1=0; frame_cd2=0
    intro_played=False
    frame_start=0

    # MAIN LOOP
    while True:
        frame_nr+=1
        DISPLAY.fill(BLACK)

        # Update map
        if map_mgr:
            map_mgr.update()
            if map_mgr.name == "Reverse Gravity Zone":
                ship1.control_reversed = map_mgr.reverse_active
                ship2.control_reversed = map_mgr.reverse_active
            else:
                ship1.control_reversed = False
                ship2.control_reversed = False
            map_mgr.apply_gravity(ship1)
            map_mgr.apply_gravity(ship2)
            map_mgr.draw(DISPLAY)

        # Update ships
        ship1.move(); ship2.move()
        ship1.change_angle2(); ship2.change_angle2()

        # Update rockets
        rocket1.move(); rocket2.move()

        # Update plasma beams
        for beam in plasma_beams[:]:
            beam.update()
            if beam.hit and not beam.hit_applied:
                beam.hit_applied = True
                explosions.append(Explode(beam.target.x, beam.target.y))
                if explosionSnd: explosionSnd.play()
                if beam.target.player == 1:
                    ship1 = Ship(x*0.8, y*0.8, 1)
                    p1_score -= 2; p2_score += 2
                else:
                    ship2 = Ship(x*0.2, y*0.8, 2)
                    p2_score -= 2; p1_score += 2
            if not beam.alive:
                plasma_beams.remove(beam)

        # AI Update
        if GAME_MODE=="PVE":
            rocket2,frame_cd2,new_mines=ai_update(ship2,ship1,rocket2,frame_nr,superweapon[1],frame_cd2,plasma_beams)
            if isinstance(new_mines, list):
                spacemines.extend(new_mines)

        # Update spacemines
        for mine in spacemines[:]:
            mine.update()
            if mine.alive:
                # Check collision with ships
                for ship,idx in [(ship1,1),(ship2,2)]:
                    if ship.alive and mine.player!=idx:
                        pt_mine=Point(mine.x+mine.radius,mine.y+mine.radius)
                        pt_ship=Point(ship.x,ship.y)
                        if dist(pt_mine,pt_ship)<mine.radius+20:
                            if mine in spacemines: spacemines.remove(mine)
                            explosions.append(Explode(ship.x,ship.y))
                            if explosionSnd: explosionSnd.play()
                            if idx==1:
                                ship1=Ship(x*0.8,y*0.8,1)
                                p1_score-=1; p2_score+=3
                            else:
                                ship2=Ship(x*0.2,y*0.8,2)
                                p2_score-=1; p1_score+=3
                            break
            else: mine.hasexploded=True

        # Update explosions
        explosions=[e for e in explosions if e.update()]

        # Update powerup
        luk.update(frame_nr)
        if not luk.alive and frame_nr%100==0:
            luk.x=random.choice(range(0,10))*80
            luk.y=random.choice(range(0,10))*60
        if frame_nr>300 and not luk_init:
            luk.alive=True; luk_init=True

        # Draw scores
        DISPLAY.blit(BF.render(f" {p1_score} ",True,WHITE,BLUE),(SW-100,50))
        DISPLAY.blit(BF.render(f" {p2_score} ",True,WHITE,RED),(50,50))
        DISPLAY.blit(SF2.render(f"Mode: {GAME_MODE}",True,WHITE),(SW//2-40,10))

        # Draw superweapon info for both players
        weapon_names = {1: "Light Speed", 2: "Naval Mine", 3: "Plasma Blast"}
        
        # Player 1 superweapon (top left)
        p1_weapon = weapon_names.get(superweapon[0], "Unknown")
        p1_cooldown_remaining = max(0, frame_cd1 + 300 - frame_nr)
        p1_ready = "READY" if p1_cooldown_remaining == 0 else f"COOLDOWN {p1_cooldown_remaining//60}s"
        DISPLAY.blit(F.render(f"P1 SW: {p1_weapon}", True, CYAN), (50, 80))
        DISPLAY.blit(F.render(p1_ready, True, GREEN if p1_cooldown_remaining == 0 else ORANGE), (50, 100))
        
        # Player 2 superweapon (top right)
        p2_weapon = weapon_names.get(superweapon[1], "Unknown")
        p2_cooldown_remaining = max(0, frame_cd2 + 300 - frame_nr)
        p2_ready = "READY" if p2_cooldown_remaining == 0 else f"COOLDOWN {p2_cooldown_remaining//60}s"
        DISPLAY.blit(F.render(f"P2 SW: {p2_weapon}", True, RED), (SW-150, 80))
        DISPLAY.blit(F.render(p2_ready, True, GREEN if p2_cooldown_remaining == 0 else ORANGE), (SW-150, 100))

        # Auto-activate superweapons when cooldown is ready
        # P1 auto-activate
        if ship1.alive and frame_nr > frame_cd1 + 300:
            if superweapon[0] == 1:  # Lightspeed
                ship1.start_lightspeed(ship2)
                frame_cd1 = frame_nr
            elif superweapon[0] == 2:  # Spacemine
                spacemines.extend(ship1.start_spacemine(frame_nr))
                frame_cd1 = frame_nr
            elif superweapon[0] == 3:  # Plasma Blast
                ship1.start_plasma_blast(ship2, plasma_beams)
                frame_cd1 = frame_nr

        # P2 auto-activate (only in PvP mode)
        if GAME_MODE == "PVP" and ship2.alive and frame_nr > frame_cd2 + 300:
            if superweapon[1] == 1:  # Lightspeed
                ship2.start_lightspeed(ship1)
                frame_cd2 = frame_nr
            elif superweapon[1] == 2:  # Spacemine
                spacemines.extend(ship2.start_spacemine(frame_nr))
                frame_cd2 = frame_nr
            elif superweapon[1] == 3:  # Plasma Blast
                ship2.start_plasma_blast(ship1, plasma_beams)
                frame_cd2 = frame_nr

        # Win check (difference > 20 like original)
        if p1_score>p2_score+20: endgame(p1_score,p2_score); return
        if p2_score>p1_score+20: endgame(p1_score,p2_score); return

        # COLLISION DETECTION (exactly like original)
        # Ship-ship collision
        col_x12=ship1.x<ship2.x+30 and ship1.x>ship2.x-30
        col_y12=ship1.y<ship2.y+30 and ship1.y>ship2.y-30
        col12=col_x12 and col_y12

        # Rocket collisions (original: ±25 box)
        col_x1r2=ship2.x<rocket1.x+25 and ship2.x>rocket1.x-25
        col_y1r2=ship2.y<rocket1.y+25 and ship2.y>rocket1.y-25
        col1r2=col_x1r2 and col_y1r2 and rocket1.exists

        col_x2r1=ship1.x<rocket2.x+25 and ship1.x>rocket2.x-25
        col_y2r1=ship1.y<rocket2.y+25 and ship1.y>rocket2.y-25
        col2r1=col_x2r1 and col_y2r1 and rocket2.exists

        # Powerup collisions (±30 box)
        col_luk1=ship1.x<luk.x+30 and ship1.x>luk.x-30 and ship1.y<luk.y+30 and ship1.y>luk.y-30
        col_luk2=ship2.x<luk.x+30 and ship2.x>luk.x-30 and ship2.y<luk.y+30 and ship2.y>luk.y-30

        # Asteroid collisions
        ast_col1=ast_col2=False
        if map_mgr and map_mgr.name in ["Gravity Chaos Zone","Reverse Gravity Zone"]:
            for a in map_mgr.asteroids:
                dx1=ship1.x-a['x']; dy1=ship1.y-a['y']
                if math.sqrt(dx1*dx1+dy1*dy1)<a['radius']+20:
                    ast_col1=True; explosion1=Explode(ship1.x,ship1.y)
                    if explosionSnd: explosionSnd.play()
                    ship1=Ship(x*0.8,y*0.8,1)
                    p1_score-=1; p2_score+=3
                    break
                dx2=ship2.x-a['x']; dy2=ship2.y-a['y']
                if math.sqrt(dx2*dx2+dy2*dy2)<a['radius']+20:
                    ast_col2=True; explosion2=Explode(ship2.x,ship2.y)
                    if explosionSnd: explosionSnd.play()
                    ship2=Ship(x*0.2,y*0.8,2)
                    p2_score-=1; p1_score+=3
                    break

        # Handle collisions (exactly like original)
        if col12:
            explosion1=Explode((ship1.x+ship2.x)/2,(ship1.y+ship2.y)/2)
            if explosionSnd: explosionSnd.play()
            ship1=Ship(x*0.8,y*0.8,1); ship2=Ship(x*0.2,y*0.8,2)
            p1_score-=1; p2_score-=1

        elif col2r1:
            explosion2=Explode(rocket2.x,rocket2.y)
            if explosionSnd: explosionSnd.play()
            rocket2=Rocket(999,999,0,False,2)
            ship1=Ship(x*0.8,y*0.8,1)
            p1_score-=1; p2_score+=3

        elif col1r2:
            explosion1=Explode(rocket1.x,rocket1.y)
            if explosionSnd: explosionSnd.play()
            rocket1=Rocket(999,999,0,False,1)
            ship2=Ship(x*0.2,y*0.8,2)
            p2_score-=1; p1_score+=3

        # Powerup effects
        if col_luk1 and luk.alive:
            ship2.lukas=True; luk.alive=False; frame_start=frame_nr
        if col_luk2 and luk.alive:
            ship1.lukas=True; luk.alive=False; frame_start=frame_nr

        # Reset debuff after 200 frames (~3.3s)
        if frame_nr>frame_start+200:
            ship1.lukas=False; ship2.lukas=False
        if frame_nr>frame_start+750:
            luk.alive=True

        # Event handling
        for e in pygame.event.get():
            if e.type==QUIT: pygame.quit(); sys.exit()
            if e.type==VIDEORESIZE: handle_resize(e)
            if not hasattr(e,'key'): continue
            if e.type==KEYDOWN:
                if e.key==K_ESCAPE: run_menu(); return

                # P1 controls (always human)
                if e.key==K_RIGHT: ship1.change_angle("RIGHT",ship1.lukas)
                if e.key==K_LEFT: ship1.change_angle("LEFT",ship1.lukas)
                if e.key==K_UP:
                    if missileSnd: missileSnd.play()
                    rocket1=Rocket(ship1.x,ship1.y,ship1.direction,True,1)

                # P1 superweapon - now auto-activates, key press removed

                # P2 controls (only PvP)
                if GAME_MODE=="PVP":
                    if e.key==K_d: ship2.change_angle("RIGHT",ship2.lukas)
                    if e.key==K_a: ship2.change_angle("LEFT",ship2.lukas)
                    if e.key==K_w:
                        if missileSnd: missileSnd.play()
                        rocket2=Rocket(ship2.x,ship2.y,ship2.direction,True,2)

                    # P2 superweapon - now auto-activates, key press removed

            elif e.type==KEYUP:
                if e.key==K_RIGHT: ship1.change_angle("RIGHT2",ship1.lukas)
                if e.key==K_LEFT: ship1.change_angle("LEFT2",ship1.lukas)
                if GAME_MODE=="PVP":
                    if e.key==K_a: ship2.change_angle("LEFT2",ship2.lukas)
                    if e.key==K_d: ship2.change_angle("RIGHT2",ship2.lukas)

        scale_display()
        fpsClock.tick(60)

        if not intro_played:
            intro([ship1,ship2])
            intro_played=True


if __name__=="__main__":
    run_menu()




