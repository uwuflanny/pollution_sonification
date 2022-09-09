import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
import soundfile as sf
import sounddevice as sd


MIN_PM = 0.0
MAX_PM = 1000
MIN_VOL = 0
MAX_VOL = 1
SAMPLE_RATE = 44100
WAVETABLE_SIZE = 8192




def map_in_range(value, in_min, in_max, out_min, out_max):
    if value < 0:
        value   *= -1
        out_max *= -1
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def mirror_extend(data):
    data_len = len(data)
    for i in range(data_len):
        data.append(data[i] * -1)

def remap(data):
    for i in range(len(data)):
        data[i] = map_in_range(data[i], MIN_PM, MAX_PM, MIN_VOL, MAX_VOL)

def amplify(data):
    max_item = max(data)    
    amp = 1 / max_item
    for i in range(len(data)):
        data[i] *= amp # floor needed ?

def interpolate(data, pps = WAVETABLE_SIZE):
    y = [0] + data + [0]    
    x = np.arange(len(y))
    f = sp.interpolate.interp1d(x, y, kind='cubic')
    newx = np.linspace(0, len(y)-1, pps)
    return f(newx)

def quantize(wave, samples):
    for i in range(len(wave)):
        wave[i] = wave[math.floor(i / samples) * samples]

    
# build wavetable
data = [4,8,12,15,17,18,18,17,15,12,8,4]
# data = [120,120,120,120,120,120,120,120,120,120,120,120]
pollution_factor = 1
mirror_extend(data)
remap(data)
amplify(data)
a = interpolate(data, WAVETABLE_SIZE)
amplify(a)
quantize(a, pollution_factor)

"""
 
# render audio
SECONDS_PLAY = 2
BUFF_SIZE = SAMPLE_RATE * SECONDS_PLAY
freq = 440
step = (freq * WAVETABLE_SIZE) / SAMPLE_RATE
buf = []
for i in range(BUFF_SIZE):
    buf.append(a[math.floor(i * step) % WAVETABLE_SIZE])

sd.play(buf, SAMPLE_RATE)
sd.wait()
"""
plt.plot(a)
plt.show()










