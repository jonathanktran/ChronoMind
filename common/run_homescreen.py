"""This file contains the run function, which runs the homescreen portion of the game."""

from display import *
import fonts
from gui import Button
import color


def run_homescreen():
    """This function is a loop which runs a number of times per second, given by the FPS value in display.
    This displays the homescreen portion of the game.
    """

    # Create a list of buttons
    buttons = [
        Button((DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2), (DISPLAY_WIDTH/8, DISPLAY_HEIGHT/8), color.RED,
               fonts.HUD.render('Play', False, color.BLACK))
    ]

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
                    for button in buttons:
                        if button.press(pg.mouse.get_pos()): return False

        # endregion Events

        # region Draw the HUD

        # Draw the background
        display.fill((255, 255, 255))

        # Draw all buttons
        for button in buttons:
            button.draw()

        # Draw the mouse
        pg.draw.circle(display, color.GREEN, pg.mouse.get_pos(), 16)

        # endregion Draw the HUD

        # Update the window
        pg.display.update()

