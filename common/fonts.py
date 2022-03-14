"""This file contains all the fonts used in the game"""

import pygame as pg


# Initialize the fonts
pg.font.init()

# The font used to display the hud
HUD = pg.font.SysFont('Trebuchet MS', 50)

# The font used to display the maths letters
MATH = pg.font.SysFont('Comic Sans MS', 60)

# The font used for the Credits Button
CREDITS = pg.font.SysFont('Trebuchet MS', 50)

# The font used for the Credits Text
CREDITSTEXT = pg.font.SysFont('Trebuchet MS', 30)

# The font used for the Quit Button
QUIT = pg.font.SysFont('Trebuchet MS', 50)

# The font used for the Back Button
BACK = pg.font.SysFont('Trebuchet MS', 50)
