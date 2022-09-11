import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
import soundfile as sf
import sounddevice as sd
from wave_buffer import WaveBuffer

MIN_PM = 0.0
MAX_PM = 1000
MIN_VOL = 0
MAX_VOL = 1
SAMPLE_RATE = 44100
WAVETABLE_SIZE = 8192



    
# build wavetable
pollution_factor = 1
data = [2.08, 2.13, 2.18, 2.18, 2.17, 2.17, 2.36, 2.54, 2.73, 2.77, 2.81, 2.85, 2.79, 2.73, 2.67, 2.29, 1.91, 1.53, 1.32, 1.11, 0.9, 0.96, 1.03, 1.09, 1.12, 1.15, 1.18, 1.2, 1.23, 1.26, 1.28, 1.29, 1.3, 1.35, 1.4, 1.45, 1.59, 1.74, 1.88, 2.01, 2.14, 2.27, 2.18, 2.1, 2.01, 2.13, 2.24, 2.36, 2.57, 2.78, 2.98, 2.95, 2.92, 2.89, 3.35, 3.8, 4.26, 5.06, 5.86, 6.66, 6.13, 5.6, 5.07, 7.66, 10.26, 12.85, 17, 25, 21, 22, 18, 25, 26, 28, 29, 21, 53, 37, 23, 19, 18, 8, 21, 17, 13, 16, 17, 18, 15, 13, 14, 15, 12, 14, 11, 13, 17, 11, 18, 26]
a = WaveBuffer(data).mirror_extend().remap(MIN_PM, MAX_PM, MIN_VOL, MAX_VOL).amplify().interpolate().amplify().quantize(pollution_factor).get_buffer()


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

plt.plot(a)
plt.show()










