"""This file contains methods for using the attention level of the player."""

import time_control
import math
from misc import clamp


# region Constants

MAX_ATTENTION = 100
MIN_ATTENTION = 20
ATTENTION_RANGE = MAX_ATTENTION - MIN_ATTENTION

# endregion Constants

# region Functionality


def get_time_mult(attention):
    """Return the time multiplier associated with the current attention level. This level is a linear relationship
    between the baseline and maximum attention, and a min and maximum time multiplier.

    :param attention: The current level of attention
    :return time multiplier: The time multiplier associated with the given level of attention.
    """

    # Clamp the attention
    attention = clamp(MIN_ATTENTION+10, MAX_ATTENTION-10, attention)

    return time_control.TIME_MULT_RANGE/3.1 * math.log((1 / ((attention - MIN_ATTENTION) / ATTENTION_RANGE)) - 1) + \
           (time_control.TIME_MULT_RANGE/2) + time_control.MIN_TIME_MULT


def get_interpolated_attention(attention_1, attention_2, time_1, current_time):
    """This function returns a linear interpolation of the attention measure, so that the attention measure is at the
    most recently read value by the time the next attention measure is read.

    :param attention_1: The most recent attention measure
    :param attention_2: The second most recent attention measure
    :param time_1: The time that attention_1 was measured at
    :param current_time: The current time
    :returns attention: An estimated attention extrapolated from the previous two attention measures.
    """

    # Find the slope between the two attention measures
    slope = (attention_1 - attention_2) / 1000

    # Return the estimated attention
    return (current_time - time_1) * slope + attention_2

# endregion Functionality
