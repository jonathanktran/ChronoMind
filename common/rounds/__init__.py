"""This folder contains all round objects, and their relevant functions.
Rounds are objects which spawn enemies. Rounds die once they have spawned all their enemies.
Each round must be added to the rounds dictionary when created, and must be removed when destroyed."""

# A dictionary of all enemies, mapping their ID to their object class
rounds = dict()
round_id = 0


def round_create(round):
    """Assign a round an ID, and add it to the rounds dictionary

    :param round: An instantiated round
    """

    global round_id
    rounds[round_id] = round
    round.id = round_id
    round_id = round_id + 1


def round_destroy(round):
    """Remove an round from the rounds dictionary

    :param round: A round which is already in the dictionary
    """

    global rounds
    rounds.pop(round.id)
