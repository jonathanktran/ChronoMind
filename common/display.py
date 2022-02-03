"""This file creates the display for the game."""

import pygame as pg


# Initialize the game
pg.init()

# Find the width and height of the screen
DISPLAY_WIDTH, DISPLAY_HEIGHT = pg.display.Info().current_w, pg.display.Info().current_h

# Set the FPS of the game
FPS = 60

# Create the display
display = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), vsync=1)

# Set the title
pg.display.set_caption("ChronoMind")

# Get a clock for the display
clock = pg.time.Clock()

# Set the mouse to be invisible
pg.mouse.set_visible(False)
