"""This file is used to extract the data from our math-related attention task."""

import neurosky.interface as interface
import platform
import pandas as pd
import time

# Connect to Neurosky headset
interface.connect(platform.system())
# If connection fails, end
if interface.headset == None:
    print("Please check your Bluetooth connection to the headset.")
    exit(1)

# Getting the list of participants
str_participant = input("Enter the participant names separated only by spaces: ")
participants = str_participant.split()

# Specify number of trials
num_trials = 1

for participant in participants:
    trial = 1
    while trial <= num_trials:
        input("Press enter when ready.")
        print("Commencing trial " + str(trial) + " of participant " + participant + "...")
        # For timed attention task (1 minute per trial)
        waves = None
        raw = None
        attention = None
        data = []
        row = []
        t_start = time.time()
        t_end = time.time() + 1 * 60  # run for 1 minute
        while time.time() < t_end:
            waves = interface.get_waves()
            raw = interface.get_raw()
            attention = interface.get_attention()
            blink = interface.get_blink()
            ts = time.time() - t_start # seconds elapsed
            print(ts)
            row = [ts, raw, attention, blink] # row of data
            for k, v in waves.items():
                row.append(v) # append wave power
            time.sleep(0.01)
            data.append(row) # append to large dataset
        print("Trial completed!")
        trial += 1

        # Creating dataframe
        # Wave data format:
        # ['delta', 'theta', 'low-alpha', 'high-alpha',
        # 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
        df = pd.DataFrame(data, columns=['seconds', 'raw_value', 'attention', 'blink', 'delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma'])

        # Saving to data directory
        df.to_csv("../neurosky/data/" + str(participant) + "_" + str(trial-1) + ".csv")

# Close Neurosky connection
interface.disconnect()