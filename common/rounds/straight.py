"""This is a round which shoots enemies in a straight line."""

from common import rounds
from common.rounds import round
from common.enemies import *


class Straight(round.Round):
    """This is the Straight Round. It spawns enemies from its starting position, sending them outwards at a given
     velocity. These enemies travel in a straight line."""

    def __init__(self, enemy, x, y, vel_x, vel_y, color, enemy_count, dt):
        """ Initialize the Straight Round

        :param enemy: The enemy class to spawn
        :param x: The starting x position of the enemies
        :param y: The starting x position of the enemies
        :param vel_x: The x velocity granted to spawned enemies
        :param vel_y: The y velocity granted to spawned enemies
        :param color: The color of the spawned enemies
        :param enemy_count: The number of enemies to spawn before destroying this spawner
        :param dt: The number of ms between each enemy spawn
        """
        super().__init__()
        self.enemy = enemy
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.enemy_count = enemy_count
        self.dt = dt
        self.time = 0

        # Create the first enemy
        self.create_enemy()

    def create_enemy(self):
        """Spawn an enemy"""

        # Spawn the enemy
        enemy_create(self.enemy(self.x, self.y, self.vel_x, self.vel_y, self.color))
        self.enemy_count = self.enemy_count - 1

        # Check if the round is finished
        if self.enemy_count == 0:
            rounds.round_destroy(self)

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Increment the time
        self.time = self.time + dt

        # If it is time for an enemy to spawn...
        if self.time >= self.dt:

            # Create an enemy
            self.create_enemy()

            # Reset the timer
            self.time -= self.dt

