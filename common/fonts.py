"""This file contains all the fonts used in the game"""

import pygame as pg


# Initialize the fonts
pg.font.init()

# The font used to display the hud
HUD = pg.font.Font('../assets/Fonts/MonsterFriendFore.otf', 50)

# The font used to display the maths letters
MATH = pg.font.Font('../assets/Fonts/MonsterFriendFore.otf', 60)

# The font used for the Credits Button
CREDITS = pg.font.Font('../assets/Fonts/MonsterFriendFore.otf', 50)

# The font used for the Credits Text
CREDITSTEXT = pg.font.Font('../assets/Fonts/MonsterFriendFore.otf', 30)

# The font used for the Quit Button
QUIT = pg.font.Font('../assets/Fonts/MonsterFriendFore.otf', 50)

# The font used for the Back Button
BACK = pg.font.Font('../assets/Fonts/MonsterFriendFore.otf', 50)
