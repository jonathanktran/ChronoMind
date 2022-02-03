"""This file contains the run method, which runs the game"""

from display import *


def run(player, enemies):

    # Run the game until it is quit out of
    while True:

        # Tick the game forward once
        dt = clock.tick(FPS)

        # Check for events
        for event in pg.event.get():

            # If the game is quit, end the game
            if event.type == pg.QUIT:
                return

            # Check for keyboard presses
            if event.type == pg.KEYDOWN:

                # Exit if the escape key is pressed
                if event.key == pg.K_ESCAPE:
                    return

        # Run the player's step event
        player.step(dt)

        # Run the step event of every enemy
        for enemy in enemies:
            enemy.step(dt)

        # Draw the background
        display.fill((255, 255, 255))

        # Draw the player
        player.draw()

        # Draw all enemies
        for enemy in enemies:
            enemy.draw()

        # Update the window
        pg.display.update()
