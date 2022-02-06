"""This is a round which spawns enemies in a back-and-forth, sprinkler-like pattern."""
import builtins

from common import rounds
from common.rounds import round
from common.enemies import *
import math
import pygame as pg


class Sprinkler(round.Round):
    """This is the Sprinkler Round. It spawns enemies from its starting position, sending them outwards at a given
    velocity. The direction of these bullets changes at a given rate, and oscillates back and forth between the minimum
    and maximum angles."""

    def __init__(self, enemy, x, y, vel, dir, lower_dir, upper_dir, dir_spd, color, enemy_count, dt):
        """ Initialize the Sprinkler round.

        :param enemy: The enemy class to spawn
        :param x: The starting x position of the enemies
        :param y: The starting y position of the enemies
        :param vel: The magnitude of velocity granted to spawned enemies
        :param dir: The starting direction of the first enemy in degrees
        :param lower_dir: The lowest direction an enemy can go in, in degrees
        :param upper_dir: The highest direction an enemy can go in, in degrees
        :param dir_spd: The number of degrees that the sprinkler will change each second
        :param color: The color of the spawned enemies
        :param enemy_count: The number of enemies to spawn before destroying this spawner
        :param dt: The number of ms between each enemy spawn
        """
        super().__init__()
        self.enemy = enemy
        self.x = x
        self.y = y
        self.vel = vel
        self.dir = math.radians(dir)
        self.lower_dir = math.radians(lower_dir)
        self.upper_dir = math.radians(upper_dir)
        self.dir_spd = math.radians(dir_spd)
        self.color = color
        self.enemy_count = enemy_count
        self.dt = dt
        self.time = dt

    def create_enemy(self, dt):
        """Spawn an enemy

        :param dt: The amount of time between the last enemy
        """

        # Find the speed
        vel_x = math.cos(self.dir) * self.vel
        vel_y = math.sin(self.dir) * self.vel

        # Spawn the enemy
        enemy_create(self.enemy(self.x, self.y, vel_x, vel_y, self.color))
        self.enemy_count = self.enemy_count - 1

        # Check if the round is finished
        if self.enemy_count == 0:
            rounds.round_destroy(self)

        # Increment the direction
        if self.dir_spd < 0:
            if self.dir < self.lower_dir:
                self.dir_spd *= -1
                self.dir -= self.lower_dir - self.dir
        else:
            if self.dir > self.upper_dir:
                self.dir_spd *= -1
                self.dir -= self.dir - self.upper_dir

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Increment the time
        self.time = self.time + dt

        # Increment the direction
        self.dir += self.dir_spd * dt / 1000

        # If it is time for an enemy to spawn...
        if self.time > self.dt:

            # Create an enemy
            self.create_enemy(dt)

            # Reset the timer
            self.time -= self.dt

