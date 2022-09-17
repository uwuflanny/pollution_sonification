
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
import random

def decrement(list, unit):
    return [x - unit for x in list if x - unit > 0]

def get_residue(data, res_threshold = 50):

    residue_data    = []
    res_history     = []
    DECADENCE       = 1.8
    
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
        0,      # REST
        50,     # FALLING
        100,    # HARARDOUS
        150     # DANGEROUS
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

def assign_notes(data, arp):
    
    last    = 0
    levels  = [
        0,      # REST
        50,     # FALLING
        100,    # HARARDOUS
        150     # DANGEROUS
    ]

    step = 0.25 # 4 notes per beat
    elapsedQuarters = 0
    note_duration = 0.25
    notes = []

    for val in data:

        # rising, also add hihat
        if val > last:
            for i in range(4):
                notes.append({
                    "note": arp[0],
                    "time": elapsedQuarters + (step * i),
                    "duration": note_duration
                })

        # not rising
        else:

            # falling, random notes
            if val == levels[1]:                
                r = np.random.randint(0, 4)
                notes.append({
                    "note": arp[r],
                    "time": elapsedQuarters,
                    "duration": note_duration
                })

            # hazardous, random full arp
            elif val == levels[2]:
                for note, time in shullfle_arpeggio([0,1,2,3], [1,1,1,0], step):
                    notes.append({
                        "note": arp[note],
                        "time": elapsedQuarters + time,
                        "duration": note_duration
                    })

            # dangerous, full arp
            elif val == levels[3]:
                for i in range(4):
                    notes.append({
                        "note": arp[i],
                        "time": elapsedQuarters + (step * i),
                        "duration": note_duration
                    })

                
                


        last = val
        elapsedQuarters += 1

    return notes