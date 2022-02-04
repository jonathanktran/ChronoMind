"""This is a bullet enemy. It kills the player when it makes contact"""

import pygame as pg
from common import enemies
from common.enemies import enemy
from common.display import display


class Bullet(enemy.Enemy):

    def __init__(self, x, y, x_vel, y_vel, color):
        super().__init__()
        self.id = None
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.radius = 8

    def step(self, dt):
        """The code runs every loop"""

        # Move the bullet
        self.x += dt * self.x_vel
        self.y += dt * self.y_vel

    def collide(self):
        """This code runs when the enemy collides with the player"""
        enemies.enemy_destroy(self)

    def draw(self):
        """Draw the bulllet to the screen"""

        pg.draw.circle(display, self.color, (self.x, self.y), self.radius)
