"""This file defines the player object"""

import pygame as pg
from display import display
from misc import lines_within_range
import color
from math import cos, pi


class Player:
    """The player object is controlled by the player."""

    def __init__(self, x, y):
        """ Initialize the player

        :param x: The starting x position of the player
        :param y: The starting y position of the player
        """

        # The starting number of lives
        self.MAX_LIVES = 10
        self.INV_TIME = 2000

        # Initialize the player attributes
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.radius = 20
        self.lives = self.MAX_LIVES
        self.invincible_timer = 0
        self.image = pg.image.load('../assets/sprites/player.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (85, 56))
        self.rect = self.image.get_rect()

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
                    self.invincible_timer = self.INV_TIME

        # Set the player to the mouse position
        self.x, self.y = pg.mouse.get_pos()

    def draw(self, display):
        """Draw the player to the screen"""

        # Draw the player normally
        if self.invincible_timer == 0: display.blit(self.image, (self.x, self.y))
        else:

            # Copy the player image
            inv_image = self.image.copy()

            # Find the current alpha value
            alpha = (-cos((self.INV_TIME - self.invincible_timer) * (2 * pi / (2000 / 3.5))) / 2 + 0.5) * 255

            # Make the image transparent
            inv_image.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
            display.blit(inv_image, (self.x, self.y))
