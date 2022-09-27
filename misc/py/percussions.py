
def get_kicks(data):
    return [{
        "note": 36,
        "time": i,
        "duration": 0.25,
        "volume": 100
    } for i in range(len(data))]

def get_claps(data):

    # group data by averages of 4 consecutive elements
    avgs = [sum(data[i:i+4]) / 4 for i in range(0, len(data), 4)]

    claps = []
    for i in range(len(avgs)):
        aqi = avgs[i]
        if aqi >= 50:
            claps.append({
                "note": 39,
                "time": i * 4 + 3.5,
                "duration": 0.25,
                "volume": 100
            })
            claps.append({
                "note": 39,
                "time": i * 4 + 3.75,
                "duration": 0.25,
                "volume": 100
            })

    return claps