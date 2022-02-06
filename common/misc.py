"""This file contains miscellaneous functions"""

import math


def point_distance(point_1, point_2):
    """ Return the distance between two given points

    :param point_1: The first point
    :param point_2: The second knife
    :return: The distance between the two given points
    """

    return math.sqrt((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)


def min_distance_on_vector_to_point(vector_x, vector_y, vector_base_x, vector_base_y, point_x, point_y,
                                    mag_max=float("inf")):
    """Returns the smallest distance between a line and a given point, where the line has a bounded absolute
    magnitude.

    :param vector_x: The x component of the vector
    :param vector_y: The y component of the vector
    :param vector_base_x: The starting x position of the vector
    :param vector_base_y: The starting y position of the vector
    :param point_x: The x position of the point
    :param point_y: The y position of the point
    :param mag_max: The maximum absolute magnitude that the vector can have
    :return: The smallest absolute magnitude between a line and a point, or None if the given vector is a 0 vector
    """

    # Return None if the vector is 0
    if vector_x == 0 and vector_y == 0:
        return None

    # Find the t-value which minimizes the distance
    t = -((vector_y * (vector_base_y - point_y)) + (vector_x * (vector_base_x - point_x))) / (
        vector_y**2 + vector_x**2)

    # Find the magnitude of the vector which minimizes the distance
    mag_min_distance = math.sqrt((vector_x * t)**2 + (vector_y * t)**2)

    # Find the t value which produces the maximum allowed magnitude
    max_t = math.sqrt(mag_max**2 / (vector_x**2 + vector_y**2))

    # Pick the allowed t value is closest to the minimum value
    if mag_min_distance > mag_max:
        t = max_t
    elif mag_min_distance < -mag_max:
        t = -max_t

    # Return the distance between the tip of the vector and the point
    return point_distance((vector_x * t + vector_base_x, vector_y * t + vector_base_y), (point_x, point_y))
