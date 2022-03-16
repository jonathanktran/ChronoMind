"""This file contains the run_homescreen function, which runs the homescreen portion of the game."""

from display import *
import fonts
from gui import Button
import color
from math import sin, pi


class Mouse:
    """This class is used to diplay the mouse."""

    # The amount of time the mouse wiggles
    MAX_WIGGLETIME = 1000

    def __init__(self):
        self.wiggletime = 0

    def step(self, dt):
        self.wiggletime = max(0, self.wiggletime - dt)

    def press(self):
        self.wiggletime = self.MAX_WIGGLETIME

    def draw(self):
        pg.draw.circle(display, color.PALE_BLUE, pg.mouse.get_pos(),
                       16 * ((self.wiggletime/1000) * (3/4) * sin(self.wiggletime * 2 * pi / 250) + 1))


def run_options(mouse, audio):

    # Create the window
    window = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    # The button to go back to the homescreen
    back = Button((DISPLAY_WIDTH/9, DISPLAY_HEIGHT/8), (DISPLAY_WIDTH/9, DISPLAY_HEIGHT/9), color.ORANGE,
                  color.WHITE, fonts.BACK.render('Back', True, color.BLACK), border_radius=16)

    # The button to increase the volume
    inc_vol = Button((DISPLAY_WIDTH/4, DISPLAY_HEIGHT/2), (DISPLAY_WIDTH/4.5, DISPLAY_HEIGHT/4.5), color.ORANGE,
                  color.WHITE, fonts.BACK.render('Decrease Volume', True, color.BLACK), border_radius=16)

    # The button to increase the volume
    dec_vol = Button((DISPLAY_WIDTH * (3/4), DISPLAY_HEIGHT/2), (DISPLAY_WIDTH/4.5, DISPLAY_HEIGHT/4.5), color.ORANGE,
                  color.WHITE, fonts.BACK.render('Increase Volume', True, color.BLACK), border_radius=16)

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed, and store that time
        dt = clock.tick(FPS)

        # Step the mouse
        mouse.step(dt)

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

                    # Press the mouse
                    mouse.press()

                    # Go back to the homescreen if the back button is pressed
                    if back.press(pg.mouse.get_pos()):
                        return False

                    # Increase the volume if in the increase volume button is pressed
                    if inc_vol.press(pg.mouse.get_pos()):
                        audio.set_volume(max(0, audio.volume - 0.01))

                    # Decrease the volume if in the decrease volume button is pressed
                    if dec_vol.press(pg.mouse.get_pos()):
                        audio.set_volume(min(0.2, audio.volume + 0.01))

        # endregion Events

        # region Draw the HUD

        # Draw the background
        display.fill((195, 148, 255))

        # Draw all buttons
        if back.press(pg.mouse.get_pos()): back.draw_hover()
        else: back.draw_unhover()

        if inc_vol.press(pg.mouse.get_pos()): inc_vol.draw_hover()
        else: inc_vol.draw_unhover()

        if dec_vol.press(pg.mouse.get_pos()): dec_vol.draw_hover()
        else: dec_vol.draw_unhover()

        # Draw the current volume
        text = fonts.HUD.render(f'{round(audio.volume * 500)}%', True, color.BLACK)
        window.blit(text, (DISPLAY_WIDTH/2 - text.get_width()/2, DISPLAY_HEIGHT/2 - text.get_height()/2))

        # Draw the mouse
        mouse.draw()

        # endregion Draw the HUD

        # Update the window
        pg.display.update()


def run_credits(mouse):

    # Create the window
    window = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    # The button to go back to the homescreen
    back = Button((DISPLAY_WIDTH/9, DISPLAY_HEIGHT/8), (DISPLAY_WIDTH/9, DISPLAY_HEIGHT/9), color.ORANGE,
                  color.WHITE, fonts.BACK.render('Back', True, color.BLACK), border_radius=16)

    # The text to display
    text =  fonts.BACK.render("CREDITS", True, color.WHITE)
    text2 = fonts.CREDITSTEXT.render("~ Graphic Design by Jeff and Janty ~", True, color.WHITE)
    text3 = fonts.CREDITSTEXT.render("~ Attention Measure by Meghana & Jonny ~", True, color.WHITE)
    text4 = fonts.CREDITSTEXT.render("~ Game Design and Implementation by Will & Zytal ~", True, color.WHITE)

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed, and store that time
        dt = clock.tick(FPS)

        # Step the mouse
        mouse.step(dt)

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

                    # Press the mouse
                    mouse.press()

                    if back.press(pg.mouse.get_pos()):
                        return False

        # endregion Events

        # region Draw the HUD

        # Draw the background
        display.fill((195, 148, 255))

        # Adds text onto screen
        window.blit(text, (DISPLAY_WIDTH/2 - text.get_width()/2, DISPLAY_HEIGHT/6.5))
        window.blit(text2, (DISPLAY_WIDTH/2 - text2.get_width()/2, DISPLAY_HEIGHT/3.8))
        window.blit(text3, (DISPLAY_WIDTH/2 - text3.get_width()/2, DISPLAY_HEIGHT/2.95))
        window.blit(text4, (DISPLAY_WIDTH/2 - text4.get_width()/2, DISPLAY_HEIGHT/2.38))

        # Draw all buttons
        if back.press(pg.mouse.get_pos()): back.draw_hover()
        else: back.draw_unhover()

        # Draw the mouse
        mouse.draw()

        # endregion Draw the HUD

        # Update the window
        pg.display.update()


def run_homescreen(audio):
    """This function is a loop which runs a number of times per second, given by the FPS value in display.
    This displays the homescreen portion of the game.
    """

    # Create the mouse
    mouse = Mouse()

    # The button used to start the game
    play = Button((DISPLAY_WIDTH/2, DISPLAY_HEIGHT * (8/24)), (DISPLAY_WIDTH/8, DISPLAY_HEIGHT/8), color.ORANGE,
                  color.WHITE, fonts.HUD.render('Play', True, color.BLACK), border_radius=16)

    # The button used to go to the credits page
    options = Button((DISPLAY_WIDTH/2, DISPLAY_HEIGHT * (12/24)), (DISPLAY_WIDTH/8, DISPLAY_HEIGHT/8), color.ORANGE,
               color.WHITE, fonts.CREDITS.render('Options', True, color.BLACK), border_radius=16)

    # The button used to go to the credits page
    credits = Button((DISPLAY_WIDTH/2, DISPLAY_HEIGHT * (16/24)), (DISPLAY_WIDTH/8, DISPLAY_HEIGHT/8), color.ORANGE,
               color.WHITE, fonts.CREDITS.render('Credits', True, color.BLACK), border_radius=16)

    # The button used to quit the game
    quit = Button((DISPLAY_WIDTH/2, DISPLAY_HEIGHT * (20/24)), (DISPLAY_WIDTH/8, DISPLAY_HEIGHT/8), color.ORANGE,
               color.WHITE, fonts.QUIT.render('Quit', True, color.BLACK), border_radius=16)

    # Tick the clock once to remove delays
    clock.tick(FPS)

    # Run the game until it is quit
    while True:

        # Wait until the FPS time has passed, and store that time
        dt = clock.tick(FPS)

        # Step the mouse
        mouse.step(dt)

        # region Events

        # Check for events
        for event in pg.event.get():

            # If the game is quit, end the game
            if event.type == pg.QUIT:
                return True, 0

            # Check for keyboard presses
            if event.type == pg.KEYDOWN:

                # End the game if the escape key is pressed
                if event.key == pg.K_ESCAPE:
                    return True, 0

            # Check if the mouse is pressed
            if event.type == pg.MOUSEBUTTONDOWN:

                # Check button presses if the left mouse button in pressed
                if event.button == pg.BUTTON_LEFT:

                    # Press the mouse
                    mouse.press()

                    # Play the game if the play button is pressed
                    if play.press(pg.mouse.get_pos()):
                        return False, audio.volume

                    # Enter the options function if the options button is pressed
                    if options.press(pg.mouse.get_pos()):
                        if run_options(mouse, audio):
                            return True, 0

                    # Enter the credits function if the credits button is pressed
                    if credits.press(pg.mouse.get_pos()):
                        if run_credits(mouse):
                            return True, 0

                    # Quit the game if the quit button is pressed
                    if quit.press(pg.mouse.get_pos()):
                        return True, 0

        # endregion Events

        # region Draw the HUD

        # Draw the background
        display.fill((84, 216, 255))

        # Draw all buttons
        if play.press(pg.mouse.get_pos()): play.draw_hover()
        else: play.draw_unhover()

        if options.press(pg.mouse.get_pos()): options.draw_hover()
        else: options.draw_unhover()

        if credits.press(pg.mouse.get_pos()): credits.draw_hover()
        else: credits.draw_unhover()

        if quit.press(pg.mouse.get_pos()): quit.draw_hover()
        else: quit.draw_unhover()

        # Draw the mouse
        mouse.draw()

        # endregion Draw the HUD

        # Update the window
        pg.display.update()
