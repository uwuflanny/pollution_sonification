
import math
import numpy as np

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def map_value_int(value, in_min, in_max, out_min, out_max):
    return math.floor(map_value(value, in_min, in_max, out_min, out_max))

