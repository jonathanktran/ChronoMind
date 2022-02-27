"""This file contains methods for using the attention level of the player."""

from misc import clamp, linear_map_range
import time_control


# region Constants

MAX_ATTENTION = 100
MIN_ATTENTION = 20

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

    # Return the estimated attentionA
    return (current_time - time_1) * slope + attention_2

# endregion Functionality
