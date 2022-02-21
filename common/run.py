"""This file contains the run method, which runs the game"""


from display import *
import fonts
import time_control
import math
import timeline
import attention
from neurosky.interface import get_attention


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

        # Get the current attention level
        current_attention = get_attention()

        # Set the time multiplier based on the attention measure
        time_control.time_mult = attention.get_time_mult(current_attention)

        # Match the audio playback speed to the time multiplier
        audio.set_rate(time_control.time_mult)

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
        display.blit(time_mult_surface, (DISPLAY_WIDTH/2 - time_mult_surface.get_width()/2, 32))

        # Draw the time multiplier
        attention_surface = fonts.HUD.render('Attention: ' + str(current_attention), False, (0, 0, 0))
        display.blit(attention_surface, (32, DISPLAY_HEIGHT - attention_surface.get_height() - 32))

        # endregion Draw the HUD

        # endregion Drawing

        # Update the window
        pg.display.update()
