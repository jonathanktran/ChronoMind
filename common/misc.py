"""This file contains miscellaneous functions"""

import math


def clamp(min_value, max_value, value):
    """ Returns a number who's minimum and maximum are bounded

    :param min_value: The minimum returned value
    :param max_value: The maximum returned value
    :param value: The value to clamp
    :return: A value clamped between two other values
    """

    return max(min(max_value, value), min_value)


def determinate(a, b):
    """Return the determinate for two vectors"""
    return a[0] * b[1] - a[1] * b[0]


def point_distance(point_1, point_2):
    """Return the distance between two given points

    :param point_1: The first point
    :param point_2: The second knife
    :return: The distance between the two given points
    """

    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def lines_point_meeting(vector_1, pos_1, vector_2, pos_2):
    """Return true if vectors pass within a given radius of one another, and false if not.

    :param vector_1: The vector component of the first line
    :param pos_1: The starting position of the first line
    :param vector_2: The vector component of the second line
    :param pos_2: The starting position of the second line
    :return: Returns the (x, y) position where the two lines intersect, or None if they do not.
    """

    # Find the determinate of the velocities
    div = determinate(vector_1, vector_2)

    # If the determinate is 0, the lines are parallel
    if div == 0:
        return None

    # Find the determinants of both lines
    d = (determinate((pos_1[0], pos_1[1]), (vector_1[0] + pos_1[0], vector_1[1] + pos_1[1])),
         determinate((pos_2[0], pos_2[1]), (vector_2[0] + pos_2[0], vector_2[1] + pos_2[1])))

    # Find the coordinates of the meeting place
    x = determinate(d, vector_1) / div
    y = determinate(d, vector_2) / div

    # Return the meeting position
    return x, y


def lines_within_range(vector_1, pos_1, vector_2, pos_2, radius):
    """Return true if vectors pass within a given radius of one another, and false if not.

    :param vector_1: The vector component of the first line
    :param pos_1: The starting position of the first line
    :param vector_2: The vector component of the second line
    :param pos_2: The starting position of the second line
    :param radius: The minimum radius which the lines must come equal to or closer than
    :return: True if the lines pass within a given radius, and false if not
    """

    # Find the differences in the lines
    v_diff = (vector_1[0] - vector_2[0], vector_1[1] - vector_2[1])
    p_diff = (pos_1[0] - pos_2[0], pos_1[1] - pos_2[1])

    # If the lines do not change distance over time
    if v_diff == (0, 0):
        return point_distance(pos_1, pos_2) <= radius

    # For each vector, we then need to find if they cross this point.
    # To do this, we clamp the meeting point magnitude between their starting point, end point.

    # Find the t value for the vectors where they meet
    t = -(p_diff[0] * v_diff[0] + p_diff[1] * v_diff[1]) / (v_diff[0]**2 + v_diff[1]**2)

    # Clamp t between the start and end of the frame
    t = clamp(0, 1, t)

    # Return whether the distance at t is less than the radius
    return point_distance((t * vector_1[0] + pos_1[0], t * vector_1[1] + pos_1[1]),
                          (t * vector_2[0] + pos_2[0], t * vector_2[1] + pos_2[1])) < radius


def linear_map_range(from_low, from_high, to_low, to_high, x):
    """Map a current linear space onto a new linear space
    :param from_low: The low value of x
    :param from_high: The high value of x
    :param to_low: The value of y when given the low value of x
    :param to_high: The value of y when given the high value of x
    :param x: The input value in the 'from' bounds
    """

    return ((to_high - to_low) / (from_high - from_low)) * (x - from_low) + to_low

