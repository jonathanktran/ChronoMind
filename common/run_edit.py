"""This file contains the run method, which runs the game"""


from display import *
import fonts
import time_control
import math
import timeline

import sys
sys.path.insert(0,"../neurosky")
import add_attention

def run(player, enemies, rounds, audio):
    """This function is a loop which runs a number of times per second, given by the FPS value in display.

    :param player: The player object
    :param enemies: A dictionary of all current enemies. The keys are the enemies' corresponding  id numbers.
    :param rounds: A dictionary of all current rounds. The keys rae the rounds' corresponding id numbers.
    :param audio: An audio file used to play music.
    """

    # Store the current time
    time = 0

    # Start the first timeline, if there is any
    timeline.check(0, 1)

    # Tick the clock once to remove delays
    clock.tick(FPS)

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed.
        dt = clock.tick(FPS) * time_control.time_mult

        # Find the current time
        time += dt

        # Check the timeline for each ms that we just covered
        timeline.check(time, dt)

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

                # Increase the time multiplier if the up arrow is pressed
                elif event.key == pg.K_UP:
                    audio.set_rate(min(time_control.time_mult / time_control.DELTA_TIME_MULT, time_control.MAX_TIME_MULT))
                    time_control.time_mult = min(time_control.time_mult / time_control.DELTA_TIME_MULT, time_control.MAX_TIME_MULT)

                # Decrease the time multiplier if the down arrow is pressed
                elif event.key == pg.K_DOWN:
                    audio.set_rate(max(time_control.time_mult * time_control.DELTA_TIME_MULT, time_control.MIN_TIME_MULT))
                    time_control.time_mult = max(time_control.time_mult * time_control.DELTA_TIME_MULT, time_control.MIN_TIME_MULT)

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

        # Draw the time multiplier
        time_mult_surface = fonts.HUD.render('Time Multiplier: ' + str(time_control.time_mult), False, (0, 0, 0))
        display.blit(time_mult_surface, (DISPLAY_WIDTH/2 - time_surface.get_width()/2, 32))

        # Draw the attention level
        attention = add_attention.get_attention()
        attention_surface = fonts.HUD.render('Attention: ' + str(attention), False, (0, 0, 0))
        display.blit(attention_surface, (32, 600))

        # endregion Draw the HUD

        # endregion Drawing

        # Update the window
        pg.display.update()
