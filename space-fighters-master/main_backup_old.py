#!/usr/bin/env python
import sys
import random
import pygame
from pygame.locals import *

#INITIALIZE
SCREENWIDTH = 800
SCREENHEIGHT= 600
pygame.init()
WINDOW = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("SpaceFighters")
pygame.display.set_icon(pygame.image.load('resources/ship1.png'))
fpsClock = pygame.time.Clock()
pygame.mouse.set_visible(0)
pygame.key.set_repeat(100, 100)

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
CURSOR_ROW = 1
CURSOR   = pygame.image.load('resources/cursor.png')

#CONSTANTS

# BG Music
pygame.mixer.music.load("resources/bg_music.mp3")

#Fonts
SPACEFONT = pygame.font.Font('resources/space.ttf', 34)
BIGFONT = pygame.font.Font('font.ttf', 34)
MEDFONT = pygame.font.Font('font.ttf', 28)
FONT = pygame.font.Font('font.ttf', 16)
SMALLFONT = pygame.font.Font('font.ttf', 9)

#TEXTURES
BACKGROUND = pygame.image.load('resources/background.png')
SHIP1   = pygame.image.load('resources/ship1.png')
SHIP2   = pygame.image.load('resources/ship2.png')
SHIP3   = pygame.image.load('resources/ship3.png')
SHIP4   = pygame.image.load('resources/ship4.png')

# TEXTURES SUPERWEAPONS
SHIP1_LS = pygame.image.load('resources/ship1_lightspeed.png')
SHIP1_SM = pygame.image.load('resources/spacemine.png')
SHIP1_PH = pygame.image.load('resources/ship1_phantom.png')
SHIP2_LS = pygame.image.load('resources/ship2_lightspeed.png')
SHIP2_SM = pygame.image.load('resources/spacemine.png')
SHIP2_PH = pygame.image.load('resources/ship2_phantom.png')
SHIP3_LS = pygame.image.load('resources/ship3_lightspeed.png')
SHIP3_SM = pygame.image.load('resources/spacemine.png')
SHIP3_PH = pygame.image.load('resources/ship3_phantom.png')
SHIP4_LS = pygame.image.load('resources/ship4_lightspeed.png')
SHIP4_SM = pygame.image.load('resources/spacemine.png')
SHIP4_PH = pygame.image.load('resources/ship4_phantom.png')

#representing colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (100,115,175)
RED = (176,52,52)
GREEN = (84,155,70)
ORANGE =(255,150,0)

#STATS to be modified and imported
#[ShipSpeed, Maneuverability, RocketSpeed, MoneyLeft, SuperWeapon]
STATS1 = [1,1,1,1000, 1]
STATS2 = [1,1,1,1000, 1]
STATS3 = [1,1,1,1000, 1]
STATS4 = [1,1,1,1000, 1]



def save_stats(player_nr):
    global STATS1
    global STATS2
    global STATS3
    global STATS4
    try:
        # Write the file to disk
        high_score_file = open("stats"+str(player_nr)+".txt", "w")
        if player_nr == 1:
            high_score_file.write(str(STATS1))
        if player_nr == 2:
            high_score_file.write(str(STATS2))
        if player_nr == 3:
            high_score_file.write(str(STATS3))
        if player_nr == 4:
            high_score_file.write(str(STATS4))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


def reset_all_stats():
    global STATS1
    global STATS2
    global STATS3
    global STATS4
    STATS1 = [1,1,1,1000, 1]
    STATS2 = [1,1,1,1000, 1]
    STATS3 = [1,1,1,1000, 1]
    STATS4 = [1,1,1,1000, 1]
    for i in range(1,5):
        try:
            resetfile = open("stats"+str(i)+".txt", 'r+')
            resetfile.truncate(0)
        except IOError:
            # Hm, can't write it.
            print("Unable to save the high score.")
        save_stats(i)


def calc_points(player_nr):
    global STATS1
    global STATS2
    global STATS3
    global STATS4
    if player_nr == 1:
        STATS1[3] = (1030 - (10 * STATS1[0] * STATS1[0] )
                     - (10 * STATS1[1] * STATS1[1] )
                     - (10 * STATS1[2] * STATS1[2] ))
    if player_nr == 2:
        STATS2[3] = (1030 - (10 * STATS2[0] * STATS2[0] )
                     - (10 * STATS2[1] * STATS2[1] )
                     - (10 * STATS2[2] * STATS2[2] ))
    if player_nr == 3:
        STATS3[3] = (1030 - (10 * STATS3[0] * STATS3[0] )
                     - (10 * STATS3[1] * STATS3[1] )
                     - (10 * STATS3[2] * STATS3[2] ))
    if player_nr == 4:
        STATS4[3] = (1030 - (10 * STATS4[0] * STATS4[0] )
                     - (10 * STATS4[1] * STATS4[1] )
                     - (10 * STATS4[2] * STATS4[2] ))
    

def up_stat(player_nr):
    global CURSOR_ROW
    global STATS1
    global STATS2
    global STATS3
    global STATS4

    if player_nr ==1:            
        if CURSOR_ROW == 1:
            STATS1[0] += 1
            if STATS1[0] > 9: STATS1[0] = 9
        if CURSOR_ROW == 2:
            STATS1[1] += 1
            if STATS1[1] > 9: STATS1[1] = 9
        if CURSOR_ROW == 3:
            STATS1[2] += 1
            if STATS1[2] > 9: STATS1[2] = 9
        if CURSOR_ROW == 4:
            STATS1[4] += 1
            if STATS1[4] > 3: STATS1[4] = 3
    if player_nr ==2:            
        if CURSOR_ROW == 1:
            STATS2[0] += 1
            if STATS2[0] > 9: STATS2[0] = 9
        if CURSOR_ROW == 2:
            STATS2[1] += 1
            if STATS2[1] > 9: STATS2[1] = 9
        if CURSOR_ROW == 3:
            STATS2[2] += 1
            if STATS2[2] > 9: STATS2[2] = 9
        if CURSOR_ROW == 4:
            STATS2[4] += 1
            if STATS2[4] > 3: STATS2[4] = 3
    if player_nr ==3:            
        if CURSOR_ROW == 1:
            STATS3[0] += 1
            if STATS3[0] > 9: STATS3[0] = 9
        if CURSOR_ROW == 2:
            STATS3[1] += 1
            if STATS3[1] > 9: STATS3[1] = 9
        if CURSOR_ROW == 3:
            STATS3[2] += 1
            if STATS3[2] > 9: STATS3[2] = 9
        if CURSOR_ROW == 4:
            STATS3[4] += 1
            if STATS3[4] > 3: STATS3[4] = 3
    if player_nr ==4:            
        if CURSOR_ROW == 1:
            STATS4[0] += 1
            if STATS4[0] > 9: STATS4[0] = 9
        if CURSOR_ROW == 2:
            STATS4[1] += 1
            if STATS4[1] > 9: STATS4[1] = 9
        if CURSOR_ROW == 3:
            STATS4[2] += 1
            if STATS4[2] > 9: STATS4[2] = 9
        if CURSOR_ROW == 4:
            STATS4[4] += 1
            if STATS4[4] > 3: STATS4[4] = 3

    calc_points(player_nr)
        
def down_stat(player_nr):
    global CURSOR_ROW
    global STATS1
    global STATS2
    global STATS3
    global STATS4
    
    if player_nr ==1:            
        if CURSOR_ROW == 1:
            STATS1[0] -= 1
            if STATS1[0] < 1: STATS1[0] = 1
        if CURSOR_ROW == 2:
            STATS1[1] -= 1
            if STATS1[1] < 1: STATS1[1] = 1
        if CURSOR_ROW == 3:
            STATS1[2] -= 1
            if STATS1[2] < 1: STATS1[2] = 1
        if CURSOR_ROW == 4:
            STATS1[4] -= 1
            if STATS1[4] < 1: STATS1[4] = 1
    if player_nr ==2:            
        if CURSOR_ROW == 1:
            STATS2[0] -= 1
            if STATS2[0] < 1: STATS2[0] = 1
        if CURSOR_ROW == 2:
            STATS2[1] -= 1
            if STATS2[1] < 1: STATS2[1] = 1
        if CURSOR_ROW == 3:
            STATS2[2] -= 1
            if STATS2[2] < 1: STATS2[2] = 1
        if CURSOR_ROW == 4:
            STATS2[4] -= 1
            if STATS2[4] < 1: STATS2[4] = 1
    if player_nr ==3:            
        if CURSOR_ROW == 1:
            STATS3[0] -= 1
            if STATS3[0] < 1: STATS3[0] = 1
        if CURSOR_ROW == 2:
            STATS3[1] -= 1
            if STATS3[1] < 1: STATS3[1] = 1
        if CURSOR_ROW == 3:
            STATS3[2] -= 1
            if STATS3[2] < 1: STATS3[2] = 1
        if CURSOR_ROW == 4:
            STATS3[4] -= 1
            if STATS3[4] < 1: STATS3[4] = 1
    if player_nr ==4:            
        if CURSOR_ROW == 1:
            STATS4[0] -= 1
            if STATS4[0] < 1: STATS4[0] = 1
        if CURSOR_ROW == 2:
            STATS4[1] -= 1
            if STATS4[1] < 1: STATS4[1] = 1
        if CURSOR_ROW == 3:
            STATS4[2] -= 1
            if STATS4[2] < 1: STATS4[2] = 1
        if CURSOR_ROW == 4:
            STATS4[4] -= 1
            if STATS4[4] < 1: STATS4[4] = 1
            
    calc_points(player_nr)

def quick_game(playercount):
    #DOES THE PLAYER WANT A QUICK GAME WITH DEFAULT VALUES?
    global STATS1
    global STATS2
    global STATS3
    global STATS4

    frame = 0.0
    frame_nr = SCREENHEIGHT + 300
    while 1:
        frame_nr -= 3
        if frame_nr < 0:
            frame_nr = SCREENHEIGHT + 300
        
        DISPLAY.fill(BLACK)
        DISPLAY.blit(BACKGROUND,(0,0))
        #DRAW MAIN MENUE
        main_txt1 = "spacefighters"
        main_txt2 = ("quick game")
        main_txt3 = ("competitive")
          
        p1_txt = SPACEFONT.render((main_txt1), True, WHITE)
        DISPLAY.blit(p1_txt,(200, 100))
        p2_txt = SPACEFONT.render((main_txt2), True, WHITE)
        DISPLAY.blit(p2_txt,(100, 250))
        p3_txt = SPACEFONT.render((main_txt3), True, WHITE)
        DISPLAY.blit(p3_txt,(100, 350))


        DISPLAY.blit(SHIP1,(180+ 300,frame_nr -300))
        DISPLAY.blit(SHIP2,(230+ 300,frame_nr -250))
        
        if playercount > 2:
            DISPLAY.blit(SHIP3,(280+ 300,frame_nr-180))
        if playercount > 3:
            DISPLAY.blit(SHIP4,(330+ 300,frame_nr-200))
        
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                handle_resize(event)
            if not hasattr(event, 'key'): continue
        
            #QUIT Event
            elif event.type == KEYDOWN:
                #print(event.key)
                if event.key == K_ESCAPE:
                    main()
                        

                # Choose Players
                
                if (event.key == K_c):
                    choose_mode(playercount)
                    
                if (event.key == K_q):
                    for i in range(0,5):
                        STATS1[i] = 4
                        STATS2[i] = 4
                        STATS3[i] = 4
                        STATS4[i] = 4
                    #DEFAULT SUPERWEAPON?
                    STATS1[i] = 2
                    STATS2[i] = 2
                    STATS3[i] = 2
                    STATS4[i] = 2
                    save_stats(1)
                    save_stats(2)
                    save_stats(3)
                    save_stats(4)

                    import main4players
                    main4players.PLAYERS = playercount
                    main4players.main()
        scale_display()
        fpsClock.tick(60)


def choose_mode(playercount, player = 1):   
    while 1:
        global CURSOR_ROW
        global STATS1
        global STATS2
        global STATS3
        global STATS4

        DISPLAY.fill(BLACK)
        DISPLAY.blit(BACKGROUND,(0,0))        

        points_pl1 = " Money left for Upgrades :  " + str(STATS1[3]) + " $ "
        bool_money_1 = STATS1[3] >= 0
        points_pl2 = " Money left for Upgrades :  " + str(STATS2[3]) + " $ "
        bool_money_2 = STATS2[3] >= 0
        points_pl3 = " Money left for Upgrades :  " + str(STATS3[3]) + " $ "
        bool_money_3 = STATS3[3] >= 0
        points_pl4 = " Money left for Upgrades :  " + str(STATS4[3]) + " $ "
        bool_money_4 = STATS4[3] >= 0
        stats_text1 = stats_text2 = stats_text3 = player_txt1_ = points_txt_ = ""


        super_text1 = "Chose your Superweapon : < Light Speed >"
        super_text2 = "Chose your Superweapon : < Space Mine >"
        super_text3 = "Chose your Superweapon : < Phantom Shield // NOT READY YET >"

        
        if player == 1:
            DISPLAY.blit(pygame.transform.scale(SHIP1,(100,100)),(580,50))
            player_txt1 = " PLAYER " + str(player) +" MODIFY STATS "
            player_txt1_ = BIGFONT.render((player_txt1), True, BLUE, BLACK)
            stats_text1 = " Ship Speed : " + STATS1[0] * "|x|"
            stats_text2 = " Maneuverability : " + STATS1[1] * "|x|"
            stats_text3 = " Rocket Max Speed : " + STATS1[2] * "|x|"
            if STATS1[3] >= 0:
                points_txt_ = MEDFONT.render((points_pl1), True, WHITE, BLACK)
            else:
                points_txt_ = MEDFONT.render((points_pl1), True, RED, BLACK)

            if STATS1[4] == 1:
                super_text_ = FONT.render((super_text1), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP1_LS,(40, 160)),(620,420))
            if STATS1[4] == 2:
                super_text_ = FONT.render((super_text2), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP1_SM,(40,40)),(620,540))
            if STATS1[4] == 3:
                super_text_ = FONT.render((super_text3), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP1_PH,(40,40)),(595,540))
                DISPLAY.blit(pygame.transform.scale(SHIP1   ,(40,40)),(635,540))
                DISPLAY.blit(pygame.transform.scale(SHIP1_PH,(40,40)),(675,540))

        if player == 2:
            DISPLAY.blit(pygame.transform.scale(SHIP2,(100,100)),(580,50))
            player_txt1 = " PLAYER " + str(player) +" MODIFY STATS "
            player_txt1_ = BIGFONT.render((player_txt1), True, RED, BLACK)
            stats_text1 = " Ship Speed : " + STATS2[0] * "|x|"
            stats_text2 = " Maneuverability : " + STATS2[1] * "|x|"
            stats_text3 = " Rocket Max Speed : " + STATS2[2] * "|x|"
            if STATS2[3] >= 0:
                points_txt_ = MEDFONT.render((points_pl2), True, WHITE, BLACK)
            else:
                points_txt_ = MEDFONT.render((points_pl2), True, RED, BLACK)

            if STATS2[4] == 1:
                super_text_ = FONT.render((super_text1), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP2_LS,(40, 160)),(620,420))
            if STATS2[4] == 2:
                super_text_ = FONT.render((super_text2), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP2_SM,(40,40)),(620,540))
            if STATS2[4] == 3:
                super_text_ = FONT.render((super_text3), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP2_PH,(40,40)),(595,540))
                DISPLAY.blit(pygame.transform.scale(SHIP2   ,(40,40)),(635,540))
                DISPLAY.blit(pygame.transform.scale(SHIP2_PH,(40,40)),(675,540))

        if player == 3:
            DISPLAY.blit(pygame.transform.scale(SHIP3,(100,100)),(580,50))
            player_txt1 = " PLAYER " + str(player) +" MODIFY STATS "
            player_txt1_ = BIGFONT.render((player_txt1), True, GREEN, BLACK)
            stats_text1 = " Ship Speed : " + STATS3[0] * "|x|"
            stats_text2 = " Maneuverability : " + STATS3[1] * "|x|"
            stats_text3 = " Rocket ,Max Speed : " + STATS3[2] * "|x|"
            if STATS3[3] >= 0:
                points_txt_ = MEDFONT.render((points_pl3), True, WHITE, BLACK)
            else:
                points_txt_ = MEDFONT.render((points_pl3), True, RED, BLACK)

            if STATS3[4] == 1:
                super_text_ = FONT.render((super_text1), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP3_LS,(40, 160)),(620,420))
            if STATS3[4] == 2:
                super_text_ = FONT.render((super_text2), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP3_SM,(40,40)),(620,540))
            if STATS3[4] == 3:
                super_text_ = FONT.render((super_text3), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP3_PH,(40,40)),(595,540))
                DISPLAY.blit(pygame.transform.scale(SHIP3   ,(40,40)),(635,540))
                DISPLAY.blit(pygame.transform.scale(SHIP3_PH,(40,40)),(675,540))

        if player == 4:
            DISPLAY.blit(pygame.transform.scale(SHIP4,(100,100)),(580,50))
            player_txt1 = " PLAYER " + str(player) +" MODIFY STATS "
            player_txt1_ = BIGFONT.render((player_txt1), True, ORANGE, BLACK)
            stats_text1 = " Ship Speed : " + STATS4[0] * "|x|"
            stats_text2 = " Maneuverability : " + STATS4[1] * "|x|"
            stats_text3 = " Rocket Max Speed : " + STATS4[2] * "|x|"
            if STATS4[3] >= 0:
                points_txt_ = MEDFONT.render((points_pl4), True, WHITE, BLACK)
            else:
                points_txt_ = MEDFONT.render((points_pl4), True, RED, BLACK)

            if STATS4[4] == 1:
                super_text_ = FONT.render((super_text1), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP4_LS,(40, 160)),(620,420))
            if STATS4[4] == 2:
                super_text_ = FONT.render((super_text2), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP4_SM,(40,40)),(620,540))
            if STATS4[4] == 3:
                super_text_ = FONT.render((super_text3), True, WHITE, BLACK)
                DISPLAY.blit(pygame.transform.scale(SHIP4_PH,(40,40)),(595,540))
                DISPLAY.blit(pygame.transform.scale(SHIP4   ,(40,40)),(635,540))
                DISPLAY.blit(pygame.transform.scale(SHIP4_PH,(40,40)),(675,540))


        stats_text1_ = FONT.render((stats_text1), True, WHITE, BLACK)
        stats_text2_ = FONT.render((stats_text2), True, WHITE, BLACK)
        stats_text3_ = FONT.render((stats_text3), True, WHITE, BLACK)

        DISPLAY.blit(stats_text1_,(180, 240))
        DISPLAY.blit(stats_text2_,(180, 340))
        DISPLAY.blit(stats_text3_,(180, 440))

        DISPLAY.blit(super_text_, (180, 540))
                     
        DISPLAY.blit(player_txt1_,(100, 100))
        DISPLAY.blit(points_txt_,(100, 150))
        DISPLAY.blit(CURSOR,(120,CURSOR_ROW*SCREENHEIGHT/6+125))
        
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                handle_resize(event)
            if not hasattr(event, 'key'): continue
                    #QUIT Event
            elif event.type == KEYDOWN:
               #print(event.key)
                if event.key == K_ESCAPE:
                    main()
                if event.key == K_BACKSPACE:
                    if player > 1:
                        choose_mode(playercount, player - 1)
                    else:
                        main()
                #EDIT STATS WITH RIGHT/LEFT , CHANGE ROW WITH UP/DOWN
                if event.key == K_UP:
                    CURSOR_ROW += -1
                    if CURSOR_ROW < 1:
                        CURSOR_ROW = 1
                if event.key == K_DOWN:
                    CURSOR_ROW += 1
                    if CURSOR_ROW > 4:
                        CURSOR_ROW = 4
                if event.key == K_RIGHT:
                    up_stat(player)
                if event.key == K_LEFT:
                    down_stat(player)
                if event.key == K_r:
                    reset_all_stats()

                if event.key == K_RETURN:
                    if player == playercount:                        
                        if playercount == 2 and bool_money_2:
                            save_stats(1)
                            save_stats(2)
                            save_stats(3)
                            save_stats(4)

                            import main4players
                            main4players.PLAYERS = 2
                            main4players.main()
                        if playercount == 3 and bool_money_3:
                            save_stats(1)
                            save_stats(2)
                            save_stats(3)
                            save_stats(4)
                            import main4players
                            main4players.PLAYERS = 3
                            main4players.main()
                        if playercount == 4 and bool_money_4:
                            save_stats(1)
                            save_stats(2)
                            save_stats(3)
                            save_stats(4)
                            import main4players
                            main4players.PLAYERS = 4
                            main4players.main()
                    elif bool_money_1 and bool_money_2 and bool_money_3 and bool_money_4:
                        choose_mode(playercount, player + 1)

        scale_display()
        fpsClock.tick(60)

def intro():
    main_txt1 = "spacefighters"
    done = False
    i = SCREENHEIGHT
    while not done and i > 102:
        if i > 100:
            i-=2
        DISPLAY.fill(BLACK)
        DISPLAY.blit(BACKGROUND,(0,0))

        p1_txt = SPACEFONT.render((main_txt1), True, WHITE)
        DISPLAY.blit(p1_txt,(200, i))
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                handle_resize(event)
            if not hasattr(event, 'key'): continue

            #QUIT Event
            elif event.type == KEYDOWN:
                done = True
        scale_display()
        fpsClock.tick(60)

def draw_glow_text(text, font, color, pos, glow_color, glow_radius=3):
    """Draw text with glow effect"""
    # Create glow surface
    glow_surf = pygame.Surface((font.size(text)[0] + glow_radius*4, font.size(text)[1] + glow_radius*4), pygame.SRCALPHA)
    text_surf = font.render(text, True, color)
    
    # Draw multiple layers for glow
    for i in range(glow_radius, 0, -1):
        alpha = int(100 / (i + 1))
        glow_layer = font.render(text, True, glow_color)
        glow_surf.blit(glow_layer, (glow_radius*2 - i, glow_radius*2 - i))
        glow_surf.set_alpha(alpha)
    
    # Draw main text on top
    DISPLAY.blit(text_surf, (pos[0], pos[1]))
    return text_surf.get_rect(topleft=pos)


def draw_neon_box(x, y, width, height, color, selected=False, border_radius=10):
    """Draw a box with neon border effect"""
    box_rect = pygame.Rect(x, y, width, height)
    
    if selected:
        # Glow effect when selected
        for i in range(8, 0, -2):
            glow_color = (color[0], color[1], color[2], int(60 / (i//2 + 1)))
            glow_surf = pygame.Surface((width + i*2, height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, glow_color, (0, 0, width + i*2, height + i*2), border_radius=border_radius)
            DISPLAY.blit(glow_surf, (x - i, y - i))
        
        # Main border (thicker when selected)
        pygame.draw.rect(DISPLAY, color, box_rect, 3, border_radius=border_radius)
        # Inner fill with slight transparency
        fill_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(fill_surf, (color[0], color[1], color[2], 30), (0, 0, width, height), border_radius=border_radius)
        DISPLAY.blit(fill_surf, (x, y))
    else:
        # Dim border when not selected
        dim_color = (100, 100, 100)
        pygame.draw.rect(DISPLAY, dim_color, box_rect, 2, border_radius=border_radius)


def draw_button(x, y, width, height, text, selected, color_normal, color_hover):
    """Draw an interactive button with hover effect"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    is_hovered = (x <= mouse_x <= x + width and y <= mouse_y <= y + height)
    
    btn_color = color_hover if (selected or is_hovered) else color_normal
    
    # Glow effect
    if selected or is_hovered:
        for i in range(6, 0, -2):
            glow_surf = pygame.Surface((width + i*2, height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*btn_color[:3], int(80 / (i//2 + 1))), (0, 0, width + i*2, height + i*2), border_radius=8)
            DISPLAY.blit(glow_surf, (x - i, y - i))
    
    # Button background
    btn_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(DISPLAY, btn_color, btn_rect, border_radius=8)
    
    # Button text
    btn_text = FONT.render(text, True, WHITE)
    text_x = x + width//2 - btn_text.get_width()//2
    text_y = y + height//2 - btn_text.get_height()//2
    DISPLAY.blit(btn_text, (text_x, text_y))
    
    return btn_rect


def draw_grid():
    """Draw futuristic grid on the floor"""
    grid_color = (0, 100, 150, 40)
    # Horizontal lines
    for y in range(SCREENHEIGHT - 150, SCREENHEIGHT, 30):
        pygame.draw.line(DISPLAY, grid_color, (0, y), (SCREENWIDTH, y), 1)
    # Vertical perspective lines
    for x in range(0, SCREENWIDTH + 1, 60):
        pygame.draw.line(DISPLAY, grid_color, (x, SCREENHEIGHT - 150), (x, SCREENHEIGHT), 1)


def draw_stars():
    """Draw background stars/particles"""
    random.seed(42)  # Fixed seed for consistent stars
    for _ in range(50):
        x = random.randint(0, SCREENWIDTH)
        y = random.randint(0, SCREENHEIGHT - 200)
        size = random.randint(1, 3)
        alpha = random.randint(50, 150)
        star_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(star_surf, (200, 220, 255, alpha), (size, size), size)
        DISPLAY.blit(star_surf, (x, y))


def draw_player_icon(x, y, player_type, color, scale=1.0):
    """Draw a simple player character icon"""
    size = int(30 * scale)
    surf = pygame.Surface((size*2, size*3), pygame.SRCALPHA)
    
    if player_type == "warrior":
        # Warrior with sword
        # Body
        pygame.draw.ellipse(surf, color, (size//2, size, size, size*1.5))
        # Head
        pygame.draw.circle(surf, (255, 200, 150), (size, size//2), size//3)
        # Sword
        pygame.draw.rect(surf, (200, 200, 255), (size+5, size//2, 4, size*1.5))
        pygame.draw.rect(surf, (150, 150, 200), (size+3, size*1.5, 8, 3))
        # Shield
        pygame.draw.ellipse(surf, (100, 100, 150), (size//4, size*1.2, size//2, size))
        
    elif player_type == "ranger":
        # Ranger with hat
        # Body
        pygame.draw.ellipse(surf, (139, 90, 43), (size//2, size, size, size*1.5))
        # Head
        pygame.draw.circle(surf, (255, 200, 150), (size, size//2), size//3)
        # Hat
        pygame.draw.ellipse(surf, (101, 67, 33), (size//3, size//4, size*1.3, size//2))
        pygame.draw.rect(surf, (101, 67, 33), (size//2, 0, size, size//2))
        # Gun
        pygame.draw.rect(surf, (80, 80, 80), (size+5, size, 3, size//2))
        
    elif player_type == "tech":
        # Tech/Scientist
        # Body
        pygame.draw.ellipse(surf, (50, 150, 100), (size//2, size, size, size*1.5))
        # Head
        pygame.draw.circle(surf, (255, 200, 150), (size, size//2), size//3)
        # Goggles
        pygame.draw.rect(surf, (100, 100, 100), (size-8, size//2-3, 16, 6))
        # Tool
        pygame.draw.rect(surf, (200, 200, 100), (size+5, size, 4, size))
    
    DISPLAY.blit(surf, (x, y))
    return surf


def draw_robot_icon(x, y, scale=1.0):
    """Draw a simple robot/enemy icon"""
    size = int(35 * scale)
    surf = pygame.Surface((size*2.5, size*3), pygame.SRCALPHA)
    
    # Robot body
    pygame.draw.rect(surf, (180, 180, 190), (size//2, size, size*1.5, size*1.5), border_radius=5)
    # Robot head
    pygame.draw.rect(surf, (200, 200, 210), (size//2, size//4, size*1.5, size), border_radius=3)
    # Left eye (red)
    pygame.draw.circle(surf, (255, 50, 50), (size//2+8, size//2), 5)
    # Right eye (red)
    pygame.draw.circle(surf, (255, 50, 50), (size+size//2-8, size//2), 5)
    # Center eye (green sensor)
    pygame.draw.circle(surf, (50, 255, 50), (size, size//2+5), 6)
    # Antenna
    pygame.draw.line(surf, (150, 150, 150), (size, size//4), (size, 0), 2)
    pygame.draw.circle(surf, (255, 100, 100), (size, 0), 3)
    # Arms
    pygame.draw.line(surf, (160, 160, 170), (size//2, size+10), (0, size+30), 4)
    pygame.draw.line(surf, (160, 160, 170), (size*2, size+10), (size*2.5, size+30), 4)
    # Claws
    pygame.draw.ellipse(surf, (200, 150, 100), (-5, size+25, 15, 10))
    pygame.draw.ellipse(surf, (200, 150, 100), (size*2, size+25, 15, 10))
    # Legs
    pygame.draw.line(surf, (140, 140, 150), (size//2+10, size*2.5), (size//2, size*3), 4)
    pygame.draw.line(surf, (140, 140, 150), (size+size//2-10, size*2.5), (size+size//2, size*3), 4)
    
    DISPLAY.blit(surf, (x, y))
    return surf


def draw_pvp_characters(x, y):
    """Draw 3 player characters for PvP mode"""
    # Draw 3 warriors side by side
    draw_player_icon(x, y, "warrior", (100, 150, 255), 1.0)  # Blue warrior
    draw_player_icon(x + 35, y + 5, "ranger", (139, 90, 43), 0.9)  # Brown ranger
    draw_player_icon(x + 70, y, "tech", (50, 180, 100), 1.0)  # Green tech


def draw_pve_characters(x, y):
    """Draw player and robot for PvE mode"""
    # Draw player and robot
    draw_player_icon(x, y, "warrior", (100, 150, 255), 1.1)  # Blue player
    draw_robot_icon(x + 50, y - 5, 1.1)  # Robot enemy


def draw_corner_frame():
    """Draw sci-fi corner decorations"""
    corner_color = (0, 200, 255)
    corner_length = 40
    corner_thickness = 3
    margin = 15
    
    # Top-left corner
    pygame.draw.line(DISPLAY, corner_color, (margin, margin), (margin + corner_length, margin), corner_thickness)
    pygame.draw.line(DISPLAY, corner_color, (margin, margin), (margin, margin + corner_length), corner_thickness)
    
    # Top-right corner
    pygame.draw.line(DISPLAY, corner_color, (SCREENWIDTH - margin, margin), (SCREENWIDTH - margin - corner_length, margin), corner_thickness)
    pygame.draw.line(DISPLAY, corner_color, (SCREENWIDTH - margin, margin), (SCREENWIDTH - margin, margin + corner_length), corner_thickness)
    
    # Bottom-left corner
    pygame.draw.line(DISPLAY, corner_color, (margin, SCREENHEIGHT - margin), (margin + corner_length, SCREENHEIGHT - margin), corner_thickness)
    pygame.draw.line(DISPLAY, corner_color, (margin, SCREENHEIGHT - margin), (margin, SCREENHEIGHT - margin - corner_length), corner_thickness)
    
    # Bottom-right corner
    pygame.draw.line(DISPLAY, corner_color, (SCREENWIDTH - margin, SCREENHEIGHT - margin), (SCREENWIDTH - margin - corner_length, SCREENHEIGHT - margin), corner_thickness)
    pygame.draw.line(DISPLAY, corner_color, (SCREENWIDTH - margin, SCREENHEIGHT - margin), (SCREENWIDTH - margin, SCREENHEIGHT - margin - corner_length), corner_thickness)


def draw_input_box(x, y, width, height, text, active, max_chars=12):
    """Draw an input text box"""
    box_color = (0, 255, 255) if active else (100, 150, 180)
    
    # Glow effect if active
    if active:
        for i in range(5, 0, -1):
            glow_surf = pygame.Surface((width + i*2, height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 200, 255, int(80 / (i+1))), (0, 0, width + i*2, height + i*2), border_radius=5)
            DISPLAY.blit(glow_surf, (x - i, y - i))
    
    # Box background
    pygame.draw.rect(DISPLAY, (20, 40, 60), (x, y, width, height), border_radius=5)
    pygame.draw.rect(DISPLAY, box_color, (x, y, width, height), 2, border_radius=5)
    
    # Text with cursor animation
    display_text = text if text else ""
    if active and pygame.time.get_ticks() % 1000 < 500:
        display_text += "_"
    
    text_surf = FONT.render(display_text, True, WHITE)
    text_x = x + 10
    text_y = y + height//2 - text_surf.get_height()//2
    DISPLAY.blit(text_surf, (text_x, text_y))
    
    return pygame.Rect(x, y, width, height)


def draw_radio_button(x, y, text, selected, color_active):
    """Draw a radio button with label"""
    radius = 10
    
    if selected:
        # Glow effect
        for i in range(4, 0, -1):
            pygame.draw.circle(DISPLAY, (*color_active[:3], 60), (x + radius, y + radius), radius + i)
        
        # Filled circle
        pygame.draw.circle(DISPLAY, color_active, (x + radius, y + radius), radius)
        pygame.draw.circle(DISPLAY, WHITE, (x + radius, y + radius), radius - 3)
    else:
        # Empty circle
        pygame.draw.circle(DISPLAY, (150, 150, 150), (x + radius, y + radius), radius, 2)
    
    # Label
    label = FONT.render(text, True, WHITE if selected else (180, 180, 180))
    DISPLAY.blit(label, (x + radius * 2 + 10, y + 2))


def draw_particle_effect():
    """Draw energy/smoke particle effect in bottom right corner"""
    current_time = pygame.time.get_ticks()
    
    for i in range(15):
        random.seed(current_time // 100 + i)
        x = SCREENWIDTH - 80 + random.randint(-30, 30)
        y = SCREENHEIGHT - 100 - (current_time // 20 + i * 10) % 150
        size = random.randint(5, 15)
        alpha = random.randint(50, 150)
        
        particle_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, (0, 255, 255, alpha), (size, size), size)
        DISPLAY.blit(particle_surf, (x, y))


def draw_ship_preview(x, y, scale=1.5):
    """Draw a ship preview icon"""
    size = int(40 * scale)
    surf = pygame.Surface((size*2, size*3), pygame.SRCALPHA)
    
    # Ship body (triangle shape)
    points = [
        (size, 0),  # top
        (size//3, size*2),  # bottom left
        (size*2 - size//3, size*2),  # bottom right
    ]
    pygame.draw.polygon(surf, (0, 200, 255), points)
    pygame.draw.polygon(surf, (100, 255, 255), points, 2)
    
    # Cockpit
    pygame.draw.circle(surf, (200, 255, 255), (size, size), size//3)
    
    # Engine glow
    for i in range(3):
        glow_y = size*2 + i * 5
        pygame.draw.ellipse(surf, (0, 255, 255, 150 - i*40), (size//2, glow_y, size, 10))
    
    DISPLAY.blit(surf, (x, y))


def draw_map_selection(x, y, map_name, map_number, selected, color):
    """Draw map selection with checkbox style like the image"""
    box_size = 18
    
    if selected:
        # Selected - show checkmark
        pygame.draw.rect(DISPLAY, color, (x, y, box_size, box_size), 2, border_radius=2)
        # Checkmark
        check_color = color
        pygame.draw.line(DISPLAY, check_color, (x + 3, y + 9), (x + 7, y + 14), 2)
        pygame.draw.line(DISPLAY, check_color, (x + 7, y + 14), (x + 15, y + 4), 2)
        # Map number
        num_text = FONT.render(f"✓ {map_name}", True, WHITE)
    else:
        # Not selected - show number
        pygame.draw.rect(DISPLAY, (150, 150, 150), (x, y, box_size, box_size), 2, border_radius=2)
        # Map number in parentheses style
        num_text = FONT.render(f"({map_number}) {map_name}", True, (180, 180, 180))
    
    DISPLAY.blit(num_text, (x + 25, y + 2))


def game_setup_menu(game_mode):
    """Game setup menu with map selection and player names"""
    selected_map = 0  # 0: Deep Space Arena, 1: Gravity Chaos Zone, 2: Reverse Gravity Zone
    player1_name = "Player 1"
    player2_name = "Player 2"
    active_input = 1  # 1 = Player 1, 2 = Player 2 (PvP) or 0 (PvE)
    selected_button = 0  # 0: Start Game, 1: Back
    menu_running = True
    
    maps = [
        "Deep Space Arena",
        "Gravity Chaos Zone", 
        "Reverse Gravity Zone"
    ]
    
    CYAN = (0, 255, 255)
    CYAN_DARK = (0, 150, 200)
    
    while menu_running:
        # Clear screen
        DISPLAY.fill((5, 10, 25))
        
        # Draw stars
        draw_stars()
        
        # Draw grid at bottom
        draw_grid()
        
        # Draw corner frames
        draw_corner_frame()
        
        # Main frame
        frame_x = 80
        frame_y = 50
        frame_width = SCREENWIDTH - 160
        frame_height = 420
        
        # Frame glow
        for i in range(10, 0, -2):
            glow_surf = pygame.Surface((frame_width + i*2, frame_height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 200, 255, int(60 / (i//2 + 1))), (0, 0, frame_width + i*2, frame_height + i*2), border_radius=15)
            DISPLAY.blit(glow_surf, (frame_x - i, frame_y - i))
        
        # Main frame background
        pygame.draw.rect(DISPLAY, (10, 30, 50, 200), (frame_x, frame_y, frame_width, frame_height), border_radius=15)
        pygame.draw.rect(DISPLAY, CYAN, (frame_x, frame_y, frame_width, frame_height), 3, border_radius=15)
        
        # Mode title at top of frame
        if game_mode == "PVP":
            mode_text = "PLAYER VS PLAYER"
        else:
            mode_text = "PLAYER VS ENVIRONMENT"
        
        mode_surf = BIGFONT.render(mode_text, True, CYAN)
        # Glow effect for mode title
        for i in range(8, 0, -2):
            glow_surf = BIGFONT.render(mode_text, True, CYAN_DARK)
            glow_surf.set_alpha(int(80 / (i//2 + 1)))
            DISPLAY.blit(glow_surf, (frame_x + frame_width//2 - mode_surf.get_width()//2, frame_y + 15))
        DISPLAY.blit(mode_surf, (frame_x + frame_width//2 - mode_surf.get_width()//2, frame_y + 15))
        
        # Player inputs
        input_y = frame_y + 70
        
        # Player 1
        p1_label = FONT.render("Player 1:", True, WHITE)
        DISPLAY.blit(p1_label, (frame_x + 50, input_y))
        draw_input_box(frame_x + 140, input_y - 3, 200, 30, player1_name, active_input == 1)
        
        # Player 2 (only for PvP mode)
        if game_mode == "PVP":
            input_y += 45
            p2_label = FONT.render("Player 2:", True, WHITE)
            DISPLAY.blit(p2_label, (frame_x + 50, input_y))
            draw_input_box(frame_x + 140, input_y - 3, 200, 30, player2_name, active_input == 2)
        
        # Map selection
        map_y = input_y + 50 if game_mode == "PVP" else input_y + 45
        map_hint = FONT.render("# Select Map... Show [K] keys...", True, (150, 170, 200))
        DISPLAY.blit(map_hint, (frame_x + 50, map_y))
        
        # Map options with checkbox style
        map_list_y = map_y + 35
        for i, map_name in enumerate(maps):
            y_pos = map_list_y + i * 35
            is_selected = (i == selected_map)
            draw_map_selection(frame_x + 70, y_pos, map_name, i + 1, is_selected, CYAN)
        
        # Particle effect in bottom right
        draw_particle_effect()
        
        # Buttons - positioned at bottom of frame
        btn_width, btn_height = 160, 40
        btn_y = frame_y + frame_height - 70
        btn_start_x = frame_x + frame_width//2 - (btn_width * 2 + 20)//2
        
        # Start Game button
        start_color = (0, 150, 200)
        start_hover = (0, 220, 255)
        draw_button(btn_start_x, btn_y, btn_width, btn_height, "Start Game",
                   selected_button == 0, start_color, start_hover)
        
        # Back button
        back_color = (180, 50, 50)
        back_hover = (255, 80, 80)
        draw_button(btn_start_x + btn_width + 20, btn_y, btn_width, btn_height, "Back",
                   selected_button == 1, back_color, back_hover)
        
        # Control hints at bottom
        hint = SMALLFONT.render("[UP/DOWN] Select Map  |  [LEFT/RIGHT] Buttons  |  [TAB] Switch Input  |  [ENTER] Confirm", True, (150, 170, 200))
        DISPLAY.blit(hint, (SCREENWIDTH//2 - hint.get_width()//2, SCREENHEIGHT - 50))
        
        scale_display()
        fpsClock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                handle_resize(event)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return None  # Go back to menu 1
                elif event.key == K_k:
                    selected_map = (selected_map + 1) % len(maps)
                elif event.key == K_UP:
                    if selected_map > 0:
                        selected_map -= 1
                elif event.key == K_DOWN:
                    if selected_map < len(maps) - 1:
                        selected_map += 1
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    selected_button = 1 - selected_button
                elif event.key == K_TAB:
                    if game_mode == "PVP":
                        active_input = 2 if active_input == 1 else 1
                    else:
                        active_input = 1
                elif event.key == K_RETURN:
                    if selected_button == 0:  # Start Game
                        return {
                            "mode": game_mode,
                            "player1_name": player1_name,
                            "player2_name": player2_name if game_mode == "PVP" else "AI",
                            "map": maps[selected_map]
                        }
                    else:  # Back - return to menu 1
                        return None
                elif active_input == 1:
                    if event.key == K_BACKSPACE:
                        player1_name = player1_name[:-1] if len(player1_name) > 0 else ""
                    elif len(player1_name) < 12 and (event.unicode.isalnum() or event.unicode == " "):
                        player1_name += event.unicode
                elif active_input == 2 and game_mode == "PVP":
                    if event.key == K_BACKSPACE:
                        player2_name = player2_name[:-1] if len(player2_name) > 0 else ""
                    elif len(player2_name) < 12 and (event.unicode.isalnum() or event.unicode == " "):
                        player2_name += event.unicode


def show_mode_menu():
    """Show PvP vs PvE menu selection with sci-fi interface"""
    selected_mode = 0  # 0 = PvP, 1 = PvE
    selected_button = 0  # 0 = Start Game, 1 = Quit Game
    menu_running = True
    
    # Colors
    CYAN = (0, 255, 255)
    CYAN_DARK = (0, 150, 200)
    BLUE_GLOW = (0, 100, 255)
    RED_GLOW = (255, 50, 50)
    
    while menu_running:
        # Clear screen with space gradient
        DISPLAY.fill((5, 10, 25))
        
        # Draw stars
        draw_stars()
        
        # Draw grid at bottom
        draw_grid()
        
        # Draw title with neon glow
        title_text = "SPACE FIGHTERS"
        title = SPACEFONT.render(title_text, True, CYAN)
        title_x = SCREENWIDTH//2 - title.get_width()//2
        
        # Glow effect for title
        for i in range(15, 0, -3):
            glow_surf = SPACEFONT.render(title_text, True, CYAN_DARK)
            glow_surf.set_alpha(int(100 / (i//3 + 1)))
            DISPLAY.blit(glow_surf, (title_x, 50))
        DISPLAY.blit(title, (title_x, 50))
        
        # Subtitle
        subtitle = MEDFONT.render("Which mode would you like to play?", True, (200, 220, 255))
        DISPLAY.blit(subtitle, (SCREENWIDTH//2 - subtitle.get_width()//2, 110))
        
        hint_sub = FONT.render("Show [I] keys...", True, (150, 170, 200))
        DISPLAY.blit(hint_sub, (SCREENWIDTH//2 - hint_sub.get_width()//2, 145))
        
        # Mode selection boxes
        box_width, box_height = 280, 200
        box_y = 180
        gap = 40
        start_x = (SCREENWIDTH - (box_width * 2 + gap)) // 2
        
        # PvP Box
        pvp_x = start_x
        pvp_color = CYAN if selected_mode == 0 else (80, 80, 80)
        draw_neon_box(pvp_x, box_y, box_width, box_height, pvp_color, selected=selected_mode == 0)
        
        # [P] label
        p_label = BIGFONT.render("[P]", True, CYAN if selected_mode == 0 else (150, 150, 150))
        DISPLAY.blit(p_label, (pvp_x + 20, box_y + 20))
        
        # Player vs Player text
        pvp_text1 = MEDFONT.render("Player", True, WHITE if selected_mode == 0 else (180, 180, 180))
        pvp_text2 = MEDFONT.render("vs Player", True, WHITE if selected_mode == 0 else (180, 180, 180))
        DISPLAY.blit(pvp_text1, (pvp_x + 100, box_y + 50))
        DISPLAY.blit(pvp_text2, (pvp_x + 80, box_y + 85))
        
        # Character icons for PvP - 3 players
        draw_pvp_characters(pvp_x + 30, box_y + 120)
        
        # PvE Box
        pve_x = start_x + box_width + gap
        pve_color = RED if selected_mode == 1 else (80, 80, 80)
        draw_neon_box(pve_x, box_y, box_width, box_height, pve_color, selected=selected_mode == 1)
        
        # [E] label
        e_label = BIGFONT.render("[E]", True, RED if selected_mode == 1 else (150, 150, 150))
        DISPLAY.blit(e_label, (pve_x + 20, box_y + 20))
        
        # Player vs Environment text
        pve_text1 = MEDFONT.render("Player", True, WHITE if selected_mode == 1 else (180, 180, 180))
        pve_text2 = MEDFONT.render("vs", True, WHITE if selected_mode == 1 else (180, 180, 180))
        pve_text3 = FONT.render("Environment", True, WHITE if selected_mode == 1 else (180, 180, 180))
        DISPLAY.blit(pve_text1, (pve_x + 100, box_y + 50))
        DISPLAY.blit(pve_text2, (pve_x + 130, box_y + 80))
        DISPLAY.blit(pve_text3, (pve_x + 100, box_y + 105))
        
        # Character icons for PvE - player and robot
        draw_pve_characters(pve_x + 60, box_y + 115)
        
        # Buttons
        btn_width, btn_height = 180, 45
        btn_gap = 20
        btn_y = 420
        btn_start_x = SCREENWIDTH//2 - (btn_width * 2 + btn_gap)//2
        
        # Start Game button
        start_color = (0, 150, 200) if selected_mode == 0 else (0, 120, 150)
        start_hover = (0, 200, 255) if selected_mode == 0 else (0, 180, 220)
        draw_button(btn_start_x, btn_y, btn_width, btn_height, "Start Game", 
                   selected_button == 0, start_color, start_hover)
        
        # Quit Game button
        quit_color = (180, 50, 50) if selected_mode == 1 else (120, 40, 40)
        quit_hover = (255, 80, 80) if selected_mode == 1 else (200, 70, 70)
        draw_button(btn_start_x + btn_width + btn_gap, btn_y, btn_width, btn_height, "Quit Game",
                   selected_button == 1, quit_color, quit_hover)
        
        # Control hints at bottom
        hint_y = 490
        hint1 = SMALLFONT.render("Press [P] for PvP  |  [E] for PvE  |  ENTER to Start  |  ESC to Quit", True, (150, 170, 200))
        DISPLAY.blit(hint1, (SCREENWIDTH//2 - hint1.get_width()//2, hint_y))
        
        hint2 = SMALLFONT.render("P1 (Blue): Arrow keys  |  P2 (Red): A/D keys", True, (100, 130, 160))
        DISPLAY.blit(hint2, (SCREENWIDTH//2 - hint2.get_width()//2, hint_y + 25))
        
        scale_display()
        fpsClock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                handle_resize(event)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if selected_button == 1:  # If on Quit button, quit
                        pygame.quit()
                        sys.exit()
                    # Otherwise do nothing on ESC in menu 1
                elif event.key == K_p:
                    selected_mode = 0
                    selected_button = 0
                elif event.key == K_e:
                    selected_mode = 1
                    selected_button = 0
                elif event.key == K_LEFT:
                    selected_mode = 0
                elif event.key == K_RIGHT:
                    selected_mode = 1
                elif event.key == K_UP or event.key == K_DOWN:
                    selected_button = 1 - selected_button
                elif event.key == K_RETURN:
                    if selected_button == 0:  # Start Game
                        return "PVP" if selected_mode == 0 else "PVE"
                    else:  # Quit Game
                        pygame.quit()
                        sys.exit()
                elif event.key == K_i:
                    # Toggle show keys info (could expand this)
                    pass


def draw_upgrade_bar(x, y, width, height, value, max_value, label, icon_type="speed"):
    """Draw an upgrade bar with label"""
    # Label
    label_surf = FONT.render(label, True, WHITE)
    DISPLAY.blit(label_surf, (x, y))
    
    # Progress bar background
    bar_bg_rect = pygame.Rect(x, y + 20, width, height)
    pygame.draw.rect(DISPLAY, (20, 40, 60), bar_bg_rect, border_radius=3)
    pygame.draw.rect(DISPLAY, (50, 70, 90), bar_bg_rect, 1, border_radius=3)
    
    # Progress bar fill
    fill_width = int((value / max_value) * width)
    fill_rect = pygame.Rect(x, y + 20, fill_width, height)
    
    # Glow effect for fill
    for i in range(5, 0, -1):
        glow_rect = pygame.Rect(x - i, y + 20 - i, fill_width + i*2, height + i*2)
        glow_surf = pygame.Surface((fill_width + i*2, height + i*2), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (0, 200, 255, 40), glow_surf.get_rect(), border_radius=3)
        DISPLAY.blit(glow_surf, (x - i, y + 20 - i))
    
    pygame.draw.rect(DISPLAY, (0, 200, 255), fill_rect, border_radius=3)
    
    # Value indicator
    value_text = SMALLFONT.render(f"x{value}", True, WHITE)
    DISPLAY.blit(value_text, (x + width + 10, y + 25))
    
    # Adjustment hints
    left_hint = SMALLFONT.render("[-]", True, (150, 170, 200))
    right_hint = SMALLFONT.render("[+]", True, (150, 170, 200))
    DISPLAY.blit(left_hint, (x - 30, y + 25))
    DISPLAY.blit(right_hint, (x + width + 35, y + 25))


def draw_superweapon_option(x, y, name, selected, index):
    """Draw a superweapon option"""
    box_width = 140
    box_height = 40
    
    if selected:
        # Glow effect
        for i in range(6, 0, -2):
            glow_surf = pygame.Surface((box_width + i*2, box_height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 200, 255, 60), glow_surf.get_rect(), border_radius=8)
            DISPLAY.blit(glow_surf, (x - i, y - i))
        
        pygame.draw.rect(DISPLAY, (0, 200, 255), (x, y, box_width, box_height), 2, border_radius=8)
        text_color = WHITE
    else:
        pygame.draw.rect(DISPLAY, (50, 70, 90), (x, y, box_width, box_height), 1, border_radius=8)
        text_color = (180, 180, 180)
    
    # Weapon name
    text_surf = FONT.render(name, True, text_color)
    text_x = x + box_width//2 - text_surf.get_width()//2
    text_y = y + box_height//2 - text_surf.get_height()//2
    DISPLAY.blit(text_surf, (text_x, text_y))


def upgrade_menu(game_settings):
    """Upgrade menu for player stats"""
    global STATS1, STATS2
    
    # Initialize upgrade values
    speed_upgrade = 4
    maneuver_upgrade = 4
    rocket_upgrade = 4
    superweapon_idx = 1  # 0: Plasma Blast, 1: Light Speed, 2: Gravity Well
    
    money = 1000
    upgrade_cost = 100
    
    selected_upgrade = 0  # 0: Speed, 1: Maneuver, 2: Rocket, 3: Superweapon
    selected_button = 0  # 0: Start Game, 1: Main Menu
    
    superweapons = ["Plasma Blast", "Light Speed", "Gravity Well"]
    
    CYAN = (0, 255, 255)
    CYAN_DARK = (0, 150, 200)
    
    menu_running = True
    
    while menu_running:
        # Clear screen
        DISPLAY.fill((5, 10, 25))
        
        # Draw stars
        draw_stars()
        
        # Draw grid at bottom
        draw_grid()
        
        # Draw corner frames
        draw_corner_frame()
        
        # Title
        title_text = "SPACE FIGHTERS"
        title = SPACEFONT.render(title_text, True, CYAN)
        title_x = SCREENWIDTH//2 - title.get_width()//2
        
        for i in range(12, 0, -3):
            glow_surf = SPACEFONT.render(title_text, True, CYAN_DARK)
            glow_surf.set_alpha(int(100 / (i//3 + 1)))
            DISPLAY.blit(glow_surf, (title_x, 20))
        DISPLAY.blit(title, (title_x, 20))
        
        # Subtitle
        subtitle1 = MEDFONT.render("Which mode would you like to play?", True, (150, 170, 200))
        subtitle1_x = SCREENWIDTH//2 - subtitle1.get_width()//2
        DISPLAY.blit(subtitle1, (subtitle1_x, 70))
        
        player_name = game_settings["player1_name"]
        subtitle2 = MEDFONT.render(f"Player 1: {player_name} - Select Your Upgrades", True, CYAN)
        subtitle2_x = SCREENWIDTH//2 - subtitle2.get_width()//2
        DISPLAY.blit(subtitle2, (subtitle2_x, 100))
        
        # Main frame
        frame_x = 80
        frame_y = 130
        frame_width = SCREENWIDTH - 160
        frame_height = 350
        
        # Frame glow
        for i in range(10, 0, -2):
            glow_surf = pygame.Surface((frame_width + i*2, frame_height + i*2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (0, 200, 255, int(60 / (i//2 + 1))), (0, 0, frame_width + i*2, frame_height + i*2), border_radius=15)
            DISPLAY.blit(glow_surf, (frame_x - i, frame_y - i))
        
        # Main frame background
        pygame.draw.rect(DISPLAY, (10, 30, 50, 200), (frame_x, frame_y, frame_width, frame_height), border_radius=15)
        pygame.draw.rect(DISPLAY, CYAN, (frame_x, frame_y, frame_width, frame_height), 3, border_radius=15)
        
        # Money display
        money_text = FONT.render(f"Money left for Upgrades: {money} $", True, (255, 200, 0))
        money_x = frame_x + frame_width//2 - money_text.get_width()//2
        DISPLAY.blit(money_text, (money_x, frame_y + 20))
        
        # Upgrade bars
        bar_y = frame_y + 60
        bar_width = 250
        bar_height = 15
        
        draw_upgrade_bar(frame_x + 50, bar_y, bar_width, bar_height, speed_upgrade, 10, "Ship Speed")
        draw_upgrade_bar(frame_x + 50, bar_y + 50, bar_width, bar_height, maneuver_upgrade, 10, "Maneuverability")
        draw_upgrade_bar(frame_x + 50, bar_y + 100, bar_width, bar_height, rocket_upgrade, 10, "Rocket Max Speed")
        
        # Superweapon selection
        superweapon_y = bar_y + 160
        super_label = FONT.render("Choose your Superweapon:", True, WHITE)
        DISPLAY.blit(super_label, (frame_x + 50, superweapon_y))
        
        sw_start_x = frame_x + 50
        sw_width = 140
        sw_gap = 10
        
        for i, sw_name in enumerate(superweapons):
            sw_x = sw_start_x + i * (sw_width + sw_gap)
            is_selected = (i == superweapon_idx)
            draw_superweapon_option(sw_x, superweapon_y + 25, sw_name, is_selected, i)
        
        # Ship preview on right side
        draw_ship_preview(frame_x + frame_width - 120, frame_y + 80, 1.5)
        
        # Particle effect in bottom right
        draw_particle_effect()
        
        # Buttons
        btn_width, btn_height = 160, 40
        btn_y = frame_y + frame_height + 20
        btn_start_x = frame_x + frame_width//2 - (btn_width * 2 + 20)//2
        
        # Start Game button
        start_color = (0, 150, 200)
        start_hover = (0, 220, 255)
        draw_button(btn_start_x, btn_y, btn_width, btn_height, "START GAME",
                   selected_button == 0, start_color, start_hover)
        
        # Main Menu button
        menu_color = (180, 50, 50)
        menu_hover = (255, 80, 80)
        draw_button(btn_start_x + btn_width + 20, btn_y, btn_width, btn_height, "MAIN MENU",
                   selected_button == 1, menu_color, menu_hover)
        
        # Control hints
        hint = SMALLFONT.render("[UP/DOWN] Select  |  [LEFT/RIGHT] Adjust  |  [ENTER] Confirm  |  [ESC] Back", True, (150, 170, 200))
        DISPLAY.blit(hint, (SCREENWIDTH//2 - hint.get_width()//2, SCREENHEIGHT - 50))
        
        scale_display()
        fpsClock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                handle_resize(event)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return None  # Go back to menu 2
                elif event.key == K_UP:
                    selected_upgrade = (selected_upgrade - 1) % 4
                elif event.key == K_DOWN:
                    selected_upgrade = (selected_upgrade + 1) % 4
                elif event.key == K_LEFT:
                    if selected_upgrade == 0 and speed_upgrade > 1 and money >= upgrade_cost:
                        speed_upgrade -= 1
                        money += upgrade_cost
                    elif selected_upgrade == 1 and maneuver_upgrade > 1 and money >= upgrade_cost:
                        maneuver_upgrade -= 1
                        money += upgrade_cost
                    elif selected_upgrade == 2 and rocket_upgrade > 1 and money >= upgrade_cost:
                        rocket_upgrade -= 1
                        money += upgrade_cost
                    elif selected_upgrade == 3:
                        superweapon_idx = (superweapon_idx - 1) % 3
                elif event.key == K_RIGHT:
                    if selected_upgrade == 0 and speed_upgrade < 10 and money >= upgrade_cost:
                        speed_upgrade += 1
                        money -= upgrade_cost
                    elif selected_upgrade == 1 and maneuver_upgrade < 10 and money >= upgrade_cost:
                        maneuver_upgrade += 1
                        money -= upgrade_cost
                    elif selected_upgrade == 2 and rocket_upgrade < 10 and money >= upgrade_cost:
                        rocket_upgrade += 1
                        money -= upgrade_cost
                    elif selected_upgrade == 3:
                        superweapon_idx = (superweapon_idx + 1) % 3
                elif event.key == K_RETURN:
                    if selected_button == 0:  # Start Game
                        # Apply upgrades to stats
                        STATS1[0] = speed_upgrade
                        STATS1[1] = maneuver_upgrade
                        STATS1[2] = rocket_upgrade
                        STATS1[3] = money
                        STATS1[4] = superweapon_idx + 1
                        
                        # For PvP, also set Player 2 defaults
                        if game_settings["mode"] == "PVP":
                            STATS2[0] = 4
                            STATS2[1] = 4
                            STATS2[2] = 4
                            STATS2[3] = 1000
                            STATS2[4] = 2
                        
                        save_stats(1)
                        save_stats(2)
                        
                        return game_settings
                    else:  # Main Menu
                        return None
                elif event.key == K_1:
                    selected_upgrade = 0
                elif event.key == K_2:
                    selected_upgrade = 1
                elif event.key == K_3:
                    selected_upgrade = 2
                elif event.key == K_4:
                    selected_upgrade = 3


def quick_game_pvp(game_settings):
    """Quick PvP game with stats from upgrade menu"""
    global STATS1, STATS2
    
    # Stats are already set by upgrade_menu
    save_stats(1)
    save_stats(2)
    
    # Launch game in PvP mode with selected map
    import main4players
    main4players.GAME_MODE = "PVP"
    main4players.PLAYERS = 2
    main4players.SELECTED_MAP = game_settings["map"]
    main4players.PLAYER1_NAME = game_settings["player1_name"]
    main4players.PLAYER2_NAME = game_settings["player2_name"]
    main4players.main()


def quick_game_pve(game_settings):
    """Quick PvE game with stats from upgrade menu"""
    global STATS1, STATS2
    
    # Stats are already set by upgrade_menu for Player 1
    # Set Player 2 (AI) defaults
    STATS2[0] = 4
    STATS2[1] = 4
    STATS2[2] = 4
    STATS2[3] = 1000
    STATS2[4] = 2
    
    save_stats(1)
    save_stats(2)
    
    # Launch game in PvE mode with selected map
    import main4players
    main4players.GAME_MODE = "PVE"
    main4players.PLAYERS = 2
    main4players.SELECTED_MAP = game_settings["map"]
    main4players.PLAYER1_NAME = game_settings["player1_name"]
    main4players.PLAYER2_NAME = "AI"
    main4players.main()


def show_map_info(game_settings):
    """Show map information screen before upgrade menu"""
    map_name = game_settings["map"]
    
    # Map info data
    if map_name == "Deep Space Arena":
        map_data = {
            "title": "Map 1",
            "name": "Deep Space Arena",
            "desc": "Bản đồ không gian tiêu chuẩn.",
            "features": [
                "Góc trái: điểm người chơi 1",
                "Góc phải: điểm người chơi 2 / AI",
                "Theo dõi kết quả trận đấu theo thời gian thực"
            ],
            "controls": [
                "Người chơi điều khiển tàu:",
                "  • Di chuyển trong không gian",
                "  • Né tránh vật cản và tấn công đối thủ",
                "Yếu tố kỹ năng quyết định kết quả trận đấu"
            ],
            "preview_color": (10, 20, 40),
            "black_hole": False,
            "asteroids": False,
            "reverse_gravity": False
        }
    elif map_name == "Gravity Chaos Zone":
        map_data = {
            "title": "Map 2",
            "name": "Gravity Chaos Zone",
            "desc": "Khu vực có hố đen có lực hút mạnh và các thiên thạch xung quanh.",
            "features": [
                "Đạn bắn / vụ nổ",
                "Kẻ địch, vật thể nguy hiểm, thiên thạch",
                "Tạo nhịp độ nhanh và tính thử thách"
            ],
            "special": [
                "Hiệu ứng lực hút:",
                "  • Tàu và vật thể bị kéo về phía hố đen"
            ],
            "preview_color": (20, 10, 30),
            "black_hole": True,
            "asteroids": True,
            "reverse_gravity": False
        }
    else:  # Reverse Gravity Zone
        map_data = {
            "title": "Map 3",
            "name": "Reverse Gravity Zone",
            "desc": "Môi trường không gian với hố đen và thiên thạch",
            "features": [
                "Hố đen trung tâm và thiên thạch xung quanh",
                "Trọng lực đảo ngược mỗi 14 giây",
                "Tăng độ khó và trải nghiệm chiến đấu linh hoạt"
            ],
            "special": [
                "Cơ chế đặc biệt:",
                "  • GRAVITY REVERSING IN: 14s",
                "  • Vòng mũi tên xoay quanh hố đen",
                "  • Đảo chiều lực hút/đẩy khi hết thời gian"
            ],
            "preview_color": (30, 10, 20),
            "black_hole": True,
            "asteroids": True,
            "reverse_gravity": True
        }
    
    while True:
        # Light background
        DISPLAY.fill((240, 245, 250))
        
        # Header with icon
        header_icon = pygame.Rect(50, 30, 30, 30)
        pygame.draw.rect(DISPLAY, (0, 100, 200), header_icon)
        
        header = BIGFONT.render("Ship Customization Interface", True, (0, 80, 160))
        DISPLAY.blit(header, (90, 30))
        
        # Left panel - Info
        panel_x = 50
        panel_y = 80
        panel_width = 350
        panel_height = 450
        
        # Panel background
        pygame.draw.rect(DISPLAY, (255, 255, 255), (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(DISPLAY, (200, 210, 220), (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)
        
        y_offset = panel_y + 20
        
        # Map title
        map_title = BIGFONT.render(map_data["title"], True, (0, 100, 200))
        DISPLAY.blit(map_title, (panel_x + 20, y_offset))
        y_offset += 40
        
        # Map name
        name_text = MEDFONT.render(map_data["name"], True, (50, 50, 50))
        DISPLAY.blit(name_text, (panel_x + 20, y_offset))
        y_offset += 35
        
        # Description
        desc_text = FONT.render(map_data["desc"], True, (80, 80, 80))
        DISPLAY.blit(desc_text, (panel_x + 20, y_offset))
        y_offset += 40
        
        # Score System
        score_title = MEDFONT.render("Score System", True, (0, 100, 200))
        DISPLAY.blit(score_title, (panel_x + 20, y_offset))
        y_offset += 30
        
        for feature in map_data["features"]:
            bullet = FONT.render("• " + feature, True, (80, 80, 80))
            DISPLAY.blit(bullet, (panel_x + 30, y_offset))
            y_offset += 22
        
        y_offset += 15
        
        # Player Control
        control_title = MEDFONT.render("Player Control", True, (0, 100, 200))
        DISPLAY.blit(control_title, (panel_x + 20, y_offset))
        y_offset += 30
        
        if "controls" in map_data:
            for control in map_data["controls"]:
                control_text = FONT.render(control, True, (80, 80, 80))
                DISPLAY.blit(control_text, (panel_x + 30, y_offset))
                y_offset += 22
        
        if "special" in map_data:
            for special in map_data["special"]:
                special_text = FONT.render(special, True, (100, 50, 150))
                DISPLAY.blit(special_text, (panel_x + 30, y_offset))
                y_offset += 22
        
        # Right panel - Gameplay preview
        preview_x = 420
        preview_y = 80
        preview_width = 330
        preview_height = 400
        
        # Preview background (space)
        pygame.draw.rect(DISPLAY, map_data["preview_color"], (preview_x, preview_y, preview_width, preview_height))
        
        # Stars in preview
        for i in range(20):
            star_x = preview_x + (i * 37) % preview_width
            star_y = preview_y + (i * 23) % preview_height
            pygame.draw.circle(DISPLAY, (255, 255, 255, 150), (star_x, star_y), 1)
        
        # Draw black hole if needed
        if map_data["black_hole"]:
            bh_x = preview_x + preview_width // 2
            bh_y = preview_y + preview_height // 2
            
            # Black hole glow
            for r in range(40, 10, -5):
                color_val = 50 + r
                pygame.draw.circle(DISPLAY, (color_val, 0, color_val), (bh_x, bh_y), r)
            pygame.draw.circle(DISPLAY, (0, 0, 0), (bh_x, bh_y), 15)
            
            # Reverse gravity indicator
            if map_data["reverse_gravity"]:
                timer_text = FONT.render("GRAVITY REVERSING IN: 14s", True, (255, 100, 100))
                DISPLAY.blit(timer_text, (preview_x + 80, preview_y + 20))
                
                # Arrow indicators
                arrow_y = bh_y - 50
                pygame.draw.polygon(DISPLAY, (100, 255, 100), [
                    (bh_x, arrow_y), (bh_x - 10, arrow_y + 15), (bh_x + 10, arrow_y + 15)
                ])  # Up
                pygame.draw.polygon(DISPLAY, (100, 255, 100), [
                    (bh_x, arrow_y + 100), (bh_x - 10, arrow_y + 85), (bh_x + 10, arrow_y + 85)
                ])  # Down
        
        # Draw asteroids
        if map_data["asteroids"]:
            for i in range(5):
                ast_x = preview_x + 50 + i * 60
                ast_y = preview_y + 80 + (i % 2) * 200
                pygame.draw.circle(DISPLAY, (150, 120, 100), (ast_x, ast_y), 15)
                pygame.draw.circle(DISPLAY, (120, 90, 70), (ast_x, ast_y), 12)
        
        # Draw ships
        ship1_x = preview_x + 80
        ship1_y = preview_y + 320
        ship2_x = preview_x + 250
        ship2_y = preview_y + 100
        
        # Simple ship shapes
        pygame.draw.polygon(DISPLAY, (0, 150, 255), [
            (ship1_x, ship1_y - 15), (ship1_x - 10, ship1_y + 10), (ship1_x + 10, ship1_y + 10)
        ])
        pygame.draw.polygon(DISPLAY, (255, 100, 100), [
            (ship2_x, ship2_y + 15), (ship2_x - 10, ship2_y - 10), (ship2_x + 10, ship2_y - 10)
        ])
        
        # Score HUD
        score1 = FONT.render("-3", True, (255, 100, 100))
        score2 = FONT.render("5", True, (100, 255, 100))
        DISPLAY.blit(score1, (preview_x + 10, preview_y + 10))
        DISPLAY.blit(score2, (preview_x + preview_width - 30, preview_y + 10))
        
        # Preview border
        pygame.draw.rect(DISPLAY, (180, 190, 200), (preview_x, preview_y, preview_width, preview_height), 3)
        
        # Continue hint
        hint = FONT.render("Press [ENTER] to continue", True, (100, 100, 100))
        DISPLAY.blit(hint, (SCREENWIDTH//2 - hint.get_width()//2, SCREENHEIGHT - 40))
        
        scale_display()
        fpsClock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                handle_resize(event)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return None
                elif event.key == K_RETURN:
                    return game_settings


def main():
    global PLAYERS
    # MAINLOOP
    reset_all_stats()
    pygame.mixer.music.play(0, 0)

    while True:
        # Show mode selection menu
        mode = show_mode_menu()
        
        if mode is None:
            continue
        
        # Show game setup menu (map selection, player name)
        game_settings = game_setup_menu(mode)
        
        if game_settings is None:
            continue  # User pressed Back, return to mode selection
        
        # Show map info screen
        game_settings = show_map_info(game_settings)
        
        if game_settings is None:
            continue  # User pressed Back, return to game setup
        
        # Show upgrade menu
        upgrade_settings = upgrade_menu(game_settings)
        
        if upgrade_settings is None:
            continue  # User pressed Back, return to map info
        
        if mode == "PVP":
            quick_game_pvp(upgrade_settings)
        else:
            quick_game_pve(upgrade_settings)


if __name__ == "__main__":
    main()
