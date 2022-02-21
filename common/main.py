"""This file is the main class, which runs the game."""

from run import run
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

# Start the music
music_thread = threading.Thread(target=audio.play)

# Play the music
music_thread.start()

# Run the game
run(player, enemy_list, round_list, audio)

# Stop the music thread
audio.stop = True
music_thread.join()

# Disconnect the headset
interface.disconnect()

# Close the window
pg.quit()
