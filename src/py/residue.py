
from http.client import BAD_GATEWAY
from ssl import ALERT_DESCRIPTION_CLOSE_NOTIFY
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


def map_value_int(value, min_value, max_value, min_result, max_result):
    return math.floor(min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result))

def arpeggiate(residue, voicing, max):
    
    def get_rising_end(start):
        if start == len(residue) - 1:
            return start
        for i in range(start, len(residue)-1):
            if residue[i+1] < residue[i]:
                return i
        return len(residue) - 1


    duration    = 0.25
    notes       = []
    voicing     = [x + 24 for x in voicing] # pitch shift voicing by 2 octaves

    target      = -1
    last        = 0
    arp_len     = 0
    arpeggio    = []

    init_start  = 0
    init_len    = 0
    init_ptr    = 0
    init_done   = True


    for i in range(len(residue) * 4):

        idx = i // 4
        val = residue[idx] 

        # rising
        if val > last and val >= 50 and idx > target:

            target = get_rising_end(idx)
            target_val = residue[target]
            arp_len = map_value_int(target_val, 0, max, 0, len(voicing)-1) # is mapping WITH MAX correct ?
            arpeggio = voicing[0:arp_len]

            init_start = map_value_int(last, 0, max, 0, len(voicing)-1)
            init_len = map_value_int(target_val, 0, max, 0, len(voicing)-1) - init_start
            init_ptr = 0
            init_done = False

        last = val

        # before falling, a full complete arpeggio is always played
        if init_done == False:
            notes.append({"note": voicing[init_start + init_ptr], "time": duration * i, "duration": duration })
            if init_ptr >= init_len:
                init_done = True
            else:
                init_ptr += 1
 
        # notes on 1,1,1,1 from first half of arpeggio
        elif val >= DANGEROUS:
            second_half = arpeggio[math.floor(len(arpeggio)/2):]
            notes.append({"note": random.choice(second_half), "time": duration * i, "duration": duration })

        # notes on 1,1,1,0 from middle part of arpeggio
        elif val >= HAZARDOUS:
            if i % 4 != 3:  
                middle_part = arpeggio[math.floor(len(arpeggio)/4):math.floor(len(arpeggio)/4*3)]
                notes.append({"note": random.choice(middle_part), "time": duration * i, "duration": duration })

        # notes on 1,0,1,0 from second half of arpeggio
        elif val >= BAD:
            if i % 2 == 0:  
                first_half = arpeggio[0:math.floor(len(arpeggio)/2)]
                notes.append({"note": random.choice(first_half), "time": duration * i, "duration": duration })


    return notes


def get_residue_arpeggio(data, voicing):
    max = np.max(data)
    residue = get_residue(data)
    return arpeggiate(residue, voicing, max)
