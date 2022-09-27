
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



def map_value(value, min_value, max_value, min_result, max_result):
    result = min_result + (value - min_value)/(max_value - min_value)*(max_result - min_result)
    return result

    

data = [30,40,10,20,40,60,10,30,50,10,220,20,30,10,30,20,30,10,30,20,30,10,30,20,30,10,30,70,30,10,30,20,30,10,30,20,30,10,30,20,30,10,30,180,70,90,90,90,90,90,89,20,30,10,30,20,30,10,150,20,30,10,30,20,30,10,30,20,30,10,30,20,50,10,30,20,30,10,30]
# data = [184,184,185,184,182,181,179,177,175,176,177,178,176,175,173,173,172,172,172,172,172,171,170,169,165,161,157,152,147,136,135,134,133,149,155,163,165,166,168,167,167,166,163,160,157,154,152,152,151,152,154,156,158,160,162,164,166,168,171,173,170,167,164,161,157,154,155,156,156,157,158,159,160,162,167,172,177,183,179,175,170,164,158,151,152,152,153,156,160,163,156,148,141,142,142,143,146,148,151,156,162,167,166,165,163,157,151,146,148,150,152,159,166,173,169,165,161,165,168,172,174,176,178,176,173,171,165,159,153,150,148,145,153,160,168,172,176,180,176,171,166,167,169,170,173,176,179,175,171,168,160,153,146,143,141,139,145,151,157,168,178,189,181,173,165,167,169,171,173,174,176,173,169,166,161,156,150,146,143,139,138,137,137,151,164,178,173,169,170,169,167,165,166,167,171,182,192,209,198,192,187,186,185,184,175,167,172,162,152,138,134,131,127,127,126,126,123,120,117,124,131,138,153,165,176,172,168,164,155,145,126,128,129,131,136,142,148,146,143,141,130,118,107,101,97,92,90,89,87,94,101,108,101,96,91,92,93,94,96,98,99,100,101,102,111,119,128,131,134,137,149,154,160,167,174,182,180,179,177,172,167,162,159,157,154,154,153,153,156]

# map data from 0 to 1
data = [map_value(x, 0, max(data), 0, 1) for x in data]

note_names = ['C-1','C-2','G-2',
             'C-3','E-3','G-3','A-3','B-3',
             'D-4','E-4','G-4','A-4','B-4',
             'D-5','E-5','G-5','A-5','B-5',
             'D-6','E-6','F#-6','G-6','A-6']

note_numbers = [MidiStringToInt(note) for note in note_names]
n_notes = len(note_numbers)

midi_data = []
for i in range(len(data)):
    note_index = round(map_value(data[i], 0, 1, n_notes-1, 0))
    midi_data.append(note_numbers[note_index])


vel_min,vel_max = 35,127
vel_data = []
for i in range(len(data)):
    note_velocity = round(map_value(data[i], 0, 1, vel_min, vel_max))
    vel_data.append(note_velocity)


from midiutil import MIDIFile #import library to make midi file, https://midiutil.readthedocs.io/en/1.2.1/
    
#create midi file object, add tempo
my_midi_file = MIDIFile(1) #one track 
my_midi_file.addTempo(track=0, time=0, tempo=120) 

#add midi notes
for i in range(len(data)):
    my_midi_file.addNote(track=0, channel=0, pitch=midi_data[i], time=i, duration=2, volume=vel_data[i])

#create and save the midi file itself
with open("asd" + '.mid', "wb") as f:
    my_midi_file.writeFile(f) 