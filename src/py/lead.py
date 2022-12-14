import math
from measures import min_thresh
from utility import map_value_int, map_value


def get_chords(data, voicing):

    # group data by averages of 4 consecutive elements
    chord   = voicing[0:5:2]
    avgs    = [sum(data[i:i+4]) / 4 for i in range(0, len(data), 4)]
    best    = min(avgs)
    worst   = max(avgs)
    notes   = []
    
    for i in range(len(avgs)):
        aqi = avgs[i]
        oct = map_value_int(aqi, best, worst, 2, 0)
        vol = map_value_int(aqi, best, worst, 60, 20)
        notes += [{"note": note + oct * 12, "time": i * 4, "duration": 4, "volume": vol} for note in chord]

    return notes

def get_lead(data, voicing):

    voicing = voicing[::-1]
    n_notes = len(voicing)
    best    = min(data)
    worst   = max(data)
    notes   = []

    for i in range(len(data)):
        aqi         = data[i]
        vol         = 75 if aqi < min_thresh else map_value_int(aqi, best, worst, 50, 25)
        note_index  = math.floor(map_value(aqi, best, worst, 0, n_notes - 1))
        notes.append({"note": voicing[note_index], "time": i, "duration": 1, "volume": vol })

    return notes

