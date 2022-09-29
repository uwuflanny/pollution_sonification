import numpy as np
import math
import scipy as sp

class WaveBuffer(object):

    def __init__(self, buffer):
        self.buffer = buffer

    def map_in_range(self, value, in_min, in_max, out_min, out_max):
        if value < 0:
            value   *= -1
            out_max *= -1
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def amplify(self, amp_target = 1):
        max_item = max(self.buffer)
        amp = amp_target / max_item
        return WaveBuffer([sample * amp for sample in self.buffer])

    def mirror_extend(self):
        half_len = len(self.buffer)        
        mirrored = self.buffer + self.buffer
        return WaveBuffer([mirrored[i] if i < half_len else mirrored[i] * -1 for i in range(len(mirrored))])

    def remap(self, in_min, in_max, out_min, out_max):
        return WaveBuffer([self.map_in_range(sample, in_min, in_max, out_min, out_max) for sample in self.buffer])

    # 8192 = default wavetable size
    def interpolate(self, pps = 8192):
        y = [0] + self.buffer + [0]
        x = np.arange(len(y))
        f = sp.interpolate.interp1d(x, y, kind='cubic')
        newx = np.linspace(0, len(y)-1, pps)
        return WaveBuffer(f(newx))

    def quantize(self, samples):
        return WaveBuffer([self.buffer[math.floor(i / samples) * samples] for i in range(len(self.buffer))])

    def get_buffer(self):
        return self.buffer


def calculate_wavetable(data, pollution_factor):
    MIN_PM = 0.0
    MAX_PM = 1000
    MIN_VOL = 0
    MAX_VOL = 1
    SAMPLE_RATE = 44100
    WAVETABLE_SIZE = 8192
    return WaveBuffer(data).mirror_extend().remap(MIN_PM, MAX_PM, MIN_VOL, MAX_VOL).amplify().interpolate().amplify().quantize(pollution_factor).get_buffer()


