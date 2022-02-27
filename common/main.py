"""This file is the main class, which runs the game."""

from run import run
from run_maths import run_maths
from display import *
from enemies import enemy_list
from rounds import round_list
import player
import music
import threading
import platform
from neurosky import interface


# Connect to Neurosky headset
interface.connect(platform.system())

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Create the music object
audio = music.AudioFile('../assets/music/Megalovania.wav')

# Adjust the music to remove start offset
audio.wf.setpos(6400)

# This variable tracks whether the game has been told to stop
stop = False

# Create the music thread
music_thread = threading.Thread(target=audio.play)

# Run the upper-limit attention calibration
stop = run_maths()

# Play the music
if not stop: music_thread.start()

# Run the game
if not stop: stop = run(player, enemy_list, round_list, audio)

# Stop the music thread
audio.stop = True
if not stop and music_thread.is_alive(): music_thread.join()

# Disconnect the headset
interface.disconnect()

# Close the window
pg.quit()
