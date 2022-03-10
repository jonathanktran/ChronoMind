import pandas as pd
import numpy as np
from neurosky import interface
import time
from collections import deque

class AttentionMeasure:

    def __init__(self):
        # Store data extracted from the headset
        self.data = []

        # Get baseline attention level mean and standard deviation as list [mean, sd]
        self.baseline_list = interface.get_baseline("../neurosky/data/calibration.csv")

        # Attention deque to store last 10 attention values from headset
        self.att_deque = deque()

        # Duration between samples
        self.sampling_rate = 0.1

        # Current attention level
        self.curr_attention = 0

    def sample(self):
        if interface.headset is not None:
            t_start = time.time()
            while True:
                # Current time from start
                curr_time = time.time() - t_start

                # If a blink is detected, wait before continuing trying to update att_list
                while interface.detect_blink() == True:
                    time.sleep(0.2)

                # Append attention ratio to list and remove first value if more than 1 sec data
                self.att_deque.append(interface.get_att_ratio(curr_time))
                if len(self.att_deque) > 1/self.sampling_rate:
                    self.att_deque.popleft()

                # Update attention level using our attention function
                self.curr_attention = interface.get_our_attention(self.att_deque, self.baseline_list, self.sampling_rate, curr_time)

                # Wait a sampling_rate number of seconds before taking next sample
                time.sleep(self.sampling_rate)
        else:
            # Set the attention to read from the gameplay file if the headset is not connected
            interface.set_file("../neurosky/data/game_1_min.csv")
        return