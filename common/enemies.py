"""This file contains all enemy objects, and their relevant functions.
Enemies are objects which harm or kill the player during gameplay. They are spawned by Rounds.
Each enemy must be added to the enemies dictionary when created, and must be removed when destroyed.
"""

import math
import pygame as pg
import display
import color


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

    def get_velocity(self, dt):
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

    def draw(self):
        """Draw the bullet to the screen"""
        pg.draw.circle(display.display, color.RED, (self.x, self.y), self.radius)

    def copy(self):
        """Return a copy of this instance"""
        return Bullet((self.x, self.y), (self.x_vel, self.y_vel), self.color)


class BlinkBullet(Enemy):
    """This is the blink bullet enemy. It kills the player when it makes contact. It jumps between two positions
    periodically.
    """

    # region Constants

    BLINK_RATE = 500
    BLINK_DISTANCE = 64

    # endregion Constants

    def __init__(self, position, velocity, color):
        """ Initialize the bullet enemy

        :param position: The starting (x, y) position tuple of the bullet
        :param velocity: The (x, y) velocity tuple of the bullet
        :param color: The color of the bullet
        """

        super().__init__()

        # Find the normal vector to the velocity
        mag = math.sqrt(velocity[0]**2 + velocity[1]**2)
        self.norm_vec = ((-self.BLINK_DISTANCE * velocity[1]) / mag, (self.BLINK_DISTANCE * velocity[0]) / mag)

        self.id = None
        self.x = position[0] + self.norm_vec[0]
        self.y = position[1] + self.norm_vec[1]
        self.x_vel = velocity[0]
        self.y_vel = velocity[1]
        self.color = color
        self.radius = 8
        self.position_time = 0

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Increment the position time
        self.position_time += dt

        # Check if it is time to blink positions
        if self.position_time > self.BLINK_RATE:

            # Reset the opacity timer
            self.position_time = self.position_time - self.BLINK_RATE

            # Invert the normal vector
            self.norm_vec = (-self.norm_vec[0], -self.norm_vec[1])

            # Change the position
            self.x += self.norm_vec[0]
            self.y += self.norm_vec[1]

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

    def draw(self):
        """Draw the bullet to the screen"""

        pg.draw.circle(display.display, color.GREEN, (self.x, self.y), self.radius)

    def copy(self):
        """Return a copy of this instance"""
        return BlinkBullet((self.x, self.y), (self.x_vel, self.y_vel), self.color)


class WaveBullet(Enemy):
    """This is the blink bullet enemy. It kills the player when it makes contact. It jumps between two positions
        periodically.
        """

    # region Constants

    WAVE_RATE = 1/750
    WAVE_SIZE = 96

    # endregion Constants

    def __init__(self, position, velocity, color):
        """ Initialize the bullet enemy

        :param position: The starting (x, y) position tuple of the bullet
        :param velocity: The (x, y) velocity tuple of the bullet
        :param color: The color of the bullet
        """

        super().__init__()

        # Find the normal vector to the velocity
        mag = math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
        self.norm_vec = ((-self.WAVE_SIZE * velocity[1]) / mag, (self.WAVE_SIZE * velocity[0]) / mag)

        self.id = None
        self.x = position[0]
        self.y = position[1]
        self.real_x = self.x
        self.real_y = self.y
        self.x_vel = velocity[0]
        self.y_vel = velocity[1]
        self.color = color
        self.radius = 8
        self.position_time = 0

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Increment the position time
        self.position_time += dt

        # Find the current magnitude of the wave
        wave_mag = math.sin(self.position_time * (self.WAVE_RATE * (2 * math.pi)))
        x_offset = wave_mag * self.norm_vec[0]
        y_offset = wave_mag * self.norm_vec[1]

        # Store the position without the offset
        self.real_x += dt / 1000 * self.x_vel
        self.real_y += dt / 1000 * self.y_vel

        # Move the bullet
        self.x = self.real_x + x_offset
        self.y = self.real_y + y_offset

        # Check if the bullet is far off screen
        if self.real_x < MIN_X or self.real_x > MAX_X or self.real_y < MIN_Y or self.real_y > MAX_Y:
            enemy_destroy(self)

    def get_velocity(self, dt):
        """Returns the velocity (vel_x, vel_y) tuple of the enemy."""
        return self.x_vel * dt / 1000, math.cos(self.position_time * (self.WAVE_RATE * (2 * math.pi))) * dt / 1000

    def collide(self):
        """This runs when the enemy collides with the player"""
        enemy_destroy(self)

    def draw(self):
        """Draw the bullet to the screen"""

        pg.draw.circle(display.display, color.BLUE, (self.x, self.y), self.radius)

    def copy(self):
        """Return a copy of this instance"""
        return WaveBullet((self.x, self.y), (self.x_vel, self.y_vel), self.color)

# endregion Enemy Classes
