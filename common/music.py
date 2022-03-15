"""This file contains music files and methods used to control them."""

import wave
from pyaudio import PyAudio
import numpy as np


class AudioFile:

    # The number of samples to read per channel
    chunk = 1600

    def __init__(self, file):
        """Initialize the Wave Read, and the Output Stream"""

        # This is a flag used to stop the audio playback
        self.stop = False

        # The rate the audio is played at
        self.rate = 1

        # The volume multiplier of the audio
        self.volume = 1

        # Get the wave file as an object
        self.wf = wave.open(file, 'rb')

        # Create the audio stream based on the wave file
        self.p = PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=int(self.wf.getframerate()),
            output=True)

    def set_rate(self, rate):
        """Set the playback rate of the music.

        :param rate: The multiplier of playback speed.
        """

        self.rate = rate

    def set_volume(self, volume):
        """Set the volume of the music.

        :param volume: The multiplier of the base volume
        """

        self.volume = volume

    def play_chunk(self):
        """Play a chunk of music at the given framerate"""

        # Find the number of real samples
        samples_per_channel = int(self.chunk * self.rate)

        # Find the audio frames from both channels, who's amplitude is modified by the volume.
        real_tones = np.fromstring(self.wf.readframes(samples_per_channel), dtype=np.int16).astype(np.float) \
                     * self.volume

        # If the track is at the end, sample from the beginning again
        if len(real_tones) != samples_per_channel*2:
            self.wf.setpos(0)
            wrapped_tones = np.fromstring(self.wf.readframes(int(samples_per_channel - len(real_tones)/2)),
                                          dtype=np.int16).astype(np.float) * self.volume
            real_tones = np.append(real_tones, wrapped_tones)

        # Check for the end of the file
        if len(real_tones) == 0:
            self.stop = True
            return

        # Find the sample positions for real tones
        real_samples = np.array([i for i in range(samples_per_channel)])

        # Find the sample positions for artificial tones
        artificial_samples = np.linspace(0.0, samples_per_channel - 1.0, self.chunk)

        # Find artificial tones produced at the desired sample times
        channel_0 = np.interp(artificial_samples, real_samples, real_tones[::2]).astype(np.int16)
        channel_1 = np.interp(artificial_samples, real_samples, real_tones[1::2]).astype(np.int16)

        # Combine the two channels
        artificial_tones = np.zeros(self.chunk*2, dtype=np.int16)
        for i in range(int(self.chunk)):
            artificial_tones[2 * i] = channel_0[i]
            artificial_tones[2 * i + 1] = channel_1[i]

        # Output the audio
        self.stream.write(artificial_tones.tobytes())

    def play(self):
        """Play the entire audio file, or until the audio is stopped"""

        # Play chunks until the audio is stopped
        while not self.stop:

            # Play another chunk
            self.play_chunk()

    def close(self):
        """Close the Output Stream and the Pyaudio Object"""

        self.stream.close()
        self.p.terminate()
