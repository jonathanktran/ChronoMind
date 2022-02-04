"""This file is the main class, which runs the game."""

from run import run
from display import *
from enemies.bullet import *
from rounds.straight import *
import player

# Initialize the mixer
pg.mixer.init()

# Play music
pg.mixer.music.load('assets/music/Megalovania.ogg')
pg.mixer.music.play()

# Add a round
rounds.round_create(Straight(Bullet, 0, DISPLAY_HEIGHT/2, 1/2, 0, (0, 255, 0), 1000, 500))

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Run the game
run(player, enemies, rounds.rounds)

# Close the window
pg.quit()

