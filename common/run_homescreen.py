"""This file contains the run function, which runs the homescreen portion of the game."""
import pygame

from display import *
import fonts
from gui import Button
import color

def run_credits():
    # Create a list of buttons
    back = Button((DISPLAY_WIDTH / 9, DISPLAY_HEIGHT / 8), (DISPLAY_WIDTH / 9, DISPLAY_HEIGHT / 9), color.WHITE,
                  fonts.BACK.render('Back', True, color.BLACK))


    # Run the game until it is quit
    while True:

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

            # Check if the mouse is pressed
            if event.type == pg.MOUSEBUTTONDOWN:

                # Check button presses if the left mouse button in pressed
                if event.button == pg.BUTTON_LEFT:
                    if back.press(pg.mouse.get_pos()):
                        return False


        # endregion Events

        # region Draw the HUD

        # Draw the background
        display.fill((210, 173, 255))

        # Draw all buttons
        back.draw()

        # Draw the mouse
        pg.draw.circle(display, color.GREEN, pg.mouse.get_pos(), 16)

        # endregion Draw the HUD

        # Update the window
        pg.display.update()




def run_homescreen():
    """This function is a loop which runs a number of times per second, given by the FPS value in display.
    This displays the homescreen portion of the game.
    """

    # Create a list of buttons
    play = Button((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT/3), (DISPLAY_WIDTH / 8, DISPLAY_HEIGHT / 8), color.WHITE,
               fonts.HUD.render('Play', True, color.BLACK))

    credits = Button((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT /2), (DISPLAY_WIDTH / 8, DISPLAY_HEIGHT / 8), color.WHITE,
               fonts.CREDITS.render('Credits', True, color.BLACK))

    quit = Button((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 1.5), (DISPLAY_WIDTH / 8, DISPLAY_HEIGHT / 8), color.WHITE,
               fonts.QUIT.render('Quit', True, color.BLACK))

    # Run the game until it is quit
    while True:

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

            # Check if the mouse is pressed
            if event.type == pg.MOUSEBUTTONDOWN:

                # Check button presses if the left mouse button in pressed
                if event.button == pg.BUTTON_LEFT:
                    if play.press(pg.mouse.get_pos()):
                        return False

                    if quit.press(pg.mouse.get_pos()):
                        return True

                    if credits.press(pg.mouse.get_pos()):
                        if run_credits():
                            return True



        # endregion Events

        # region Draw the HUD

        # Draw the background
        display.fill((59, 210, 255))

        # Draw all buttons
        play.draw()
        credits.draw()
        quit.draw()

        # Draw the mouse
        pg.draw.circle(display, color.GREEN, pg.mouse.get_pos(), 16)

        # endregion Draw the HUD

        # Update the window
        pg.display.update()