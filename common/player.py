"""This file defines the player object"""

import pygame as pg
from display import display
from misc import point_distance


class Player:

    def __init__(self, x, y):

        # Initialize the player attributes
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.radius = 16
        self.lives = 3

    def step(self, dt, enemies):
        """The code runs every loop"""

        # Set the player to the mouse position
        self.x, self.y = pg.mouse.get_pos()

        # Check for enemy collisions
        for enemy in enemies:
            if abs(point_distance((self.x, self.y), (enemy.x, enemy.y))) < (self.radius + enemy.radius):
                enemy.collide()
                self.lives = self.lives - 1

    def draw(self):
        """Draw the player to the screen"""
        pg.draw.circle(display, (255, 0, 0), (self.x, self.y), self.radius)
