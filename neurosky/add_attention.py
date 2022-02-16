# Use the get_attention(headset) function in neurosky.py to get the current attention level
# Will need to find a way to constantly update the attention level 
# (something like an infinite loop, or constant calls to a function)

# Potential variables to create: attention_threshold, attention (= get_attention(headset))

import mindwave
import pandas as pd
import time

headset = None

def connect(version):
    '''
    Code to connect to Neurosky, adapted from neurosky.py.
    Make sure that the headset (MindWave Mobile) is connected to your computer 
    using Bluetooth to avoid connection issues.
    '''
    global headset
    
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
    
def get_attention():
    '''
    Obtain the current Neurosky attention level measure.
    Use this in the game code to print the attention measure.
    '''
    return headset.attention
    
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

    

# SPACE INVADERS PROJECT CODE BELOW FOR REFERENCE:


# # Display attention value on screen
#     self.attentionText = Text(FONT, 20, 'Attention', WHITE, 180, 5)

# # Neuropy values
#     self.attMathValue = Text(FONT, 25, str(self.neuropy.attention), GREEN, 480, 450)
#     self.attMathValue.draw(self.screen)

# # add non-zero value of attention and meditation
#     if self.neuropy.attention > 0: # INSTEAD WE WILL FEED IN THE ATTENTION MEASURE RECORDED FROM HEADSET
#         self.attPractice.append(self.neuropy.attention)
        
# # Check if att and med are above threshold value
#     self.attHigh = True if self.neuropy.attention >= self.attThreshold else False
    
# # Draw neuropy text and value
#     attColor = GREEN
#     if self.attHigh:
#         attColor = RED
#     self.attentionText2 = Text(FONT, 20, str(self.neuropy.attention), attColor, 320, 5)
#     self.attentionText2.draw(self.screen)
#     self.attentionText.draw(self.screen)
    
# # Slow motion when attention is high
#      if self.attHigh:
#         # implement slowmo