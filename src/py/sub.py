from code import interact
from operator import index
import wave
import matplotlib.pyplot as plt
from wave_buffer import WaveBuffer
import math
import numpy as np
from scipy.optimize import fmin
from utility import map_value_int, map_value
from measures import WAVETABLE_SIZE, SAMPLE_RATE, BPM, min_thresh, max_thresh



def get_intervals(data):

    intervals   = []
    start       = 0
    goin        = False

    for i in range(len(data)):

        val = data[i]
        
        if val >= min_thresh and goin == False:
            goin = True
            start = i

        if val < min_thresh and goin == True:
            goin = False
            intervals.append((start, i))

    # handle last position
    if goin:
        intervals.append((start, len(data)))

    return intervals



def get_wavetables(data, intervals):

    wavetables = []

    for start, end in intervals:

        interval    = data[start:end]
        if len(interval) == 1:
            interval = [interval[0], interval[0]]

        avg         = sum(interval) / len(interval)
        quantize    = map_value_int(avg, min_thresh, max_thresh, 1, 100)
        wavetable   = WaveBuffer(interval).mirror_extend().interpolate(WAVETABLE_SIZE).amplify().quantize(quantize).get_buffer()
        wavetables.append(wavetable)

    return wavetables



def envelope_buffer(buffer):

    samples     = len(buffer)
    attack_s    = samples * 0.1
    decay_s     = samples * 0.1

    for i in range(samples):
        if i < attack_s:
            buffer[i] *= map_value(i, 0, attack_s, 0, 1)
        if i > samples - decay_s:
            buffer[i] *= map_value(i, samples - decay_s, samples, 1, 0)

    return buffer


def compute_LFO(min, max, samp_period):
    freq = 1 / (samp_period / SAMPLE_RATE)
    period = SAMPLE_RATE / freq
    half = (max - min) / 2
    return lambda x: math.sin(2.0 * math.pi * (x) / period) * half + half + min


def get_wav(data, intervals, wavetables, B):

    B_PER_SEC   = BPM / 60                  # beats per second
    SECONDS     = B / B_PER_SEC             # total track seconds
    SAMPLES     = SECONDS * SAMPLE_RATE     # total track samples

    NOTE_FREQ   = 65.41                                         # C2
    NOTES_PER_B = 4                                             # notes per beat
    STEP        = (NOTE_FREQ * WAVETABLE_SIZE) / SAMPLE_RATE    # wavetable step
    SAMPS_PER_N = int(SAMPLE_RATE / B_PER_SEC / NOTES_PER_B)    # samples per note

    LFO         = compute_LFO(0.5, 1.5, SAMPLE_RATE // B_PER_SEC)
    buff        = np.zeros(int(SAMPLES))
    lfo_ptr     = 0

    for interval_idx in range(len(intervals)):

        interval    = intervals[interval_idx]
        start, end  = interval[0], interval[1]
        wavetable   = wavetables[interval_idx]

        for data_idx in range(start, end):

            aqi = data[data_idx]
            vol = map_value(aqi, min_thresh, max_thresh, 0, 0.05)
            dur = map_value_int(aqi, min_thresh, max_thresh, SAMPS_PER_N // 4, SAMPS_PER_N)

            for note_idx in range(NOTES_PER_B):

                note_start  = math.floor((data_idx + (note_idx / NOTES_PER_B)) * (SAMPLE_RATE / B_PER_SEC))
                note_buff   = np.array([wavetable[math.floor(i * STEP) % WAVETABLE_SIZE] * vol * LFO(i + lfo_ptr) for i in range(dur)])
                env_buffer  = envelope_buffer(note_buff)
                lfo_ptr     += dur
                buff[note_start:note_start + dur] += env_buffer

    return buff
        


def get_sub(data):
    
    intervals   = get_intervals(data)
    wavetables  = get_wavetables(data, intervals)
    buff        = get_wav(data, intervals, wavetables, len(data))
    return np.array([buff, buff])

