"""This file contains methods for interfacing with the NeuroSky headset."""

from neurosky import mindwave
import time
import pandas as pd
from scipy.fft import fft, fftfreq


# A reference to the NeuroSky headset
headset = None

# Read the recorded attention
recorded_headset = None

# The number of seconds recorded
recorded_time = None


def connect(version):
    """
    Code to connect to Neurosky, adapted from neurosky.py.
    Make sure that the headset (MindWave Mobile) is connected to your computer 
    using Bluetooth to avoid connection issues.
    """

    global headset

    # Try connecting to the headset
    try:
        print("Connecting...")
        if version == "Windows":
            headset = mindwave.Headset('COM6')  # windows version. set up COM port first (see video)
        else:
            headset = mindwave.Headset('/dev/tty.MindWaveMobile-SerialPo')  # mac version
        print("Connected!")

        print("Starting...")

        # Wait for the headset to steady down
        while headset.poor_signal > 5 or headset.attention == 0:
            time.sleep(0.1)
        print('Started!')

    # If the headset could not connect, keep the headset as None.
    except Exception:
        print("Could not Connect, using recorded NeuroSky values.")


def nearest_recorded_sample(time):
    """This method is used to find the recorded sample taken at the time nearest the current time, when the headset
    is not used and a recording of the headset is being used instead.

    :param time: The nearest time to find in seconds
    :return values: The recorded headset values who's timestamp is closest to the given
    """

    return recorded_headset.iloc[(recorded_headset['seconds']-(time % recorded_time)).abs().argsort()[0]]


def get_attention(time):
    """ The function returns the current attention level measured by the neurosky.
    If the neurosky is not connected, a recording of brain activity is used instead. This recording lasts one minute,
    and loops after each minute passes.

    :param time: The current time in seconds
    :return attention: The current attention of the headset or the recording, as an integer.
    """

    # If the headset is connected
    if headset is not None:
        return headset.attention

    # If the headset is not connected, return the recorded value for the given time
    else:
        return nearest_recorded_sample(time)["attention"]


def get_waves(time):
    """ The function returns each of the current wave bands level measured by the neurosky.
    If the neurosky is not connected, a recording of brain activity is used instead. This recording lasts one minute,
    and loops after each minute passes.

    :param time: The current time in seconds
    :return waves: A list of the current wave bands of the headset or the recording, as an integer.
    """

    # If the headset is connected
    if headset is not None:
        return headset.waves

    # If the headset is not connected, return the recorded values for the given time
    else:
        return nearest_recorded_sample(time)[5:]


def get_raw(time):
    """ The function returns the current raw value measured by the neurosky.
    If the neurosky is not connected, a recording of brain activity is used instead. This recording lasts one minute,
    and loops after each minute passes.

    :param time: The current time in seconds
    :return raw: The current raw value measured by headset or the recording, as an integer.
    """

    # If the headset is connected
    if headset is not None:
        return headset.raw_value

    # If the headset is not connected, return the recorded value for the given time
    else:
        return nearest_recorded_sample(time)["raw_value"]


def get_blink(time):
    """ The function returns the current blink value measured by the neurosky.
    If the neurosky is not connected, a recording of brain activity is used instead. This recording lasts one minute,
    and loops after each minute passes.

    :param time: The current time in seconds
    :return blink: The current blink value measured by headset or the recording, as an integer.
    """

    # If the headset is connected
    if headset is not None:
        return headset.blink

    # If the headset is not connected, return the recorded value for the given time
    else:
        return nearest_recorded_sample(time)["blink"]


def disconnect():
    '''
    Code to disconnect from Neurosky.
    '''
    if headset is not None: headset.stop()
    print("Stopped!")


def test_connection(): 
    '''
    Testing if code runs as expected.
    '''
    connect("Darwin")
    
    t_end = time.time() + 10 # run for 10 seconds
    while time.time() < t_end:
        print(get_attention())
        time.sleep(0.01)
    
    disconnect()


def get_values(time):
    """This function returns the current values of the headset as a list. If the headset is not connected, a list of
    recorded values at the nearest time are returned instead.

    :param time: The current time in seconds
    :return blink: The current blink value measured by headset or the recording, as an integer.
    """

    # If the headset is connected, return a list of values in the following form:
    # ['seconds', 'raw_value', 'attention', 'our-attention', 'blink',
    # 'delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
    if headset is not None:

        # Create a list of neurosky pre-made measures
        measure_list = [time, headset.raw_value, headset.attention, headset.blink]

        # Append each wave band to the list
        # Neurosky defines low-alpha: 7.5-9.25 Hz, high-alpha: 10-11.75 Hz, mid-gamma: 41-49.75 Hz
        # http://developer.neurosky.com/docs/doku.php?id=thinkgear_communications_protocol
        for k, v in headset.waves.items():
            measure_list.append(v)

        # Calculate our attention ratio (gamma/alpha) and insert into list
        gamma = measure_list[11]
        alpha = (measure_list[6] + measure_list[7]) / 2
        if alpha == 0: # to avoid division by 0
            measure_list.insert(3, 2)
        else:
            measure_list.insert(3, gamma/alpha)

        # Return the list of measures and waves
        return measure_list

    # If the headset is not connected, return the recorded values for the given time
    else:
        return nearest_recorded_sample(time)[1:].tolist()


def to_dataframe(data):
    """This method returns a dataframe from a given list of neurosky headset data.

    :param data: A list of lists, where each list contains headset information
    """

    # Create a dataframe from the data with the given form:
    # ['seconds', 'raw_value', 'attention', 'our-attention', 'blink',
    # 'delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
    return pd.DataFrame(data, columns=['seconds', 'raw_value', 'attention', 'our-attention', 'blink', 'delta', 'theta', 'low-alpha',
                                     'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma'])


def set_file(file):
    """Set the file to read from, in the event that the headset is not connected"""

    global recorded_headset, recorded_time

    # Read the recorded headset values as a dataframe
    recorded_headset = pd.read_csv(file)

    # Find the number of seconds in the recorded headset file
    recorded_time = recorded_headset.iloc[-1]['seconds']


def get_baseline(data_csv):
    """This method takes a data csv file and returns the baseline attention level:
    mean and standard deviation

    :param data_csv: A list of lists, where each list contains headset information
    :return a list [att, sd] where att is attention and sd is standard deviation
    """

    df = pd.read_csv(data_csv)
    att = df['our-attention'].mean()
    sd = df['our-attention'].std()

    return [att, sd]


def get_rolling_mean(att_list):
    """This method calculates the player's attention level using a list of the last 10 attention values recorded by the headset

    :param att_list: A list of the last 10 attention values recorded by the headset
    :return att_level: A rolling average of the last 10 attention values
    """

    att_level = sum(att_list)/len(att_list)
    return att_level


def get_slow_strength(rolling_att, baseline_list):
    """This method calculates the number of standard deviations the attention level is away from the baseline attention level

    :param rolling_att: A rolling average of the player's last 10 attention values
    :param baseline_list: A list [baseline_att_mean, baseline_att_sd]
    :return slow_strengh: The slow strengh if it is greater than 0, otherwise 0
    """

    baseline_att = baseline_list[0]
    sd = baseline_list[1]

    slow_strength = (rolling_att - baseline_att)/sd
    
    # Return 0 instead of slow strength if slow strength is less than 0
    if slow_strength < 0:
        return 0
        
    return slow_strength


def get_our_attention(att_deque, baseline_list, sampling_rate, time):
    """This method calculates an attention level from 0-100 based on the number of
    standard deviations away from the baseline attention level

    :param att_deque: A deque of the last 1 second attention values recorded by the headset
    :param baseline_list: A list [baseline_att_mean, baseline_att_sd]
    :param time: Current time since starting the game
    :return current_attention: A calculated attention level from 0-100
    """
    # If the headset is connected
    if headset is not None:
        if len(att_deque) < 1/sampling_rate:
            # If att_deque has less than 1 second data, use baseline attention instead
            rolling_att = baseline_list[0]
        else:
            # Get rolling mean of attention values
            rolling_att = get_rolling_mean(att_deque)

        # Find number of standard deviations rolling_att is from baseline_att
        num_sd = get_slow_strength(rolling_att, baseline_list)

        # Calculate attention level using number of standard deviations from baseline
        if(num_sd >= 3):
            current_attention = 100
        else:
            current_attention = num_sd/3 * 100
        
        return current_attention

    # If the headset is not connected, return the recorded value for the given time
    else:
        return nearest_recorded_sample(time)["attention"]

def get_att_ratio(time):
    """This method gets the attention level by dividing the player's gamma value by their alpha value"""

    if headset is not None:
        # Get list of headset waves
        waves_list = []
        for k, v in headset.waves.items():
            waves_list.append(v)

        # Calulate attention ratio (gamma/alpha)
        gamma = waves_list[7]
        alpha = (waves_list[2] + waves_list[3]) / 2
        if alpha == 0: # to avoid division by 0
            our_att_ratio = 2
        else:
            our_att_ratio = gamma/alpha
        return our_att_ratio

    # If the headset is not connected, return the recorded value for the given time
    else:
        return nearest_recorded_sample(time)["our-attention"]

def get_microvolts(raw_value):
    """This method converts the raw_value to microvolts, based on the link:
    http://support.neurosky.com/kb/science/how-to-convert-raw-values-to-voltage

    :param raw_value: raw value from Neurosky headset, as seen in csv files
    :return: value in microvolts
    """
    return raw_value * (1.8/4096) / 2000 * 1000000

def remove_blink(df):
    """Filters out blink data from calibration data, before and after the
    peak blink.

    :param df: calibration dataframe containing column called "raw_value"
    :return: calibration dataframe containing column called "raw_uv" that
    has removed blinks
    """

    # Convert raw_value to microvolts for analysis
    df["raw_uv"] = get_microvolts(df["raw_value"])

    # Make sure df index is correct
    df = df.reset_index()

    # Find index of raw_uv column
    raw_uv_ind = df.columns.get_loc("raw_uv")

    # Create dataframe of values above 75 uV or below -75 uV
    # As these are very high, they are most likely blinks
    out_range_df = df[(df["raw_uv"] >= 75) | (df["raw_uv"] <= -75)]

    # For each point in the out of range dataframe:
    for time in out_range_df["seconds"]:
        # Obtain the previous value of raw_uv (before the blink section)
        prev_df = df[df["seconds"] < time - 0.2]
        prev_ind = int(prev_df.iloc[len(prev_df) - 1]["index"])
        prev_uv = df.iloc[prev_ind, raw_uv_ind]
        # For the range less than 200 ms and greater than 200 ms of the peak blink,
        # Set these equal to the previous value of raw_uv
        df.loc[(df["seconds"] <= time + 0.2) & (df["seconds"] >= time - 0.2), "raw_uv"] = prev_uv
    return df

def transform_calibration(df):
    """Uses Fast Fourier Transform on the raw values in microvolts and
    appends the transformed values as a new column in the provided df

    :param df: calibration dataframe without any filtering
    :return: calibration dataframe with power values for gamma and alpha appended
    """
    # Perform filtering on dataframe
    df = remove_blink(df)

    # Perform FFT
    df["transformed_uv"] = fft((df["raw_uv"]).to_numpy())
    N = len(df) # number of points
    T = 0.5  # sample spacing: currently 0.5 s
    freq = fftfreq(N, T)[:N // 2]  # frequency
    power = 2.0 / N * np.abs(df["transformed_uv"][0:N // 2])

    # # Put FFT transform results into a dataframe
    # freq_pow_df = pd.DataFrame(data={'freq': freq, 'power': power})
    #
    # # Create subset dataframes for alpha and gamma
    # alpha_df = freq_pow_df[(freq_pow_df["freq"] >= 8) & (freq_pow_df["freq"] <= 13)]
    # gamma_df = freq_pow_df[(freq_pow_df["freq"] >= 30) & (freq_pow_df["freq"] <= 50)]
    #
    # # Calculate the mean power for alpha and gamma and append to our dataframe
    # df["our-alpha"] = alpha_df["power"].mean()
    # df["our-gamma"] = gamma_df["power"].mean()
    #
    # # Edit the our-attention column to have the ratio using our derived
    # # alpha and gamma values
    # df["our-attention"] = df["our-gamma"] / df["our-alpha"]
    return df

def detect_blink():
    """Checks if there is a blink at the current point

    :param df: calibration dataframe containing column called "raw_value"
    :return: calibration dataframe containing column called "raw_uv" that
    has removed blinks
    """

    if headset is not None:
        # Convert raw_value to microvolts for analysis
        raw_uv = get_microvolts(headset.raw_value)
        if (raw_uv >= 75) | (raw_uv <= -75):
            return True
        else:
            return False
    else:
        return False