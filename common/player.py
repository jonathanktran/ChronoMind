"""This file defines the player object"""

import pygame as pg
from display import display
from misc import lines_within_range
import color


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
        self.lives = 10
        self.invincible_timer = 0

    def step(self, dt, enemies):
        """This runs every frame.

        :param dt: The amount of time since the previous frame
        :param enemies: A list of enemies to check for collisions
        """

        # Find the distance of the player to the mouse
        x_diff = pg.mouse.get_pos()[0] - self.x
        y_diff = pg.mouse.get_pos()[1] - self.y

        # Decrement the invincibility timer
        self.invincible_timer = max(self.invincible_timer - dt, 0)

        # Do not check collisions if the player is invincible
        if self.invincible_timer == 0:

            # Check for enemy collisions
            for enemy in enemies:

                # Find whether the enemy collides with the player
                collision = lines_within_range((x_diff, y_diff), (self.x, self.y),
                                                  enemy.get_velocity(dt), (enemy.x, enemy.y),
                                                  self.radius + enemy.radius)

                # If the player collides with the enemy
                if collision:

                    # Run the enemy's collision event
                    enemy.collide()

                    # Lose a life
                    self.lives = self.lives - 1

                    # Become invincible
                    self.invincible_timer = 2000

        # Set the player to the mouse position
        self.x, self.y = pg.mouse.get_pos()

    def draw(self):
        """Draw the player to the screen"""

        # Draw the body
        if self.invincible_timer == 0: pg.draw.circle(display, color.RED, (self.x, self.y), self.radius)
        else: pg.draw.circle(display, (255,
                                       255 * (self.invincible_timer/2000),
                                       255 * (self.invincible_timer/2000)), (self.x, self.y), self.radius)
        # Draw the outline
        pg.draw.circle(display, color.BLACK, (self.x, self.y), self.radius, 1)
