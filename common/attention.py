"""This file contains methods for using the attention level of the player."""

# region Constants

MAX_ATTENTION = 100
MIN_TIME_MULT = 0.6

# endregion Constants

# region Functionality


def get_time_mult(attention, calibration_setting):
    """Return the time multiplier associated with the current attention level. This is dependant upon the calibration
    settings. Attention levels below the calibrated minimum have a time multiplier of 1. Attention levels above the
    calibration threshold are linearly determined, with a minimum time multiplier achieved at an attention of 100.

    :param attention: The current level of attention
    :param calibration_setting: The attention values used to set the minimum attention bound
    :return time multiplier: The time multiplier associated with the given level of attention.
    """

    return 1 if attention < calibration_setting \
        else (MIN_TIME_MULT if attention >= MAX_ATTENTION
        else (attention - calibration_setting) * ((MIN_TIME_MULT - 1) / (MAX_ATTENTION - calibration_setting)) + 1)


def get_calibration_settings(dataframe):
    """This function returns the lower limit of attention, past which time is slowed.

    :param dataframe: The dataframe containing the data from the calibration phase.
    :return int: A low bound on attention
    """

    # Find the number of attention values to sample from, ignoring those times when the person wasn't paying attention.
    attention_count = round(dataframe.shape[0]/2)

    # Find the the top 50% of attention values
    attention_values = dataframe['attention'].nlargest(attention_count)

    # Return the 1/4 quartile for those values
    return attention_values.quantile(0.1)


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
