"""This file contains methods for interfacing with the NeuroSky headset."""

import neurosky.mindwave as mindwave
import time


# A reference to the NeuroSky headset
headset = None


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
    
def get_attention():
    '''
    Obtain the current Neurosky attention level measure.
    Use this in the game code to print the attention measure.
    '''
    return headset.attention if headset is not None else 45

def get_waves():
    '''
    Obtain the current wave powers in a list of format:
    ['delta', 'theta', 'low-alpha', 'high-alpha',
    'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']
    '''
    return headset.waves if headset is not None else []

def get_raw():
    '''
    Obtain the current raw EEG value.
    '''
    return headset.raw_value if headset is not None else -1

def get_blink():
    '''
    Obtain the current Neurosky attention level measure.
    Use this in the game code to print the attention measure.
    '''
    return headset.blink if headset is not None else -1

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
