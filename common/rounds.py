"""This file contains all round objects, and their relevant functions.
Rounds are objects which spawn enemies. Rounds die once they have spawned all their enemies.
Each round must be added to the rounds dictionary when created, and must be removed when destroyed."""

import enemies
import math


# region Round List

# A dictionary of all rounds, mapping their ID to their instance pointer
round_list = dict()
round_id = 0


# region Functionality

def round_create(round, delay):
    """Assign a round an ID, and add it to the rounds dictionary

    :param round: An instantiated round
    :param delay: The amount of time since the round should have been created
    """

    global round_id
    round_list[round_id] = round
    round.id = round_id
    round_id = round_id + 1


def round_destroy(round):
    """Remove an round from the rounds dictionary

    :param round: A round which is already in the dictionary
    """

    round_list.pop(round.id)

# endregion Functionality

# endregion Round List

# region Round Classes


class Round:
    """This is the abstract parent class for all rounds."""

    def __init__(self):
        """The runs every step"""
        pass

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """
        pass

    def create_enemy(self, delay):
        """Spawn an enemy

        :param delay: The amount of time this enemy is being created past the expected time
        """
        pass


class Sprinkler(Round):
    """This is the Sprinkler Round. It spawns enemies from its starting position, sending them outwards at a given
    velocity. The direction of these bullets changes at a given rate, and oscillates back and forth between the minimum
    and maximum angles."""

    def __init__(self, enemy, position, vel, dir, lower_dir, upper_dir, dir_spd, color, enemy_count, dt):
        """ Initialize the Sprinkler round.

        :param enemy: The enemy class to spawn
        :param position: The starting position of each enemy
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
        self.x = position[0]
        self.y = position[1]
        self.vel = vel
        self.dir = math.radians(dir)
        self.lower_dir = math.radians(lower_dir)
        self.upper_dir = math.radians(upper_dir)
        self.dir_spd = math.radians(dir_spd)
        self.color = color
        self.enemy_count = enemy_count
        self.dt = dt
        self.time = dt

    def create_enemy(self, delay):
        """Spawn an enemy

        :param delay: The amount of time this enemy is being created past the expected time
        """

        # Find the speed
        vel_x = math.cos(self.dir) * self.vel
        vel_y = math.sin(self.dir) * self.vel

        # Spawn the enemy
        enemies.enemy_create(self.enemy((self.x, self.y), (vel_x, vel_y), self.color), delay)
        self.enemy_count = self.enemy_count - 1

        # Check if the round is finished
        if self.enemy_count == 0:
            round_destroy(self)

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
            self.create_enemy(self.time - self.dt)

            # Reset the timer
            self.time -= self.dt


class Straight(Round):
    """This is the Straight Round. It spawns enemies from its starting position, sending them outwards at a given
     velocity. These enemies travel in a straight line."""

    def __init__(self, enemy, position, velocity, color, enemy_count, dt):
        """Initialize the Straight Round

        :param enemy: The enemy class to spawn
        :param position: The starting position of each enemy
        :param velocity: The velocity of each enemy
        :param color: The color of the spawned enemies
        :param enemy_count: The number of enemies to spawn before destroying this spawner
        :param dt: The number of ms between each enemy spawn
        """

        super().__init__()
        self.enemy = enemy
        self.x = position[0]
        self.y = position[1]
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]
        self.color = color
        self.enemy_count = enemy_count
        self.dt = dt
        self.time = dt

    def create_enemy(self, delay):
        """Spawn an enemy

        :param delay: The amount of time this enemy is being created past the expected time
        """

        # Spawn the enemy
        enemies.enemy_create(self.enemy((self.x, self.y), (self.vel_x, self.vel_y), self.color), delay)
        self.enemy_count = self.enemy_count - 1

        # Check if the round is finished
        if self.enemy_count == 0:
            round_destroy(self)

    def step(self, dt):
        """This runs every frame

        :param dt: The amount of time since the previous frame
        """

        # Increment the time
        self.time = self.time + dt

        # If it is time for an enemy to spawn...
        if self.time >= self.dt:

            # Create an enemy
            self.create_enemy(self.time - self.dt)

            # Reset the timer
            self.time -= self.dt


# endregion Round Classes
