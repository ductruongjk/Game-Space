#!/usr/bin/env python3
"""
Space Fighters - Main Entry Point
A space shooter game with PvP, PvE, multiple maps, and upgrade system.
"""
import sys
import pygame
from pygame.locals import *

# Import our modules
from settings import *
from menu import MainMenu, MapSelect, WinnerScreen
from upgrades import UpgradeScreen
from game import Game


def load_stats(player_num):
    """Load player stats from file [speed, maneuver, rocket, money, superweapon]"""
    try:
        with open(f"stats{player_num}.txt", "r") as f:
            content = f.read().strip()
            # Parse list format
            if content.startswith('[') and content.endswith(']'):
                stats = [int(x.strip()) for x in content[1:-1].split(',')]
                if len(stats) >= 5:
                    return stats
    except:
        pass
    # Default stats
    return [1, 1, 1, STARTING_MONEY, SUPERWEAPON_LIGHTSPEED]


def save_stats(player_num, stats):
    """Save player stats to file"""
    try:
        with open(f"stats{player_num}.txt", "w") as f:
            f.write(str(stats))
    except:
        print(f"Warning: Could not save stats for player {player_num}")


def calculate_reward(winner, is_pve):
    """Calculate money reward based on win/loss"""
    if is_pve:
        if winner == 1:  # Player won against AI
            return UPGRADE_REWARD_WIN_PVE
        else:  # AI won
            return UPGRADE_REWARD_LOSS_PVE
    else:
        if winner == 1:  # P1 won
            return UPGRADE_REWARD_WIN_PVP
        else:  # P2 won
            return UPGRADE_REWARD_LOSS_PVP


def main():
    """Main game loop with menu flow"""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create window (fullscreen option available)
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Space Fighters")
    
    # Try to load icon
    try:
        icon = pygame.image.load('resources/ship1.png')
        pygame.display.set_icon(icon)
    except:
        pass
    
    # Create virtual surface for scaling
    virtual_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Hide mouse cursor
    pygame.mouse.set_visible(0)
    
    # Main menu loop
    while True:
        # Show main menu
        menu = MainMenu(window, virtual_surf)
        game_mode = menu.show()
        
        if game_mode is None:
            break  # Quit selected
        
        # Show map selection
        map_select = MapSelect(window, virtual_surf)
        map_name = map_select.show()
        
        if map_name == "back":
            continue  # Go back to main menu
        
        # Load current stats
        stats1 = load_stats(1)
        stats2 = load_stats(2)
        
        # Show upgrade screen for Player 1
        upgrade1 = UpgradeScreen(window, virtual_surf, 1, stats1, stats1[3], is_ai=False)
        new_stats1 = upgrade1.show()
        
        if new_stats1 is None:
            continue  # ESC pressed, go back
        
        save_stats(1, new_stats1)
        
        # For PvP, show upgrade for Player 2
        if game_mode == GAME_MODE_PVP:
            upgrade2 = UpgradeScreen(window, virtual_surf, 2, stats2, stats2[3], is_ai=False)
            new_stats2 = upgrade2.show()
            
            if new_stats2 is None:
                continue
            
            save_stats(2, new_stats2)
        else:
            # For PvE, AI gets random upgrades
            upgrade2 = UpgradeScreen(window, virtual_surf, 2, stats2, stats2[3], is_ai=True)
            new_stats2 = upgrade2.show()
            save_stats(2, new_stats2)
        
        # Start game
        game = Game(window, virtual_surf, game_mode, map_name, new_stats1, new_stats2)
        result = game.run()
        
        if result is None:
            continue  # Game was interrupted
        
        # Calculate rewards
        winner = result['winner']
        money_earned = calculate_reward(winner, game_mode == GAME_MODE_PVE)
        
        # Update money for winner
        if winner == 1:
            new_stats1[3] += money_earned
            save_stats(1, new_stats1)
        else:
            new_stats2[3] += money_earned
            save_stats(2, new_stats2)
        
        # Show winner screen
        winner_screen = WinnerScreen(window, virtual_surf, winner, 
                                     result['p1_score'], result['p2_score'],
                                     game_mode == GAME_MODE_PVE, money_earned)
        winner_screen.show()
        
        # Loop back to menu for next match
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
