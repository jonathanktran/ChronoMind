"""This file is the main class, which runs the game."""

from run import run
from display import *
from enemies.bullet import *
from rounds.straight import *
import player


# Add some enemies
enemy_create(Bullet(0, 0, 1/2,  1/2, (255, 0, 0)))

# Add a round
rounds.round_create(Straight(Bullet, DISPLAY_WIDTH/2, 0, 1, 2, (0, 255, 0), 100, 1000))

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Run the game
run(player, enemies, rounds.rounds)

# Close the window
pg.quit()

