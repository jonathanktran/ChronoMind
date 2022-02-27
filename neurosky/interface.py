"""This file contains methods for interfacing with the NeuroSky headset."""

import neurosky.mindwave as mindwave
import time
import pandas as pd


# A reference to the NeuroSky headset
headset = None

# Read the recorded attention
recorded_headset = pd.read_csv("../neurosky/data/game_1_min.csv")


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
        while (headset.poor_signal > 5 or headset.attention == 0):
            time.sleep(0.1)
        print('Started!')

    # If the headset could not connect, keep the headset as None.
    except Exception:
        print("Could not Connect")


def nearest_recorded_sample(time):
    """This method is used to find the recorded sample taken at the time nearest the current time, when the headset
    is not used and a recording of the headset is being used instead.

    :param time: The nearest time to find in seconds
    :return values: The recorded headset values who's timestamp is closest to the given
    """

    return recorded_headset.iloc[(recorded_headset['seconds']-(time % 60)).abs().argsort()[0]]


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
    headset.stop()
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
    # ['seconds', 'raw_value', 'attention', 'blink',
    # 'delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
    if headset is not None:

        # Create a list of neurosky pre-made measures
        measure_list = [time, headset.raw_value, headset.attention, headset.blink]

        # Append each wave band to the list
        for k, v in headset.waves.items():
            measure_list.append(v)

        # Return the list of measures and waves
        return measure_list

    # If the headset is not connected, return the recorded values for the given time
    else:
        return nearest_recorded_sample(time)[1:].tolist()


def to_csv(data):
    """This method creates a csv file in the data folder from a given list of neurosky headset data.

    :param data: A list of lists, where each list contains headset information
    """

    # Create a dataframe from the data with the given form:
    # ['seconds', 'raw_value', 'attention', 'blink',
    # 'delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
    df = pd.DataFrame(data, columns=['seconds', 'raw_value', 'attention', 'blink', 'delta', 'theta', 'low-alpha',
                                     'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma'])

    # Write the dataframe to a file
    df.to_csv("../neurosky/data/calibration.csv")
