"""This is a round which shoots"""

from common import rounds
from common.rounds import round
from common.enemies import *
import math


class Sprinkler(round.Round):

    def __init__(self, enemy, x, y, vel, dir, lower_dir, upper_dir, dir_spd, color, enemy_count, dt):
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
        self.time = 0

    def create_enemy(self, dt):
        """Spawn an enemy"""

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
        self.dir += self.dir_spd * dt / 100
        if self.dir_spd < 0:
            if self.dir < self.lower_dir:
                self.dir_spd *= -1
                self.dir -= self.lower_dir - self.dir
        else:
            if self.dir > self.upper_dir:
                self.dir_spd *= -1
                self.dir -= self.dir - self.upper_dir

    def step(self, dt):
        """This runs every step"""

        # Increment the time
        self.time = self.time + dt

        # If it is time for an enemy to spawn...
        if self.time > self.dt:

            # Create an enemy
            self.create_enemy(dt)

            # Reset the timer
            self.time -= self.dt

