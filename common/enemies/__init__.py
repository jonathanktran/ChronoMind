"""This folder contains all enemy objects, and their relevant functions.
Enemies are objects which harm or kill the player during gameplay. They are spawned by Rounds.
Each enemy must be added to the enemies dictionary when created, and must be removed when destroyed."""

from common import display


# A dictionary of all enemies, mapping their ID to their object class
enemies = dict()
enemy_id = 0

# The boundary values a bullet dies at when outside
MIN_X = -display.DISPLAY_WIDTH
MAX_X = display.DISPLAY_WIDTH*2
MIN_Y = -display.DISPLAY_HEIGHT
MAX_Y = display.DISPLAY_HEIGHT*2


def enemy_create(enemy):
    """Assign an enemy an ID, and add it to the enemies dictionary

    :param enemy: An instantiated enemy
    """

    global enemy_id
    enemies[enemy_id] = enemy
    enemy.id = enemy_id
    enemy_id = enemy_id + 1


def enemy_destroy(enemy):
    """Remove an enemy from the enemies dictionary

    :param enemy: An enemy which is already in the dictionary
    """

    global enemies
    enemies.pop(enemy.id)

