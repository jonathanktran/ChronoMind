"""This file is the main class, which runs the game."""

from run import run
from display import *
from enemies.bullet import *
from rounds.straight import *
import player
import music

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Start the music
pg.mixer.music.play()

#enemy_create(Bullet(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, 0, 0, (0, 0, 0)))

# Run the game
run(player, enemies, rounds.rounds)

# Close the window
pg.quit()

