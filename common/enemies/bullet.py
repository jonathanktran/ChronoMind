"""This file contains the bullet class, a child of the enemy class."""

import pygame as pg

import common.display
from common import enemies
from common.enemies import enemy
from common.display import display


class Bullet(enemy.Enemy):
    """This is the bullet enemy. It kills the player when it makes contact."""

    def __init__(self, x, y, x_vel, y_vel, color):
        """ Initialize the bullet enemy

        :param x: The starting x of the bullet
        :param y: The starting y of the bullet
        :param x_vel: The x velocity of the bullet
        :param y_vel: The y velocity of the bullet
        :param color: The color of the bullet
        """

        super().__init__()
        self.id = None
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.radius = 8

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Move the bullet
        self.x += dt/1000 * self.x_vel
        self.y += dt/1000 * self.y_vel

        # Check if the bullet is far off screen
        if self.x < enemies.MIN_X or self.x > enemies.MAX_X or self.y < enemies.MIN_Y or self.y > enemies.MAX_Y:
            enemies.enemy_destroy(self)

    def collide(self):
        """This runs when the enemy collides with the player"""
        enemies.enemy_destroy(self)

    def draw(self):
        """Draw the bullet to the screen"""
        pg.draw.circle(display, self.color, (self.x, self.y), self.radius)
