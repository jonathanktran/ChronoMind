"""This file is used to extract the data from actual gameplay."""

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

# Otherwise, record during gameplay
input("Press enter when ready.")
# For timed attention task (1 minute per trial)
waves = None
raw = None
attention = None
data = []
row = []
t_start = time.time()
t_end = time.time() + 1 * 60  # run for 1 minute
while time.time() < t_end:
    waves = interface.get_waves(0)
    raw = interface.get_raw(0)
    attention = interface.get_attention(0)
    blink = interface.get_blink(0)
    ts = time.time() - t_start # seconds elapsed
    print(ts)
    row = [ts, raw, attention, blink] # row of data
    for k, v in waves.items():
        row.append(v) # append wave power
    # Calculate our attention ratio (gamma/alpha) and insert into list
    gamma = row[11]
    alpha = (row[6] + row[7]) / 2
    row.insert(3, gamma / alpha)
    data.append(row) # append to large dataset
    time.sleep(0.1)
print("Recording completed!")

# Creating gameplay dataframe
# Wave data format:
# ['delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
df = pd.DataFrame(data, columns=['seconds', 'raw_value', 'attention', 'our_attention', 'blink', 'delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma'])

# Saving to data directory
df.to_csv("../neurosky/data/game_1_min.csv")

# Close Neurosky connection
interface.disconnect()