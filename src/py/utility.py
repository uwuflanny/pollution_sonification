
import math

def map_value(value, in_min, in_max, out_min, out_max):
    if in_min == in_max:
        return (out_min + out_max) / 2
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def map_value_int(value, in_min, in_max, out_min, out_max):
    return math.floor(map_value(value, in_min, in_max, out_min, out_max))

