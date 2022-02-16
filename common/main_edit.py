"""This file is the main class, which runs the game."""
import os
import sys
sys.path.insert(0,"../neurosky")
import add_attention
sys.path.insert(0, os.path.abspath("/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages"))

from run_edit import run
from display import *
from enemies import enemy_list
from rounds import round_list
import player
import music
import threading

# Connect to Neurosky headset - specify "mac" or "windows"
add_attention.connect("mac")

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Create the music object
audio = music.AudioFile('../assets/music/Megalovania.wav')

# Adjust the music to remove start offset
audio.wf.setpos(6400)

# Start the music
music_thread = threading.Thread(target=audio.play)

# Play the music
music_thread.start()

# Run the game
run(player, enemy_list, round_list, audio)

# Stop the music thread
audio.stop = True
music_thread.join()

# Close the window
pg.quit()
