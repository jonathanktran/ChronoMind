"""This file contains the run method, which runs the game"""

from display import *
import fonts


def run(player, enemies, rounds):

    # Run the game until it is quit out of
    while True:

        # Tick the game forward once
        dt = clock.tick(FPS)

        # region Events

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

        # endregion Events

        # region Steps

        # Run the player's step event
        player.step(dt, list(enemies.values()))

        # Run the step event of every round
        for round in list(rounds.values()):
            round.step(dt)

        # Run the step event of every enemy
        for enemy in list(enemies.values()):
            enemy.step(dt)

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
        lives_surface = fonts.lives.render('Lives: ' + str(player.lives), False, (0, 0, 0))
        display.blit(lives_surface, (32, 32))

        # endregion Draw the HUD

        # endregion Drawing

        # Update the window
        pg.display.update()
