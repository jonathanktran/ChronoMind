"""This is the abstract parent class for all enemies."""


class Enemy:
    """This is the abstract parent class for all enemies."""

    def __init__(self):
        pass

    def step(self, dt):
        """The runs every step

        :param dt: The amount of time since the previous frame
        """
        pass

    def collide(self):
        """This runs when this enemy collides with the player"""
        pass

    def draw(self):
        """Draw this enemy to the screen"""
        pass
