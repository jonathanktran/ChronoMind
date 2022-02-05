"""This is a round which shoots"""

from common import rounds
from common.rounds import round
from common.enemies import *


class Straight(round.Round):

    def __init__(self, enemy, x, y, vel_x, vel_y, color, enemy_count, dt):
        super().__init__()
        self.enemy = enemy
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.enemy_count = enemy_count
        self.dt = dt
        self.time = dt

    def create_enemy(self):
        """Spawn an enemy"""

        # Spawn the enemy
        enemy_create(self.enemy(self.x, self.y, self.vel_x, self.vel_y, self.color))
        self.enemy_count = self.enemy_count - 1

        # Check if the round is finished
        if self.enemy_count == 0:
            rounds.round_destroy(self)

    def step(self, dt):
        """This runs every step"""

        # Increment the time
        self.time = self.time + dt

        # If it is time for an enemy to spawn...
        if self.time > self.dt:

            # Create an enemy
            self.create_enemy()

            # Reset the timer
            self.time -= self.dt

