
major = {
    "I":    [["IV", "V", "vi"], ["ii", "iii"], ["I", "vii°"]], 
    "ii":   [["IV", "V"], ["I", "iii", "vi"], ["ii", "vii°"]],
    "iii":  [["IV", "vi"], ["I", "ii", "V"], ["iii", "vii°"]],
    "IV":   [["I", "V"], ["ii", "iii", "vi", "vii°"], ["IV"]],
    "V":    [["I"], ["IV", "vi"], ["ii", "iii", "V", "vii°"]],
    "vi":   [["ii", "IV"], ["I", "iii", "V"], ["vi", "vii°"]],
    "vii°": [["I"], ["iii", "vi"], ["ii", "IV", "V", "vii°"]]
}

minor = {
    "i":    [["iv", "v", "bVI"], ["bIII", "bVII"], ["i", "ii°"]],
    "ii°":  [["i", "v", "bVII"], ["bIII", "iv", "bVI"], ["ii°"]],
    "bIII": [["iv", "bVI"], ["i", "v", "bVII"], ["ii°", "bIII"]],
    "iv":   [["i", "v", "bVII"], ["ii°", "bVI"], ["bIII", "iv"]],
    "v":    [["i"], ["iv", "bVI", "bVII"], ["ii°", "bIII", "v"]],
    "bVI":  [["ii°", "iv"], ["bVII", "v", "bVII"], ["i", "bVI"]],
    "bVII": [["i"], ["bVI", "v", "bIII"], ["ii°", "iv", "bVII"]]
}

minor_harmonic = {
    "i":    [["iv", "V", "bVI"], ["bIII", "vii°"], ["i", "ii°"]],
    "ii°":  [["i", "V", "vii°"], ["bIII", "iv", "bVI"], ["ii°"]],
    "bIII": [["iv", "bVI"], ["i", "V", "vii°"], ["ii°", "bIII"]],
    "iv":   [["i", "V", "vii°"], ["ii°", "bVI"], ["bIII", "iv"]],
    "V":    [["i"], ["iv", "bVI", "vii°"], ["ii°", "bIII", "V"]],
    "bVI":  [["ii°", "iv"], ["bIII", "vii°", "V"], ["i", "bVI"]],
    "vii°": [["i"], ["bVI", "V", "bIII"], ["ii°", "iv", "vii°"]]
}

major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
minor_scale = [0, 2, 3, 5, 7, 8, 10, 12]
harmonic_major_scale = [0, 2, 4, 5, 7, 8, 11, 12]
melodic__major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
harmonic_minor_scale = [0, 2, 3, 5, 7, 8, 11, 12]
melodic_minor_scale = [0, 2, 3, 5, 7, 9, 11, 12]

major_chord = [0, 4, 7]
minor_chord = [0, 3, 7]

major_arp = [0, 4, 7, 12]
minor_arp = [0, 3, 7, 12]

def get_major_arp(key):
    return [x + key for x in major_arp]

def get_minor_arp(key):
    return [x + key for x in minor_arp]

def get_scale(key, scale):
    return [x + key for x in scale]

def get_major_scale(key):
    return [x + key for x in major_scale]

def get_minor_scale(key):
    return [x + key for x in minor_scale]
