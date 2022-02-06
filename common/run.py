"""This file contains the run method, which runs the game"""


from display import *
import fonts
import common.rounds
from common.rounds.straight import Straight
from common.rounds.sprinkler import Sprinkler
from common.enemies.bullet import Bullet
import math


# Test Variables
test = [False] * 4


def run(player, enemies, rounds):
    """This function is a loop which runs a number of times per second, given by the FPS value in display.

    :param player: The player object
    :param enemies: A dictionary of all current enemies. The keys are the enemies' corresponding  id numbers.
    :param rounds: A dictionary of all current rounds. The keys rae the rounds' corresponding id numbers.
    """

    # Store the current time
    time = 0

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed.
        dt = clock.tick(FPS)

        # Find the current time
        time += dt

        # Game Testing
        global test
        if time >= 0 and not test[0]:
            common.rounds.round_create(Straight(Bullet, 0, DISPLAY_HEIGHT/2, DISPLAY_WIDTH, 0, (0, 255, 0), 1000, 500))
            test[0] = True
        if time >= 8000 and not test[1]:
            common.rounds.round_create(Straight(Bullet, DISPLAY_WIDTH/2, 0, 0, DISPLAY_HEIGHT, (0, 255, 0), 1000, 500))
            test[1] = True
        if time >= 16000 and not test[2]:
            common.rounds.round_create(Sprinkler(Bullet, DISPLAY_WIDTH, DISPLAY_HEIGHT/2, DISPLAY_WIDTH, 180, 135, 225, 30, (0, 255, 0), 1000, 250))
            test[2] = True
        if time >= 24000 and not test[3]:
            common.rounds.round_create(Sprinkler(Bullet, DISPLAY_WIDTH/2, DISPLAY_HEIGHT+8, DISPLAY_HEIGHT, 270, 225, 315, 30, (0, 255, 0), 1000, 250))
            test[3] = True

        # region Events

        # Check for events
        for event in pg.event.get():

            # If the game is quit, end the game
            if event.type == pg.QUIT:
                return

            # Check for keyboard presses
            if event.type == pg.KEYDOWN:

                # End the game if the escape key is pressed
                if event.key == pg.K_ESCAPE:
                    return

        # endregion Events

        # region Steps

        # Run the player's step event
        player.step(dt, list(enemies.values()))

        # Run the step event of every enemy
        for enemy in list(enemies.values()):
            enemy.step(dt)

        # Run the step event of every round
        for round in list(rounds.values()):
            round.step(dt)

        # endregion Steps

        # region Drawing

        # Draw the background
        display.fill((255, 255, 255))

        # Draw the player
        player.draw()

        # Draw all enemies
        for enemy in enemies.values():
            enemy.draw()

        # region Draw the HUD

        # Draw the number of lives
        lives_surface = fonts.HUD.render('Lives: ' + str(player.lives), False, (0, 0, 0))
        display.blit(lives_surface, (32, 32))

        # Draw the time
        time_surface = fonts.HUD.render('Time: ' + str(math.floor(time/1000)), False, (0, 0, 0))
        display.blit(time_surface, (DISPLAY_WIDTH - time_surface.get_width() - 32, 32))

        # endregion Draw the HUD

        # endregion Drawing

        # Update the window
        pg.display.update()
