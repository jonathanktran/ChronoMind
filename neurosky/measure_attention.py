"""This file contains the methods for attention measurement during gameplay."""

from neurosky import interface
import time
from collections import deque

class AttentionMeasure:

    def __init__(self):
        # Store data extracted from the headset
        self.data = []

        # Get baseline attention level mean and standard deviation as list [mean, sd]
        self.baseline_list = interface.get_baseline("../neurosky/data/calibration.csv")

        # Duration between samples
        self.sampling_rate = 0.1

        # Current attention level
        self.curr_attention = 0

        # Attention deque to store last 10 raw_uv values from headset
        self.att_deque = deque([self.baseline_list[0] for i in range(20)])

    def sample(self):
        if interface.headset is not None:
            t_start = time.time()
            while True:
                # Current time from start
                curr_time = time.time() - t_start

                # If a blink is detected, wait before continuing trying to update att_list
                while interface.detect_blink() == True:
                    time.sleep(0.2)

                # Wait until headset steadies, then get raw_uv value
                while interface.headset.poor_signal > 5:
                    time.sleep(0.01)
                raw_uv = interface.get_microvolts(interface.get_raw(curr_time))
                # If raw_uv > 10 uV from the last value, set raw_uv to last value + 10
                if raw_uv > self.att_deque[len(self.att_deque)-1] + 10:
                    raw_uv = self.att_deque[len(self.att_deque)-1] + 10
                # If raw_uv < 10 uV from the last value, set raw_uv to last value - 10
                elif raw_uv < self.att_deque[len(self.att_deque)-1] - 10:
                    raw_uv = self.att_deque[len(self.att_deque) - 1] - 10
                # Append raw_uv values to deque
                self.att_deque.append(raw_uv)

                # Remove first value
                self.att_deque.popleft()

                # Update attention level using our attention function
                #self.curr_attention = interface.get_our_attention(self.att_deque, self.baseline_list, curr_time)
                self.curr_attention = interface.get_attention(curr_time)

                # Wait a sampling_rate number of seconds before taking next sample
                time.sleep(self.sampling_rate)
        else:
            # Set the attention to read from the gameplay file if the headset is not connected
            interface.set_file("../neurosky/data/game_1_min.csv")
        return