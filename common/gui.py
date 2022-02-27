"""This file contains GUI objects used in the game."""

import pygame as pg
import typing
from display import display


class Button:
    """This class is a GUI element which players can click on to return True.
    Buttons can optionally display text.
    """

    def __init__(self, position: typing.Tuple[int, int], hitbox: typing.Tuple[int, int],
                 color: typing.Tuple[int, int, int], text=None):
        """Initialize the button.

        :param position: A tuple of integers representing the center x and y of the button
        :param hitbox: A tuple of integers, representing the width and height of the button hitbox
        :param text: The text object displayed at the center of the button
        """

        self.position = position
        self.color = color
        self.size = hitbox

        # region Hitbox

        # Find the lower half of each dimension of the hitboxes
        lower_x = round(hitbox[0] / 2)
        lower_y = round(hitbox[1] / 2)

        # Set the hitbox regions
        self.hitbox_lower_x = self.position[0] - lower_x
        self.hitbox_upper_x = self.position[0] + (hitbox[0] - lower_x)
        self.hitbox_lower_y = self.position[1] - lower_y
        self.hitbox_upper_y = self.position[1] + (hitbox[1] - lower_y)

        # endregion Hitbox

        # region Text

        self.text = text

        if text is not None:
            self.text_pos = (self.position[0] - self.text.get_width()/2,
                              self.position[1] - self.text.get_height()/2)

        # endregion Text

    def press(self, position: typing.Tuple[int, int]):
        """Attempt to press the button at the given position.

        :param position: A tuple of two ints, representing the position the button is being pressed at
        """

        # If the position is within the hixbox, press the button
        if self.hitbox_lower_x <= position[0] <= self.hitbox_upper_x and \
           self.hitbox_lower_y <= position[1] <= self.hitbox_upper_y:
            return True

    def draw(self):
        """Draw the button to the screen"""

        # Draw the square
        pg.draw.rect(display, self.color,
                     pg.Rect(self.hitbox_lower_x, self.hitbox_lower_y, self.size[0], self.size[1]))

        # Draw the text
        if self.text is not None: display.blit(self.text, self.text_pos)
