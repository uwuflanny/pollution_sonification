
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


def get_scale(key, scale):
    return [x + key for x in scale]

def get_major_scale(key):
    return [x + key for x in major_scale]

def get_minor_scale(key):
    return [x + key for x in minor_scale]
