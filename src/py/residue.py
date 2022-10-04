
from http.client import BAD_GATEWAY
from ssl import ALERT_DESCRIPTION_CLOSE_NOTIFY
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
import random
import sys

DECADENCE   = 1.8
REST        = 0
BAD         = 50
HAZARDOUS   = 100
DANGEROUS   = 150

# decrement every element of list by unit, of <= 0, remove
def decrement(list, unit):
    return [x - unit for x in list if x - unit > 0]

def get_residue(data, res_threshold = 50):

    residue_data    = []
    res_history     = []
      
    for pm in data:

        if pm >= res_threshold:
            residue_data.append(pm)
        
        res = max(residue_data) if len(residue_data) > 0 else 0
        res_history.append(res)
        ln_res = math.log(res, DECADENCE) if res > 0 else 0
        residue_data = decrement(residue_data, ln_res)

    return res_history


def map_value_int(value, min_value, max_value, min_result, max_result):
    return math.floor(min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result))

def arpeggiate(residue, voicing):
    
    # given an index, find the last index of rising residue
    def get_rising_end(start):
        if start == len(residue) - 1:
            return start
        for i in range(start, len(residue)-1):
            if residue[i+1] < residue[i]:
                return i
        return len(residue) - 1

    # find max value of residue
    max_res     = max(residue) # 700 or max(residue) # TODO IS max better than 700 ?
    duration    = 0.25
    notes       = []
    voicing     = [x + 12 for x in voicing] # pitch shift voicing by 2 octaves

    target_idx  = -1
    last_res    = 0
    arpeggio    = []

    init_ptr    = 0
    init_done   = True

    for i in range(len(residue) * 4):

        idx = i // 4
        res = residue[idx] 

        # rising slope detected
        if i % 4 == 0 and res > last_res and res >= BAD and idx > target_idx:

            # find the end of the rising slope
            target_idx  = get_rising_end(idx)
            target_res  = residue[target_idx]
            
            # falling arpeggio
            arpeggio    = voicing[0:map_value_int(target_res, 0, max_res, 0, len(voicing)-1)]
            first_half  = arpeggio[0:math.floor(len(arpeggio)/2)]
            second_half = arpeggio[math.floor(len(arpeggio)/2):]
            middle_part = arpeggio[math.floor(len(arpeggio)/4):math.floor(len(arpeggio)/4*3)]

            # initial arpeggio (calculated from slope height and width)
            init_start  = map_value_int(last_res,   0, max_res, 0, len(voicing) - 1)    # initial note index (mapped residue to len(voicing))
            init_end    = map_value_int(target_res, 0, max_res, 0, len(voicing) - 1)    # ending note index (mapped residue to len(voicing))
            init_notes  = math.ceil(target_idx - idx + 1) * 4                           # actual number of notes (in pows of 4)
            init_idxs   = np.linspace(init_start, init_end, init_notes, dtype=int)      # indexes of notes (not actual notes)
            init_arp    = [voicing[pos] for pos in init_idxs]                           # broadcasting indexes to notes
            init_done   = False
            init_ptr    = 0

        last_res = res

        # before falling, a full complete arpeggio is always played
        if init_done == False:
            notes.append({"note": init_arp[init_ptr], "time": duration * i, "duration": duration })
            if init_ptr >= len(init_arp) - 1:
                init_done = True
            else:
                init_ptr += 1
 
        # notes on 1,1,1,1 from first half of arpeggio
        elif res >= DANGEROUS:
            notes.append({"note": random.choice(second_half), "time": duration * i, "duration": duration, "volume": 50 })

        # notes on 1,1,1,0 from middle part of arpeggio
        elif res >= HAZARDOUS and i % 4 != 3:
            notes.append({"note": random.choice(middle_part), "time": duration * i, "duration": duration, "volume": 50 })

        # notes on 1,0,1,0 from second half of arpeggio
        elif res >= BAD and i % 2 == 0:
            notes.append({"note": random.choice(first_half), "time": duration * i, "duration": duration, "volume": 50 })

    return notes


def get_residue_arpeggio(data, voicing):
    residue = get_residue(data)
    return arpeggiate(residue, voicing), residue

