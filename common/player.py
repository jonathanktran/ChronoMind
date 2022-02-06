"""This file defines the player object"""

import math
import pygame as pg
from display import display
from misc import point_distance, min_distance_on_vector_to_point


class Player:
    """The player object is controlled by the player."""

    def __init__(self, x, y):
        """ Initialize the player

        :param x: The starting x position of the player
        :param y: The starting y position of the player
        """

        # Initialize the player attributes
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.radius = 16
        self.lives = 3

    def step(self, dt, enemies):
        """This runs every frame.

        :param dt: The amount of time since the previous frame
        :param enemies: A list of enemies to check for collisions
        """

        # Find the distance of the player to the mouse
        x_diff = pg.mouse.get_pos()[0] - self.x
        y_diff = pg.mouse.get_pos()[1] - self.y
        mouse_dist = math.sqrt(x_diff ** 2 + y_diff ** 2)

        # Check for enemy collisions
        for enemy in enemies:

            # Find the smallest magnitude along the vector to the mouse
            min_distance = min_distance_on_vector_to_point(x_diff, y_diff, self.x, self.y, enemy.x, enemy.y,
                                                           mag_max=mouse_dist)

            # If the player is not moving
            if min_distance is None:
                if point_distance((enemy.x, enemy.y), (self.x, self.y)) < self.radius + enemy.radius:
                    enemy.collide()
                    self.lives = self.lives - 1

            # If the player is moving
            elif min_distance < (self.radius + enemy.radius):
                enemy.collide()
                self.lives = self.lives - 1

        # Set the player to the mouse position
        self.x, self.y = pg.mouse.get_pos()

    def draw(self):
        """Draw the player to the screen"""
        pg.draw.circle(display, (255, 0, 0), (self.x, self.y), self.radius)
