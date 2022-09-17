from midiutil.MidiFile import MIDIFile
from os import replace
import numpy as np
import math
import json
import sys
import string
import os 
from notes import get_minor_scale, get_major_arp
from residue import get_residue, get_residue_states, assign_notes
import matplotlib.pyplot as plt

# settings
time = 120
tracks = 1
sign_num = 4
sign_den = 4
beats = 20
bpm = 120
outputMidiFile = MIDIFile(tracks)





data    = [30,40,10,20,40,60,10,30,50,10,220,20,30,10,30,20,30,10,30,20,30,10,30,20,30,10,30,70,30,10,30,20,30,10,30,20,30,10,30,20,30,10,30,180,70,90,90,90,90,90,89,20,30,10,30,20,30,10,150,20,30,10,30,20,30,10,30,20,30,10,30,20,50,10,30,20,30,10,30]
residue = get_residue(data)
states  = get_residue_states(residue)
arp     = get_major_arp(60)
notes   = assign_notes(states, arp)


# render audio
elapsedQuarters = 0
outputMidiFile.addTrackName(0, elapsedQuarters, "arpeggio")
outputMidiFile.addTempo(0, elapsedQuarters, bpm)
for note in notes:
    pitch, time, duration = note["note"], note["time"], note["duration"]
    outputMidiFile.addNote(0, 0, pitch, time, duration, 100)
    elapsedQuarters += 0.25

# plot data blue residue red
plt.plot(data, 'b')
plt.plot(residue, 'r')
plt.plot(states, 'g')
plt.show()



# save file as midi
with open("result.mid", 'wb') as outf:
    outputMidiFile.writeFile(outf)
  
