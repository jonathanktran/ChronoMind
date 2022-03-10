"""This file is the main class, which runs the game."""

from run import run
from run_maths import run_maths
from run_homescreen import run_homescreen
from display import *
from enemies import enemy_list
from rounds import round_list
import player
import music
import threading
import platform
from neurosky import interface, calibration, measure_attention
import attention
import pandas as pd


# region Initialization

# Connect to Neurosky headset
interface.connect(platform.system())

# Create the player
player = player.Player(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)

# Create the music object
audio = music.AudioFile('../assets/music/Megalovania.wav')
audio.set_volume(1/2)

# Adjust the music to remove start offset
audio.wf.setpos(6400)

# This variable tracks whether the game has been told to stop
stop = False

# Create the music thread
music_thread = threading.Thread(target=audio.play)

# Create calibration object, specifying the number of minutes to run,
# which should be equivalent to the run_maths.py variable MAX_TIME / 60000
calib_obj = calibration.Calibration(1)

# Create the calibration thread
calibration_thread = threading.Thread(target=calib_obj.sample)

# Create attention measure object
att_obj = measure_attention.AttentionMeasure()

# Create the attention measure thread
attention_thread = threading.Thread(target=att_obj.sample)

# endregion Initialization

# region Run Homescreen

# Run the main menu
stop = run_homescreen()

# endregion Run Homescreen

# region Run Maths Calibration

# Run the upper-limit attention calibration
if not stop:
    # Start sampling
    calibration_thread.start()
    stop = run_maths()

# Stop sampling the calibration data
if not stop and calibration_thread.is_alive(): calibration_thread.join()

# endregion Run Maths Calibration

# region Run Game

# If the game is still running...
if not stop:

    # Play the music
    music_thread.start()

    # Calibrate the headset
    calibration_dataframe = pd.read_csv("../neurosky/data/calibration.csv")
    calibration_setting = attention.get_calibration_settings(calibration_dataframe)

# Run the game
if not stop:
    # Start measuring attention
    attention_thread.start()
    stop = run(player, enemy_list, round_list, calibration_setting, att_obj)

# Stop measuring attention
if not stop and attention_thread.is_alive(): attention_thread.join()

# endregion Run Game

# region Close Game

# Stop the music thread
audio.stop = True
if not stop and music_thread.is_alive(): music_thread.join()

# Disconnect the headset
interface.disconnect()

# Close the window
pg.quit()

# endregion Close Game
