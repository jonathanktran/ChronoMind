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

        # Attention deque to store last 20 raw_uv values from headset
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

                # Append raw_uv values to deque
                self.att_deque.append(raw_uv)

                # Remove first value
                self.att_deque.popleft()

                # Update attention level using our attention function
                new_attention = interface.get_our_attention(self.att_deque, self.baseline_list, curr_time)
                # If new_attention > 10 from the curr_attention, set curr_attention to curr_attention + 10
                if new_attention > self.curr_attention + 10:
                    self.curr_attention = self.curr_attention + 10

                # If new_attention < 10 from the curr_attention, set curr_attention to curr_attention - 10
                elif new_attention < self.curr_attention - 10:
                    self.curr_attention = self.curr_attention - 10

                # If new_attention is within 10 of the curr_attention, just update curr_attention with
                # the new_attention value
                else:
                    self.curr_attention = new_attention

                # Wait a sampling_rate number of seconds before taking next sample
                time.sleep(self.sampling_rate)
        else:
            # Set the attention to read from the gameplay file if the headset is not connected
            interface.set_file("../neurosky/data/game_1_min.csv")
        return