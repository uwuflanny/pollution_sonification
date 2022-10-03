
def note_to_midi(midstr):
    notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
    answer = 0
    i = 0
    #Note
    letter = midstr.split('-')[0].upper()
    for note in notes:
        for form in note:
            if letter.upper() == form:
                answer = i
                break
        i += 1
    #Octave
    answer += (int(midstr[-1]))*12
    return answer

def get_harmonization(data):

    # scales
    major           = [0, 2, 4, 5, 7, 9, 11]
    minor           = [0, 2, 3, 5, 7, 8, 10]
    melodic_minor   = [0, 2, 3, 5, 7, 9, 11]
    harmonic_minor  = [0, 2, 3, 5, 7, 8, 11]

    # [0, 2, 3, 5, 7, 8, 11, 0, 2, 3, 5, 7, 8, 11, 0, 2, 3, 5, 7, 8, 11, 0, 2, 3, 5, 7, 8, 11]
    scales = [
        major,
        minor,
        melodic_minor,
        harmonic_minor
    ]

    # get scale based on average aqi
    avg = sum(data) / len(data)
    scale = scales[(int)(-1 if avg // 50 > len(scales)-1 else avg // 50)]

    # voice scale and return
    key = 36
    return [x + key + 12 for x in scale] + [x + key + 24 for x in scale] + [x + key + 36 for x in scale]

    
    



    
