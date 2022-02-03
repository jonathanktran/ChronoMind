"""This file defines the player object"""

import pygame as pg
from display import display


class Player:

    def __init__(self, x, y):

        # Initialize the player attributes
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.radius = 16

    def step(self, dt):
        """The code runs every loop"""
        self.x, self.y = pg.mouse.get_pos()

    def draw(self):
        """Draw the player to the screen"""
        pg.draw.circle(display, (255, 0, 0), (self.x, self.y), self.radius)