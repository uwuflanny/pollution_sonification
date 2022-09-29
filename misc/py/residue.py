
from http.client import BAD_GATEWAY
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
import random

DECADENCE   = 1.8
REST        = 0
BAD         = 50
HAZARDOUS   = 100
DANGEROUS   = 150

def decrement(list, unit):
    return [x - unit for x in list if x - unit > 0]

def get_residue(data, res_threshold = 50):

    residue_data    = []
    res_history     = []
      
    for pm in data:

        if pm > res_threshold:
            residue_data.append(pm)
        
        res = max(residue_data) if len(residue_data) > 0 else 0
        res_history.append(res)
        ln_res = math.log(res, DECADENCE) if res > 0 else 0
        residue_data = decrement(residue_data, ln_res)

    return res_history

def get_residue_states(data):

    states  = []
    levels  = [
        REST,
        BAD,
        HAZARDOUS,
        DANGEROUS
    ]

    for residue in data:

        level = levels[0]
        for i in range(1, len(levels)):
            if residue > levels[i]:
                level = levels[i]
            else:
                break
 
        states.append(level)

    return states

def shullfle_arpeggio(arr, pattern, step):

    # arr       = [0,1,2,3]
    # pattern   = [0,1,0,1]

    notes = []
    for i in range(len(arr)):
        if pattern[i] == 1:
            r = random.choice(arr)
            arr = [x for x in arr if x != r]
            notes.append((r, step * i))

    return notes

def assign_notes(states, arp):
    
    last    = 0

    step = 0.25 # 4 notes per beat
    elapsedQuarters = 0
    note_duration = 0.25
    notes = []

    for i in range(len(states)):

        val = states[i]

        # rising, also add hihat
        if val > last:
            notes   += [{"note": arp[0],    "time": elapsedQuarters + (step * i), "duration": note_duration } for i in range(4)]

        # not rising
        else:

            # falling, single random note
            if val == BAD:                
                random_note = np.random.randint(0, 4)
                notes.append({"note": arp[random_note], "time": elapsedQuarters, "duration": note_duration })

            # hazardous, random full arp
            elif val == HAZARDOUS:
                notes += [{"note": arp[note], "time": elapsedQuarters + time, "duration": note_duration} for note, time in shullfle_arpeggio([0,1,2,3], [1,1,1,0], step)]

            # dangerous, full arp
            elif val == DANGEROUS:
                notes += [{"note": arp[i], "time": elapsedQuarters + (step * i), "duration": note_duration } for i in range(4)]

        last = val
        elapsedQuarters += 1

    return notes


def get_residue_arpeggio(data, arp):
    residue = get_residue(data)
    states = get_residue_states(residue)
    return assign_notes(states, arp)