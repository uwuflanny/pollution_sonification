
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy as sp


def decrement(list, unit):
    return [x - unit for x in list if x - unit > 0]

def get_residue(data, res_threshold = 50):

    residue_data    = []
    res_history     = []
    DECADENCE       = 2
    
    for pm in data:

        if pm > res_threshold:
            residue_data.append(pm)
        
        res = max(residue_data) if len(residue_data) > 0 else 0
        res_history.append(res)
        ln_res = math.log(res, DECADENCE) if res > 0 else 0
        residue_data = decrement(residue_data, ln_res)

    return res_history

def get_residue_states(data):

    levels  = [
        0,      # REST
        50,     # FALLING
        100,    # HARARDOUS
        150,    # DANGEROUS
        200     # LETHAL
    ]
    rising  = max(levels) + 50
    states  = []
    last    = 0

    for residue in data:

        level = levels[0]
        for i in range(1, len(levels)):
            if residue > levels[i]:
                level = levels[i]
            else:
                break
 
        states.append(rising if level > last else level)
        last = level

    return states

