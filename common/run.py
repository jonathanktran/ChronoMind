"""This file contains the run method, which runs the game"""

import builtins
from display import *
import fonts
import math
import timeline
import attention
import neurosky.interface as interface
BGIMAGE = pg.image.load('../assets/sprites/background.jpg').convert_alpha()
GOIMAGE = pg.image.load('../assets/sprites/game_over.png').convert_alpha()
r = GOIMAGE.get_rect()
r.center = display.get_rect().center


def run(player, enemies, rounds, calibration_setting, att_object):
    """This function is a loop which runs a number of times per second, given by the FPS value in display.

    :param player: The player object
    :param enemies: A dictionary of all current enemies. The keys are the enemies' corresponding  id numbers.
    :param rounds: A dictionary of all current rounds. The keys rae the rounds' corresponding id numbers.
    :param calibration_setting: The settings used to calibrate the attention bounds.
    :param att_object: The object of the class AttentionMeasure measuring the current attention
    """

    # Store the current time
    time = 0

    # Store the real time
    realtime = 0

    # Start the first timeline, if there is any
    timeline.check(0, 1)

    # The current time multiplier
    time_mult = 1

    # Add the first 8 seconds of enemies
    timeline.add_level(0)
    timeline.add_level(4000)

    # Tick the clock once to remove delays
    clock.tick(FPS)

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed, and store that time
        dt = clock.tick(FPS)

        # Store the real amount of time that has passed
        realtime += dt

        # Set the time multiplier based on the attention measure
        current_attention = att_object.curr_attention
        time_mult = attention.get_time_mult(current_attention, calibration_setting)

        # Adjust the time by the time multiplier
        dt = dt * time_mult

        # Add new enemies and rounds to the timeline every 4 seconds
        if time % 4000 > (time + dt) % 4000: timeline.add_level(int(time) + 4000)

        # Find the current time
        time += dt

        # Check the timeline for each ms that we just covered
        timeline.check(time, dt)

        # region Events

        # Check for events
        for event in pg.event.get():

            # If the game is quit, end the game
            if event.type == pg.QUIT:
                return True

            # Check for keyboard presses
            if event.type == pg.KEYDOWN:

                # End the game if the escape key is pressed
                if event.key == pg.K_ESCAPE:
                    return True

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
        display.blit(BGIMAGE, (0, 0))

        # Draw the player
        player.draw(display)

        # Draw all enemies
        for enemy in enemies.values():
            enemy.draw(display)

        # region Draw the HUD

        # Draw the number of lives

        pg.draw.rect(display, (255, 0, 0), (10, 10, 300 * (player.lives / player.MAX_LIVES), 25))
        pg.draw.rect(display, (255, 255, 255), (10, 10, 300, 25), 4)

        # If the player runs out of lives, end game and return to home screen
        if player.lives == 0:
            display.blit(GOIMAGE, r)
            pg.display.flip()
            pg.event.pump()
            pg.time.delay(2000)
            return False

        # Draw the time
        time_surface = fonts.HUD.render('Time: ' + str(math.floor(time/1000)), False, (255, 255, 255))
        display.blit(time_surface, (DISPLAY_WIDTH - time_surface.get_width() - 32, 32))

        # Draw the time multiplier
        time_mult_surface = fonts.HUD.render('Time Multiplier: ' + "{:.2f}".format(time_mult), False, (255, 255, 255))
        display.blit(time_mult_surface, (DISPLAY_WIDTH/2 - time_mult_surface.get_width()/2, 32))

        # Draw the time multiplier
        attention_surface = fonts.HUD.render('Attention: ' + str(builtins.round(current_attention)), False, (255, 255, 255))
        display.blit(attention_surface, (32, DISPLAY_HEIGHT - attention_surface.get_height() - 32))

        # Update the window
        pg.display.update()
