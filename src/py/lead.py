import random

def map_value(value, min_value, max_value, min_result, max_result):
    result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
    return result

def randomize_progression(data, chord):
    # group data by averages of 4 consecutive elements
    avgs = [sum(data[i:i+4]) / 4 for i in range(0, len(data), 4)]
    notes   = []
    for i in range(len(avgs)):
        # select maj / min
        aqi = avgs[i]
        # add chord
        if aqi >= 25:
            notes += [{"note": note, "time": i * 4, "duration": 4} for note in chord]
        # add bass
        notes.append({"note": chord[0] - 12, "time": i * 4, "duration": 4, "volume": 100})

    return notes


def get_lead(data, voicing):

    MAX_AQI = 800
    notes = []
    data = [map_value(x, 0, MAX_AQI, 0, 1) for x in data]
    n_notes = len(voicing)

    for i in range(len(data)):
        note_index = round(map_value(data[i], 0, 1, n_notes-1, 0))
        notes.append({"note": voicing[note_index], "time": i, "duration": 1})

    return notes







