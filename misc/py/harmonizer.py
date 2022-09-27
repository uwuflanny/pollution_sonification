


def MidiStringToInt(midstr):
    Notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
    answer = 0
    i = 0
    #Note
    letter = midstr.split('-')[0].upper()
    for note in Notes:
        for form in note:
            if letter.upper() == form:
                answer = i
                break
        i += 1
    #Octave
    answer += (int(midstr[-1]))*12
    return answer

def get_harmonization():

    voicing = ['C-1','C-2','G-2',
            'C-3','E-3','G-3','A-3','B-3',
            'D-4','E-4','G-4','A-4','B-4',
            'D-5','E-5','G-5','A-5','B-5',
            'D-6','E-6','F#-6','G-6','A-6']

    voicing_midi = [MidiStringToInt(note) for note in voicing]
    leading = voicing_midi[0]
    octave_shift = 12 * 4

    chord = [0, 4, 7]
    chord = [x + leading + octave_shift for x in chord]
    arpeggio = [0, 4, 7, 12]
    arpeggio = [x + leading + octave_shift for x in arpeggio]

    return voicing_midi, leading, arpeggio, chord

    
    



    
