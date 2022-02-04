"""This file contains the run method, which runs the game"""


from display import *
import fonts
import common.rounds
from common.rounds.straight import Straight
from common.rounds.sprinkler import Sprinkler
from common.enemies.bullet import Bullet
import builtins

test = [False] * 3


def run(player, enemies, rounds):

    # Run the game until it is quit out of
    while True:

        # Tick the game forward once
        dt = clock.tick(FPS)

        global test
        if pg.time.get_ticks() > 8000 and not test[0]:
            common.rounds.round_create(Straight(Bullet, DISPLAY_WIDTH/2, 0, 0, 1/2, (0, 255, 0), 1000, 500))
            test[0] = True
        if pg.time.get_ticks() > 16000 and not test[1]:
            common.rounds.round_create(Sprinkler(Bullet, DISPLAY_WIDTH, DISPLAY_HEIGHT/2, 3/4, 180, 135, 225, 90, (0, 255, 0), 1000, 250))
            test[1] = True
        if pg.time.get_ticks() > 24000 and not test[2]:
            common.rounds.round_create(Sprinkler(Bullet, DISPLAY_WIDTH/2, DISPLAY_HEIGHT, 3/4, 270, 225, 315, 90, (0, 255, 0), 1000, 250))
            test[2] = True

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

        # Draw the time
        time_surface = fonts.lives.render('Time: ' + str(builtins.round(pg.time.get_ticks()/100)), False, (0, 0, 0))
        display.blit(time_surface, (DISPLAY_WIDTH - time_surface.get_width() - 32, 32))

        # endregion Draw the HUD

        # endregion Drawing

        # Update the window
        pg.display.update()
