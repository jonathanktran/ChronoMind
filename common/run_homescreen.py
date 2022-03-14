"""This file contains the run function, which runs the homescreen portion of the game."""
import pygame

from display import *
import fonts
from gui import Button
import color


def run_credits():

    # Create a list of buttons
    back = Button((DISPLAY_WIDTH / 9, DISPLAY_HEIGHT / 8), (DISPLAY_WIDTH / 9, DISPLAY_HEIGHT / 9), color.ORANGE,
                  color.WHITE, fonts.BACK.render('Back', True, color.BLACK))

    window = pg.display.set_mode((0,0), pg.FULLSCREEN)
    text = fonts.BACK.render("Credits", True, color.WHITE)
    text2 = fonts.CREDITSTEXT.render("~ Level & Graphic Design by Jeff & Jonny", True, color.WHITE)
    text3 = fonts.CREDITSTEXT.render("~ Audio Wavelet Transforms (Music) by Will", True, color.WHITE)
    text4 = fonts.CREDITSTEXT.render("~ Extracting raw EEG data by Meghana & Jonny", True, color.WHITE)
    text5 = fonts.CREDITSTEXT.render("~ Game Design and Implementation by Will & Zytal", True, color.WHITE)
    text6 = fonts.CREDITSTEXT.render("~ Home Screen and Headset Calibration by Will & Janty", True, color.WHITE)
    text7= fonts.CREDITSTEXT.render("~ Smoothing & Filtering Raw EEG data to get Attention Level Measure"
                                     "and Baseline Attention by Meghana", True, color.WHITE)

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
        display.fill((195, 148, 255))

        # Adds text onto screen
        window.blit(text, (DISPLAY_WIDTH / 2.2, DISPLAY_HEIGHT / 6.5))
        window.blit(text2, (DISPLAY_WIDTH / 5, DISPLAY_HEIGHT / 3.8))
        window.blit(text3, (DISPLAY_WIDTH / 5, DISPLAY_HEIGHT / 2.95))
        window.blit(text4, (DISPLAY_WIDTH / 5, DISPLAY_HEIGHT / 2.38))
        window.blit(text5, (DISPLAY_WIDTH / 5, DISPLAY_HEIGHT / 1.99))
        window.blit(text6, (DISPLAY_WIDTH / 5, DISPLAY_HEIGHT / 1.71))
        window.blit(text7, (DISPLAY_WIDTH / 5, DISPLAY_HEIGHT / 1.5))

        # Draw all buttons
        if back.press(pg.mouse.get_pos()): back.draw_hover()
        else: back.draw_unhover()

        # Draw the mouse
        pg.draw.circle(display, color.DARKGREEN, pg.mouse.get_pos(), 16)

        # endregion Draw the HUD

        # Update the window
        pg.display.update()




def run_homescreen():
    """This function is a loop which runs a number of times per second, given by the FPS value in display.
    This displays the homescreen portion of the game.
    """

    # Create a list of buttons
    play = Button((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT/3), (DISPLAY_WIDTH / 8, DISPLAY_HEIGHT / 8), color.ORANGE,
                  color.WHITE, fonts.HUD.render('Play', True, color.BLACK))

    credits = Button((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT /2), (DISPLAY_WIDTH / 8, DISPLAY_HEIGHT / 8), color.ORANGE,
               color.WHITE, fonts.CREDITS.render('Credits', True, color.BLACK))

    quit = Button((DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 1.5), (DISPLAY_WIDTH / 8, DISPLAY_HEIGHT / 8), color.ORANGE,
               color.WHITE, fonts.QUIT.render('Quit', True, color.BLACK))

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
        display.fill((84, 216, 255))

        # Draw all buttons
        if play.press(pg.mouse.get_pos()): play.draw_hover()
        else: play.draw_unhover()

        if credits.press(pg.mouse.get_pos()): credits.draw_hover()
        else: credits.draw_unhover()

        if quit.press(pg.mouse.get_pos()): quit.draw_hover()
        else: quit.draw_unhover()

        # Draw the mouse
        pg.draw.circle(display, color.DARKGREEN, pg.mouse.get_pos(), 16)

        # endregion Draw the HUD

        # Update the window
        pg.display.update()