import numpy as np
import math
import scipy as sp
from scipy.interpolate import splev, splrep
from measures import WAVETABLE_SIZE

class WaveBuffer(object):

    def __init__(self, buffer):
        self.buffer = buffer

    def amplify(self, amp_target = 1):
        max_item = max(self.buffer)
        amp = amp_target / max_item
        return WaveBuffer([sample * amp for sample in self.buffer])

    def mirror_extend(self):
        half_len = len(self.buffer)        
        mirrored = self.buffer + self.buffer
        return WaveBuffer([mirrored[i] if i < half_len else mirrored[i] * -1 for i in range(len(mirrored))])

    def interpolate(self, points = WAVETABLE_SIZE): # 8192 = default wavetable size
        y = self.buffer
        x = np.arange(len(y))
        spl = splrep(x, y, per=True)
        newx = np.linspace(0, len(y)-1, points)
        return WaveBuffer(splev(newx, spl))

    def quantize(self, samples):
        return WaveBuffer([self.buffer[math.floor(i / samples) * samples] for i in range(len(self.buffer))])

    def get_buffer(self):
        return self.buffer




