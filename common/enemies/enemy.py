"""This is the abstract parent class for all enemies"""


class Enemy:

    def __init__(self):
        pass

    def step(self, dt):
        """The code runs every loop"""
        pass

    def collide(self):
        """This code runs when the enemy collides with the player"""
        pass

    def draw(self):
        """Draw the bulllet to the screen"""
        pass
