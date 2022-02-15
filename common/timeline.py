"""The timeline a dictionary of enemies or rounds, who's keys are frames.
The enemies and rounds are instantiated, but not added to their respective lists."""

from display import DISPLAY_WIDTH, DISPLAY_HEIGHT
import enemies
import rounds
from math import floor


# The timeline dictionary
timeline = dict()

# region Reference Positions

MIDDLE_TOP = (DISPLAY_WIDTH/2, 0)
MIDDLE_BOTTOM = (DISPLAY_WIDTH/2, DISPLAY_HEIGHT)
MIDDLE_LEFT = (0, DISPLAY_HEIGHT/2)
MIDDLE_RIGHT = (DISPLAY_WIDTH, DISPLAY_HEIGHT/2)

# endregion Reference Positions

# region Reference Speeds

# Speed Magnitudes
FAST_HORIZONTAL = DISPLAY_WIDTH
FAST_VERTICAL = DISPLAY_HEIGHT

# Speed Vectors
FAST_RIGHT = (DISPLAY_WIDTH, 0)
FAST_LEFT = (-DISPLAY_WIDTH, 0)
FAST_UP = (0, -DISPLAY_HEIGHT)
FAST_DOWN = (0, DISPLAY_HEIGHT)
SLOW_RIGHT = (DISPLAY_WIDTH/2, 0)
SLOW_LEFT = (-DISPLAY_WIDTH/2, 0)
SLOW_UP = (0, -DISPLAY_HEIGHT/2)
SLOW_DOWN = (0, DISPLAY_HEIGHT/2)

# endregion Reference Speeds

# region Reference Colors

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# endregion Reference Colors

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


# endregion Functionality

# region Timeline Creation

add(0, enemies.Bullet(MIDDLE_LEFT, SLOW_RIGHT, GREEN))
add(2000, enemies.Bullet(MIDDLE_RIGHT, SLOW_LEFT, GREEN))
add(4000, enemies.Bullet(MIDDLE_TOP, SLOW_DOWN, GREEN))
add(6000, enemies.Bullet(MIDDLE_BOTTOM, SLOW_UP, GREEN))
add(8000, rounds.Sprinkler(enemies.Bullet, MIDDLE_LEFT, FAST_HORIZONTAL, DIR_RIGHT, -45, 45, 90, BLUE, 8, 2000/8))
add(10000, rounds.Sprinkler(enemies.Bullet, MIDDLE_RIGHT, FAST_HORIZONTAL, DIR_LEFT, DIR_BOTTOM_LEFT, DIR_TOP_LEFT, 90, BLUE, 8, 2000/8))
add(12000, rounds.Sprinkler(enemies.Bullet, MIDDLE_TOP, FAST_VERTICAL, DIR_DOWN, DIR_BOTTOM_RIGHT, DIR_BOTTOM_LEFT, 90, BLUE, 8, 2000/8))
add(14000, rounds.Sprinkler(enemies.Bullet, MIDDLE_BOTTOM, FAST_VERTICAL, DIR_UP, DIR_TOP_LEFT, DIR_TOP_RIGHT, 90, BLUE, 8, 2000/8))

# endregion Timeline Creation
