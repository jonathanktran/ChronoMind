from neurosky import interface
import time

class Calibration:

    def __init__(self, max_min):
        # Store data extracted from the headset
        self.data = []

        # Number of minutes to sample
        self.max_min = 1
        
        # Duration between samples (0.1 s = 10 samples/second)
        self.sampling_rate = 0.1

    def sample(self):
        if interface.headset is not None:
            # Run for t_end seconds
            t_start = time.time()
            t_end = t_start + self.max_min * 60
            while time.time() < t_end:
                # Append values every sampling_rate number of seconds
                self.data.append(interface.get_values(time.time() - t_start))
                time.sleep(self.sampling_rate)

            # Transform to dataframe
            df = interface.to_dataframe(self.data)

            # Transform so data starts at 0 seconds
            start_time = df["seconds"][0]
            df["seconds"] = df["seconds"] - start_time

            # FFT on dataframe to get alpha and gamma power
            df = interface.transform_calibration(df)

            # Save as calibration file in data folder
            df.to_csv("../neurosky/data/calibration.csv", index=False)
        else:
            # Set the attention to read from the calibration file if the headset is not connected
            interface.set_file("../neurosky/data/calibration.csv")
        return