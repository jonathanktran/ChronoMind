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
        if version == "mac":
            headset = mindwave.Headset('/dev/tty.MindWaveMobile-SerialPo') # mac version
        else:
            headset = mindwave.Headset('COM6') # windows version. set up COM port first (see video)
        print("Connected!")

        print("Starting...")

        # Wait for the headset to steady down
        while (headset.poor_signal > 5 or headset.attention == 0):
            time.sleep(0.1)
        print('Started!')

    # If the headset could not connect, keep the headset as None.
    except Exception:
        pass

    
def get_attention():
    '''
    Obtain the current Neurosky attention level measure.
    Use this in the game code to print the attention measure.
    '''
    return headset.attention if headset is not None else 45


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
    connect("mac")
    
    t_end = time.time() + 10 # run for 10 seconds
    while time.time() < t_end:
        print(get_attention())
        time.sleep(0.01)
    
    disconnect()
