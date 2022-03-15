"""The timeline a dictionary of enemies or rounds, who's keys are frames.
The enemies and rounds are instantiated, but not added to their respective lists.
"""

from display import DISPLAY_WIDTH, DISPLAY_HEIGHT
import enemies
import rounds
from math import floor, cos, sin, radians, atan, log, exp, ceil
import builtins
import random
from numpy.random import randint, normal
import numpy as np
import misc


# The timeline dictionary
timeline = dict()

# region References

# region Reference Movements

# region Reference Positions

MIDDLE_TOP = (DISPLAY_WIDTH/2, 0)
MIDDLE_BOTTOM = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT)
MIDDLE_LEFT = (0, DISPLAY_HEIGHT/2)
MIDDLE_RIGHT = (DISPLAY_WIDTH, DISPLAY_HEIGHT/2)
BOTTOM_LEFT = (0, DISPLAY_HEIGHT)
BOTTOM_RIGHT = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
TOP_LEFT = (0, 0)
TOP_RIGHT = (DISPLAY_WIDTH, 0)

# endregion Reference Positions

# region Reference Speeds

# Speed Magnitudes
speed_magnitudes =    [
    DISPLAY_WIDTH/4,
    DISPLAY_WIDTH/2,
    DISPLAY_WIDTH
]

# Speed Probabilities
speed_probabilities = [
    0.25,
    0.5,
    0.25
]

# endregion Reference Speeds

# region Reference Directions

DIR_RIGHT = 0
DIR_BOTTOM_RIGHT = 45
DIR_DOWN = 90
DIR_BOTTOM_LEFT = 135
DIR_LEFT = 180
DIR_TOP_LEFT = 225
DIR_UP = 270
DIR_TOP_RIGHT = 315

# endregion Reference Directions

# endregion Reference Movements

# region Reference Rounds and Enemies

# A dictionary correlating round types with base difficulties
round_list = [
    rounds.Straight,
    rounds.Sprinkler,
    rounds.Row
]

# A dictionary correlating round types with base difficulties
enemy_list = [
    enemies.Bullet,
    enemies.WaveBullet,
    enemies.BlinkBullet
]

# endregion Reference Rounds and Enemies

# region Reference Round Spawnrate

round_spawnrate_list = [
    {'enemy_count': 8, 'dt': 500},
    {'enemy_count': 16, 'dt': 250},
    {'enemy_count': 32, 'dt': 125},
]

# endregion Reference Round Spawnrate

# region Reference Difficulties

BASE_ENEMY_DIFFICULTY = 0.5
BASE_ROUND_DIFFICULTY = 2

# endregion Reference Difficulties

# endregion References

# region Functionality


def add(time, event):
    """Add an event to the timeline at the given time.

    :param time: The time of the event in ms
    :param event: An enemy or round
    """

    # If the time is already in the timeline, append it to the list
    if time in timeline:
        timeline[time].append(event)

    # Otherwise, create a new list at the given time
    else:
        timeline[time] = [event]


def check(time, dt):
    """Start all events at the given time

    :param time: The current time in ms
    :param dt: The amount of time between the previous check
    """

    # For every frame since the previous check...
    for ms in range(floor(time-dt+1), floor(time+1)):

        # If the time has a corresponding event(s), start them
        if ms in timeline:

            # For every event at the given time...
            for event in timeline[ms]:

                # If the instance is an enemy, add the enemy to the enemies list
                if isinstance(event, enemies.Enemy):
                    enemies.enemy_create(event, time - ms)

                # If the event is a round, add the round to the round list
                else:
                    rounds.round_create(event, time - ms)

            # Remove this time from the timeline
            del timeline[ms]


def get_enemy_round_difficulty(difficulty):
    """This function returns the difficulty allocated to rounds, and the difficultly allocated to enemies.

    :param difficulty: The current difficulty
    :return difficulty: The difficulty allocated, in the form (round_difficulty, enemy_difficulty)
    """

    # Find the probability of a round and the probability of an enemy
    p_round = 1 / 1 + exp(-(difficulty-9)/4)

    # Find the difficulty assigned to rounds
    round_difficulty = misc.clamp(0, 1, normal(loc=p_round, scale=0.1))

    # Return a number of rounds and enemies to use
    return round_difficulty, 1-round_difficulty


def get_difficulty_assignment(average_value, difficulty):
    """Returns a random list of numbers of length 1 - max_count, who's numbers sum to the provided difficulty.

    :param average_value: The average difficulty
    :param difficulty: The total difficulty to assign throughout the list
    """

    # Find the average number of elements in the list, given the average element value and the sum value
    avg_count = ceil(difficulty / average_value)

    # Find the length of the list
    length = max(1, randint(avg_count-2, avg_count+2))

    # Find a normally distributed list of the found length
    normal_list = [max(0, normal(loc=average_value, scale=average_value/5)) for _ in range(length)]

    # Find the sum of the list
    random_list_sum = sum(normal_list)

    # Scale each entry so that the sum is the difficulty
    return [element * (difficulty/random_list_sum) for element in normal_list]


def get_round_specific_arguments(round_type, arguments):
    """This function return arguments specific to the given round"""

    if round_type is rounds.Straight:
        return {}

    elif round_type is rounds.Sprinkler:
        return {'lower_dir': arguments['direction']-45, 'upper_dir': arguments['direction']+45, 'dir_spd': 90}

    elif round_type is rounds.Row:

        # Check whether the row is horizontal or vertical
        if arguments['position'][0] == 0 or arguments['position'][0] == DISPLAY_WIDTH:

            # Check if the row is facing left or right
            if 90 < arguments['direction'] <= 270:

                # Find the positions, randomly choosing which is first
                positions = [(DISPLAY_WIDTH, 0), (DISPLAY_WIDTH, DISPLAY_HEIGHT)]
                random.shuffle(positions)

            else:

                # Find the positions, randomly choosing which is first
                positions = [(0, 0), (0, DISPLAY_HEIGHT)]
                random.shuffle(positions)

        else:

            # Check if the row is facing up or down
            if 180 > arguments['direction']:

                # Find the positions, randomly choosing which is first
                positions = [(0, 0), (DISPLAY_WIDTH, 0)]
                random.shuffle(positions)

            else:

                # Find the positions, randomly choosing which is first
                positions = [(0, DISPLAY_HEIGHT), (DISPLAY_WIDTH, DISPLAY_HEIGHT)]
                random.shuffle(positions)

        return {'position_1': positions[0],
                'position_2': positions[1],
                'pos_spd': random.choice((0.5, 1, 2, 4))
                }


def get_position_and_direction():
    """This function returns a position and a valid direction for enemies moving in that direction."""

    # First, select a quadrant
    quadrant = random.randint(0, 3)

    # Then, find a direction in that quadrant normal around the cardinal directions
    direction = misc.clamp((quadrant-1)*90, (quadrant+1)*90, np.random.normal(loc=(quadrant*90), scale=22.5))

    # Linearly sample the position from a 90 degrees cone in the opposite direction, from the center of the screen
    pos_dir = atan(DISPLAY_HEIGHT/DISPLAY_WIDTH) * (random.random() - 0.5)
    vx, vy = -cos(radians(direction) + pos_dir), -sin(radians(direction) + pos_dir)

    # Find which face is hit first
    top_dist = -(DISPLAY_HEIGHT/2) / vy
    bottom_dist = (DISPLAY_HEIGHT/2) / vy
    left_dist = -(DISPLAY_WIDTH/2) / vx
    right_dist = (DISPLAY_WIDTH/2) / vx

    # Set the position to be the minimum distance
    if vy < 0:
        if vx < 0: position = (top_dist * vx + DISPLAY_WIDTH/2, 0) if top_dist < left_dist else \
                              (0, left_dist * vy + DISPLAY_HEIGHT/2)
        else: position = (top_dist * vx + DISPLAY_WIDTH/2, 0) if top_dist < right_dist else \
                         (DISPLAY_WIDTH, right_dist * vy + DISPLAY_HEIGHT / 2)
    else:
        if vx < 0: position = (bottom_dist * vx + DISPLAY_WIDTH/2, DISPLAY_HEIGHT) if bottom_dist < left_dist else \
                              (0, left_dist * vy + DISPLAY_HEIGHT / 2)
        else: position = (bottom_dist * vx + DISPLAY_WIDTH/2, DISPLAY_HEIGHT) if bottom_dist < right_dist else \
                         (DISPLAY_WIDTH, right_dist * vy + DISPLAY_HEIGHT / 2)

    # Return the position and direction
    return direction, position


def add_level(time):
    """This function adds a four seconds worth of enemies to the timeline at the given time.

    :param time: The current time in ms
    """

    # First, find the difficulty from the time
    difficulty = max(4, builtins.round(3 * log(time/1000 + 1)))

    # First, find the max number of rounds that can be active at once
    round_difficulty, enemy_difficulty = get_enemy_round_difficulty(difficulty)

    # Find the number of rounds and enemies
    round_difficulties = get_difficulty_assignment(BASE_ROUND_DIFFICULTY, round_difficulty)
    enemy_difficulties = get_difficulty_assignment(BASE_ROUND_DIFFICULTY, enemy_difficulty)
    print(round_difficulties, enemy_difficulties)

    # Next, randomly generate the rounds to add
    for round in round_difficulties:

        # Select the round type
        round_type = random.choice(round_list)

        # Get the round's enemy's position and direction
        direction, position = get_position_and_direction()

        # Get the round's velocity
        velocity = misc.clamp(DISPLAY_WIDTH/4, DISPLAY_WIDTH,
                              np.random.normal(loc=DISPLAY_WIDTH/2, scale=DISPLAY_WIDTH/8))

        # Select an enemy
        enemy_type = random.choice(enemy_list)

        # Get the round's spawnrate
        round_spawnrate = random.choice(round_spawnrate_list)

        # Get the round's type-specific arguments
        round_args = get_round_specific_arguments(round_type, {'position': position, 'direction': direction,
                                                               'velocity': velocity, 'enemy_type': enemy_type,
                                                               **round_spawnrate})

        # Add the round
        add(time, round_type(position=position, direction=direction, velocity=velocity,
                             enemy=enemy_type, **round_spawnrate,  **round_args))

    # Then, randomly generate the enemies to add
    for enemy in enemy_difficulties:

        # Select the enemy type
        enemy_type = random.choice(enemy_list)

        # Get the round's enemy's position and direction
        direction, position = get_position_and_direction()

        # Get the enemy's magnitude of velocity
        velocity = misc.clamp(DISPLAY_WIDTH/4, DISPLAY_WIDTH,
                              np.random.normal(loc=DISPLAY_WIDTH/2, scale=DISPLAY_WIDTH/8))

        # Retrieve the velocity in terms of (x,y) velocities instead of (mag, dir)
        velocity = (velocity * cos(radians(direction)), velocity * sin(radians(direction)))

        # Randomly select at time to spawn the enemy in the next four seconds
        spawn_time = random.randrange(time, time+4000)

        # Add the enemy
        add(spawn_time, enemy_type(position=position, velocity=velocity))


# endregion Functionality
