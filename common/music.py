"""This file contains music files and methods used to control them."""

import pygame as pg


# Initialize the mixer
pg.mixer.init()

# Load the current song
pg.mixer.music.load('assets/music/Megalovania.wav')
