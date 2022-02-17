"""This file contains methods for using the attention level of the player."""

from misc import clamp, linear_map_range
import time_control


# region Constants

MAX_ATTENTION = 60
MIN_ATTENTION = 30

# endregion Constants

# region Functionality


def get_time_mult(attention):
    """Return the time multiplier associated with the current attention level. This level is a linear relationship
    between the baseline and maximum attention, and a min and maximum time multiplier.

    :param attention: The current level of attention
    :return time multiplier: The time mulitplier associated with the given level of attention.
    """

    return linear_map_range(MIN_ATTENTION, MAX_ATTENTION, time_control.MAX_TIME_MULT, time_control.MIN_TIME_MULT,
                            clamp(MIN_ATTENTION, MAX_ATTENTION, attention))

# endregion Functionality
