import math

def map_value(value, min_value, max_value, min_result, max_result):
    return min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)

def map_value_int(value, min_value, max_value, min_result, max_result):
    return math.floor(map_value(value, min_value, max_value, min_result, max_result))

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
        vol = map_value_int(aqi, best, worst, 50, 100)
        notes += [{"note": note + oct * 12, "time": i * 4, "duration": 4, "volume": vol} for note in chord]

    return notes

def get_lead(data, voicing):

    voicing = voicing[::-1]
    data    = [map_value(x, 0, max(data), 0, 1) for x in data]
    n_notes = len(voicing)
    notes   = []

    for i in range(len(data)):
        note_index = math.floor(map_value(data[i], 0, 1, 0, n_notes - 1))
        notes.append({"note": voicing[note_index], "time": i, "duration": 1})

    return notes

