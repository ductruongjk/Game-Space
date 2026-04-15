#!/usr/bin/env python3
"""Space Shooter - Based on space-fighters-master original rules"""
import sys
import pygame
import math
import random
from pygame.locals import *

sys.path.insert(0, '.')
from settings import *
from entities import Ship, Rocket, Spacemine, Explode, LukPowerup
from maps import DeepSpaceMap, GravityChaosMap, ReverseGravityMap
from screens import MainMenu, ModeSelect, MapSelect, UpgradeScreen

# ==================== INITIALIZE ====================
pygame.init()
SW, SH = 800, 600
WINDOW = pygame.display.set_mode((SW, SH), pygame.RESIZABLE)
pygame.display.set_caption("Space Shooter")
try:
    pygame.display.set_icon(pygame.image.load('resources/ship1big.png'))
except:
    pass
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(0)
pygame.key.set_repeat(1, 10)

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
    pygame.mixer.music.load("resources/bg_music.mp3")
    missileSnd = pygame.mixer.Sound('resources/missile.wav')
    explosionSnd = pygame.mixer.Sound('resources/explosion.wav')
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
    BG = pygame.image.load('resources/background1600.png')
    S1 = pygame.image.load('resources/ship1.png')
    S2 = pygame.image.load('resources/ship2.png')
    R1 = pygame.image.load('resources/rocket1.png')
    R2 = pygame.image.load('resources/rocket2.png')
    EG = pygame.image.load('resources/endgamescreen1600.png')
    LP = pygame.image.load('resources/lukas_powerup.png')
    EXG = pygame.image.load('resources/explosion_anim_1200x1200.png')
    RG = pygame.image.load('resources/respawn_anim_900x900_test.png')
    S1LS = pygame.image.load('resources/ship1_lightspeed.png')
    S2LS = pygame.image.load('resources/ship2_lightspeed.png')
    S1SM = pygame.image.load('resources/spacemine1.png')
    S2SM = pygame.image.load('resources/spacemine2.png')
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
            s.x+=-s.speed*math.sin(rad)
            s.y+=-s.speed*math.cos(rad)
            if s.x>SW: s.x=0
            if s.x<0: s.x=SW
            if s.y>SH: s.y=0
            if s.y<0: s.y=SH
            img=pygame.transform.rotate(S1 if s.player==1 else S2, s.direction)
            s.image=img
            DISPLAY.blit(img,(s.x,s.y))
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
            s.ls_alive=True
            s.ls_start=[s.x,s.y]
            rad=s.direction*math.pi/180
            s.ls_end=[s.x+50*(-s.speed*math.sin(rad)),s.y+50*(-s.speed*math.cos(rad))]
            img=pygame.transform.rotate(S1LS if s.player==1 else S2LS, s.direction)
            DISPLAY.blit(img,(s.x,s.y))
            p_start=Point(s.ls_start[0],s.ls_start[1])
            p_end=Point(s.ls_end[0],s.ls_end[1])
            p_other=Point(other.x,other.y)
            hit=lies_btwn(p_other,p_start,p_end) and (dist(p_end,p_other)<100 or dist(p_start,p_other)<100)
            s.alive=False
            return [hit,False,False]
        return [False,False,False]

    def stop_lightspeed(s):
        if not s.alive and s.ls_alive:
            s.ls_alive=False
            s.alive=True
            s.x=s.ls_end[0]
            s.y=s.ls_end[1]

    def start_spacemine(s,frame_nr):
        return Spacemine(s.x,s.y,s.k_left,s.k_right,s.speed,s.player,frame_nr,True)


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
    def __init__(s,x,y,left,right,spd,p,now,alive):
        s.x=x; s.y=y; s.direction=left+right; s.alive=alive
        s.speed=0.2*spd; s.player=p; s.radius=20
        s.last=pygame.time.get_ticks()
        s.duration=16000
        s.hasexploded=False

    def update(s):
        if not s.alive: return
        now=pygame.time.get_ticks()
        rad=s.direction*math.pi/180
        s.x+=-s.speed*math.sin(rad)
        s.y+=-s.speed*math.cos(rad)
        if s.x>SW: s.x=0
        if s.x<0: s.x=SW
        if s.y>SH: s.y=0
        if s.y<0: s.y=SH
        m_color=S1SM if s.player==1 else S2SM
        elapsed=now-s.last
        stages=[(s.duration-6000,40,30),(s.duration-5000,43,33),(s.duration-4000,46,36),
                (s.duration-3000,49,39),(s.duration-2000,52,42),(s.duration-1000,57,46),(s.duration,63,52)]
        for thresh,size,radius in stages:
            if elapsed<=thresh:
                DISPLAY.blit(pygame.transform.scale(m_color,(size,size)),(s.x,s.y))
                s.radius=radius
                return
        s.alive=False


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
def ai_update(ai_ship, player_ship, rocket, frame_nr, sw_type, frame_cd):
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
                rad = ai_ship.direction * math.pi / 180
                ls_end_x = ai_ship.x + 50 * (-ai_ship.speed * math.sin(rad))
                ls_end_y = ai_ship.y + 50 * (-ai_ship.speed * math.cos(rad))
                end_dist = math.sqrt((ls_end_x - player_ship.x)**2 + (ls_end_y - player_ship.y)**2)
                if end_dist < 100:
                    kill_bool = ai_ship.start_lightspeed(player_ship)
                    if kill_bool[0]:
                        new_frame_cd = frame_nr
    elif sw_type == 2:  # Spacemine
        if frame_nr > frame_cd + 200:
            if dist_to_player < 150:
                new_frame_cd = frame_nr
                return ai_ship.start_spacemine(frame_nr), new_frame_cd, False

    return new_rocket, new_frame_cd, should_shoot


# ==================== MAP MANAGER (from original) ====================
class MapManager:
    def __init__(s, name):
        s.name=name; s.frame_count=0
        s.black_hole_x=SW//2; s.black_hole_y=SH//2
        s.black_hole_radius=50; s.gravity_strength=0.3
        s.gravity_direction=1
        s.reverse_interval=14*60; s.reverse_timer=s.reverse_interval
        s.asteroids=[]
        if name in ["Gravity Chaos Zone","Reverse Gravity Zone"]:
            for i in range(8):
                angle=random.uniform(0,2*math.pi)
                dist=random.randint(150,280)
                s.asteroids.append({
                    'x':s.black_hole_x+math.cos(angle)*dist,
                    'y':s.black_hole_y+math.sin(angle)*dist,
                    'vx':random.uniform(-0.8,0.8),'vy':random.uniform(-0.8,0.8),
                    'radius':random.randint(18,28),'angle':random.uniform(0,360)
                })

    def apply_gravity(s, ship):
        if s.name=="Deep Space Arena": return
        dx=s.black_hole_x-ship.x; dy=s.black_hole_y-ship.y
        distance=math.sqrt(dx*dx+dy*dy)
        if distance<10: distance=10
        force=s.gravity_strength*10000/(distance*distance)
        if force>3: force=3
        nx=dx/distance; ny=dy/distance
        ship.x+=nx*force*s.gravity_direction
        ship.y+=ny*force*s.gravity_direction

    def update(s):
        s.frame_count+=1
        if s.name=="Reverse Gravity Zone":
            s.reverse_timer-=1
            if s.reverse_timer<=0:
                s.gravity_direction*=-1; s.reverse_timer=s.reverse_interval
        for a in s.asteroids:
            a['x']+=a['vx']; a['y']+=a['vy']; a['angle']+=1
            dx=s.black_hole_x-a['x']; dy=s.black_hole_y-a['y']
            dist=math.sqrt(dx*dx+dy*dy)
            if dist>0: a['vx']+=(dx/dist)*0.05; a['vy']+=(dy/dist)*0.05
            if a['x']>SW: a['x']=0
            elif a['x']<0: a['x']=SW
            if a['y']>SH: a['y']=0
            elif a['y']<0: a['y']=SH

    def draw(s, display):
        if s.name=="Deep Space Arena": return
        rot=(s.frame_count*2)%360
        for i in range(5,0,-1):
            radius=s.black_hole_radius+i*15
            color=(50+i*20,0,100+i*30)
            pygame.draw.circle(display,color,(int(s.black_hole_x),int(s.black_hole_y)),radius)
        pygame.draw.circle(display,(0,0,0),(int(s.black_hole_x),int(s.black_hole_y)),s.black_hole_radius)
        pygame.draw.circle(display,(100,0,150),(int(s.black_hole_x),int(s.black_hole_y)),s.black_hole_radius,3)
        for arm in range(4):
            arm_angle=math.radians(rot+arm*90)
            sx=s.black_hole_x+math.cos(arm_angle)*30
            sy=s.black_hole_y+math.sin(arm_angle)*30
            ex=s.black_hole_x+math.cos(arm_angle)*60
            ey=s.black_hole_y+math.sin(arm_angle)*60
            pygame.draw.line(display,(150,50,200),(sx,sy),(ex,ey),3)
        if s.name=="Reverse Gravity Zone":
            col=(100,255,100) if s.gravity_direction==1 else (255,100,100)
            txt="PULL" if s.gravity_direction==1 else "PUSH"
            text=F.render(txt,True,col)
            display.blit(text,(s.black_hole_x-20,s.black_hole_y-70))
        for a in s.asteroids:
            x,y=int(a['x']),int(a['y']); r=a['radius']
            pygame.draw.circle(display,(139,125,107),(x,y),r)
            pygame.draw.circle(display,(100,90,80),(x,y),r-3)
            pygame.draw.circle(display,(80,70,60),(x-r//3,y-r//3),r//4)


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
def normalize_stats(s):
    """Convert stats to list format [?,speed,?,money,maneuver,?,?,rocket,?,super]"""
    if isinstance(s, dict):
        # Convert dict to list format
        sw_val=1 if s.get("super")=="Light Speed" else 2 if s.get("super")=="Spacemine" else 1
        return [1, int(s.get("speed",1)), 1, 1000, int(s.get("maneuver",1)), 1, 1, int(s.get("rocket",1)), 1, sw_val]
    elif isinstance(s, list):
        return s
    return [1,1,1,1000,1,1,1,1,1,1]

def run_menu():
    global GAME_MODE, SELECTED_MAP, PLAYER1_NAME, PLAYER2_NAME
    global shipspeed, maneuv, rocketspeed, superweapon

    while True:
        menu=MainMenu(WINDOW,VS)
        mode=menu.show()
        if mode is None: pygame.quit(); sys.exit()
        GAME_MODE=mode

        mode_sel=ModeSelect(WINDOW,VS)
        result=mode_sel.show()
        if result is None: continue
        if result=="back": continue

        map_sel=MapSelect(WINDOW,VS)
        mresult=map_sel.show()
        if mresult is None: continue
        if mresult=="back": continue
        SELECTED_MAP=mresult

        # Upgrades
        stats1=load_stats(1); stats2=load_stats(2)
        try:
            S1_raw=eval(stats1) if isinstance(stats1,str) else [1,1,1,1000,1]
            S2_raw=eval(stats2) if isinstance(stats2,str) else [1,1,1,1000,1]
        except: S1_raw=S2_raw=[1,1,1,1000,1]

        # Convert to list format
        S1=normalize_stats(S1_raw)
        S2=normalize_stats(S2_raw)

        up1=UpgradeScreen(WINDOW,VS,1)
        u1=up1.show()
        if u1 is None: continue
        save_stats(1,u1)

        if GAME_MODE=="PVP":
            up2=UpgradeScreen(WINDOW,VS,2)
            u2=up2.show()
            if u2 is None: continue
            save_stats(2,u2)
        else:
            up2=UpgradeScreen(WINDOW,VS,2,is_ai=True)
            u2=up2.show()  # AI auto-generates stats
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
        superweapon=[int(S1[-2]) if len(S1)>=2 else 1,int(S2[-2]) if len(S2)>=2 else 1]

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
    superweapon=[int(S1[-2]) if len(S1)>=2 else 1,int(S2[-2]) if len(S2)>=2 else 1]

    # Init map
    map_mgr=MapManager(SELECTED_MAP)

    # Init entities
    if missileSnd: missileSnd.set_volume(0.1)
    if explosionSnd: explosionSnd.set_volume(0.3)
    pygame.mixer.music.play(0,0)

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
        DISPLAY.blit(BG,(0,0))

        # Update map
        if map_mgr:
            map_mgr.update()
            map_mgr.apply_gravity(ship1)
            map_mgr.apply_gravity(ship2)
            map_mgr.draw(DISPLAY)

        # Update ships
        ship1.move(); ship2.move()
        ship1.change_angle2(); ship2.change_angle2()

        # Update rockets
        rocket1.move(); rocket2.move()

        # AI Update
        if GAME_MODE=="PVE":
            rocket2,frame_cd2,_=ai_update(ship2,ship1,rocket2,frame_nr,superweapon[1],frame_cd2)
            ship2.stop_lightspeed()

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

                # P1 superweapon
                if e.key==K_DOWN:
                    if superweapon[0]==1:  # Lightspeed
                        if frame_nr>frame_cd1+200 and ship1.alive:
                            kb=ship1.start_lightspeed(ship2)
                            if kb[0]:
                                explosion_super1=Explode(ship2.x,ship2.y)
                                if explosionSnd: explosionSnd.play()
                                ship2=Ship(x*0.2,y*0.8,2)
                                p2_score-=1; p1_score+=3
                            frame_cd1=frame_nr
                        ship1.stop_lightspeed()
                    elif superweapon[0]==2:  # Spacemine
                        if frame_nr>frame_cd1+200 and ship1.alive:
                            frame_cd1=frame_nr
                            spacemines.append(ship1.start_spacemine(frame_nr))

                # P2 controls (only PvP)
                if GAME_MODE=="PVP":
                    if e.key==K_d: ship2.change_angle("RIGHT",ship2.lukas)
                    if e.key==K_a: ship2.change_angle("LEFT",ship2.lukas)
                    if e.key==K_w:
                        if missileSnd: missileSnd.play()
                        rocket2=Rocket(ship2.x,ship2.y,ship2.direction,True,2)

                    # P2 superweapon
                    if e.key==K_s:
                        if superweapon[1]==1:  # Lightspeed
                            if frame_nr>frame_cd2+200 and ship2.alive:
                                kb=ship2.start_lightspeed(ship1)
                                if kb[0]:
                                    explosion_super2=Explode(ship1.x,ship1.y)
                                    if explosionSnd: explosionSnd.play()
                                    ship1=Ship(x*0.8,y*0.8,1)
                                    p1_score-=1; p2_score+=3
                                frame_cd2=frame_nr
                            ship2.stop_lightspeed()
                        elif superweapon[1]==2:  # Spacemine
                            if frame_nr>frame_cd2+200 and ship2.alive:
                                frame_cd2=frame_nr
                                spacemines.append(ship2.start_spacemine(frame_nr))

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




