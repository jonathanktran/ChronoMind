"""This file contains all enemy objects, and their relevant functions.
Enemies are objects which harm or kill the player during gameplay. They are spawned by Rounds.
Each enemy must be added to the enemies dictionary when created, and must be removed when destroyed."""
from display import *
import pygame as pg
import display
IMAGE = pg.image.load('../assets/sprites/asteroid_1.png').convert_alpha()
IMAGE = pg.transform.scale(IMAGE, (50, 50))


# region Enemy List

# A dictionary of all enemies, mapping their ID to their instance pointer
enemy_list = dict()
enemy_id = 0

# region Constants

# The boundary values a bullet dies at when outside
MIN_X = -display.DISPLAY_WIDTH
MAX_X = display.DISPLAY_WIDTH*2
MIN_Y = -display.DISPLAY_HEIGHT
MAX_Y = display.DISPLAY_HEIGHT*2

# endregion Constants

# region Functionality


def enemy_create(enemy, delay):
    """Assign an enemy an ID, and add it to the enemies dictionary

    :param enemy: An instantiated enemy
    :param delay: The amount of ms since the enemy should have been created
    """

    global enemy_id, enemy_list

    # Add the enemy to the enemy list
    enemy_list[enemy_id] = enemy
    enemy.id = enemy_id
    enemy_id = enemy_id + 1

    # Step the enemy forward to account for the delay
    enemy.step(delay)


def enemy_destroy(enemy):
    """Remove an enemy from the enemies dictionary

    :param enemy: An enemy which is already in the dictionary
    """

    global enemy_list
    enemy_list.pop(enemy.id)

# endregion Functionality

# endregion Enemy List

# region Enemy Classes


class Enemy:
    """This is the abstract parent class for all enemies."""

    def __init__(self):
        pass

    def step(self, dt):
        """The runs every step

        :param dt: The amount of time since the previous frame
        """
        pass

    def get_velocity(self):
        """Returns the velocity (vel_x, vel_y) tuple of the enemy."""
        pass

    def collide(self):
        """This runs when this enemy collides with the player"""
        pass

    def draw(self):
        """Draw this enemy to the screen"""
        pass

    def copy(self):
        """Return a copy of this instance"""
        pass


class Bullet(Enemy):
    """This is the bullet enemy. It kills the player when it makes contact."""

    def __init__(self, position, velocity, color):
        """ Initialize the bullet enemy

        :param position: The starting (x, y) position tuple of the bullet
        :param velocity: The (x, y) velocity tuple of the bullet
        :param color: The color of the bullet
        """

        super().__init__()
        self.id = None
        self.x = position[0]
        self.y = position[1]
        self.x_vel = velocity[0]
        self.y_vel = velocity[1]
        self.color = color
        self.radius = 8
        self.image = IMAGE
        self.rect = self.image.get_rect()

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Move the bullet
        self.x += dt/1000 * self.x_vel
        self.y += dt/1000 * self.y_vel

        # Check if the bullet is far off screen
        if self.x < MIN_X or self.x > MAX_X or self.y < MIN_Y or self.y > MAX_Y:
            enemy_destroy(self)

    def get_velocity(self, dt):
        """Returns the velocity (vel_x, vel_y) tuple of the enemy."""
        return self.x_vel * dt/1000, self.y_vel * dt/1000

    def collide(self):
        """This runs when the enemy collides with the player"""
        enemy_destroy(self)

    def copy(self):
        """Return a copy of this instance"""
        return Bullet((self.x, self.y), (self.x_vel, self.y_vel), self.color)

# endregion Enemy Classes
