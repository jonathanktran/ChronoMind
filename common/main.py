"""This file is the main class, which runs the game."""

from run import run
from display import *
from enemies import enemy_list
from rounds import round_list
import player
import music

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Start the music
pg.mixer.music.play()

# Run the game
run(player, enemy_list, round_list)

# Close the window
pg.quit()
