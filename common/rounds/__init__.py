# A list of all rounds
rounds = dict()
round_id = 0


def round_create(round):
    """Create a round"""

    global round_id
    rounds[round_id] = round
    round.id = round_id
    round_id = round_id + 1


def round_destroy(round):
    """Destroy a round"""
    global rounds
    rounds.pop(round.id)
