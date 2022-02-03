"""This file is the main class, which runs the game."""

import pygame as pg

from run import run
from display import *
from enemies import bullet
import player

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Create enemies
enemies = [
    bullet.Bullet(0, 0, 1/4, 1/4, (0, 0, 255))
]

# Run the game
run(player, enemies)

# Close the window
pg.quit()

