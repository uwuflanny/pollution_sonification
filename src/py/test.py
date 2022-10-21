from code import interact
from operator import index
import wave
import matplotlib.pyplot as plt
from wave_buffer import WaveBuffer
import math
import numpy as np
from scipy.optimize import fmin
from utility import map_value_int, map_value
from measures import WAVETABLE_SIZE, SAMPLE_RATE, BPM, MIN_THRESH, MAX_THRESH


def compute_LFO(min, max, samp_period, start_value):
    freq = 1 / (samp_period / SAMPLE_RATE)
    period = SAMPLE_RATE / freq
    half = (max - min) / 2
    return lambda x: math.sin(2.0 * math.pi * (x) / period) * half + half + min


lfo = compute_LFO(0, 3, 500, 1)
data = [lfo(i) for i in range(1000)]

plt.plot(data)
plt.show()
