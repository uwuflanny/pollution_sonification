
from http.client import BAD_GATEWAY
from ssl import ALERT_DESCRIPTION_CLOSE_NOTIFY
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp
import random
import sys
from measures import RES_DECADENCE, min_thresh
from utility import map_value_int, map_value

def decrement(list, unit):
    return [x - unit for x in list if x - unit > 0]

def get_residue(data, res_threshold = min_thresh):

    residue_data    = []
    res_history     = []
      
    for pm in data:

        if pm >= res_threshold:
            residue_data.append(pm)
        
        res = max(residue_data) if len(residue_data) > 0 else 0
        res_history.append(res)
        ln_res = math.log(res, RES_DECADENCE) if res > 0 else 0
        residue_data = decrement(residue_data, ln_res)

    return res_history

def arpeggiate(residue, voicing):
    
    # given an index, find the last index of rising residue
    def get_rising_end(start):
        if start == len(residue) - 1:
            return start
        for i in range(start, len(residue)-1):
            if residue[i+1] < residue[i]:
                return i
        return len(residue) - 1

    # guard
    if not any(res >= min_thresh for res in residue):
        return []

    # find max value of residue
    max_res     = math.ceil(max(residue) / min_thresh) * min_thresh
    duration    = 0.25
    notes       = []
    voicing     = [x + 12 for x in voicing] # pitch shift voicing by 2 octaves
    last_res    = 0

    init_ptr    = 0
    init_done   = True
    target_idx  = -1

    # iterate len(residue) *4 times
    # each value in residue is a beat, each beat has 4 notes
    for i in range(len(residue) * 4):

        # check if a new beat has started
        if i % 4 == 0:

            idx = i // 4                                            # beat index
            res = residue[idx]                                      # residue value at beat index
            vol = map_value_int(res, 0, max_res, 0, 100)            # map residue value to volume
            last_res = residue[idx-1] if idx > 0 else 0             # previous residue value, last_res if idx = 0 is always 0

            # detect rising slope
            if res > last_res and res >= min_thresh and idx > target_idx:

                # find the end of the rising slope
                target_idx  = get_rising_end(idx)
                target_res  = residue[target_idx]

                arp_len     = map_value_int(target_res, 0, max_res, 0, len(voicing)-1)  # arpeggio lenght
                init_start  = map_value_int(res, 0, max_res, 0, len(voicing) - 1)       # initial note index (mapped residue to len(voicing))
                init_notes  = math.ceil(target_idx - idx + 1) * 4                       # actual number of notes (in pows of 4)
                init_idxs   = np.linspace(init_start, arp_len, init_notes, dtype=int)   # indexes of notes of initial arp (not actual notes)
                init_arp    = [voicing[pos] for pos in init_idxs]                       # broadcasting indexes to notes
                init_done   = False
                init_ptr    = 0

        # get dissonation
        dissonation = 0
        ratio = map_value_int(res, 0, max_res, 5, 2)
        value = map_value_int(res, 0, max_res, 2, 4)
        if i % ratio == 0:
            dissonation = random.randint(-value,value)  # TODO remove randomness

        # before falling, a full complete init arpeggio is always played
        if init_done == False:
            notes.append({"note": init_arp[init_ptr] + dissonation, "time": duration * i, "duration": duration, "volume": vol })
            if init_ptr >= len(init_arp) - 1:
                init_done = True
            else:
                init_ptr += 1

        # falling, note on 1,0,1,0
        elif res >= min_thresh and i % 2 == 0:
            note_idx = map_value_int(res, 0, max_res, 0, len(voicing) - 1)
            notes.append({"note": voicing[note_idx] + dissonation, "time": duration * i, "duration": duration, "volume": vol })

    return notes


def get_residue_arpeggio(data, voicing):
    residue = get_residue(data)
    return arpeggiate(residue, voicing), residue

