from midiutil.MidiFile import MIDIFile
from os import replace
import numpy as np
import math
import json
import sys
import string
import os 
from notes import get_minor_scale
from residue import get_residue, get_residue_states
import matplotlib.pyplot as plt

# settings
time = 120
tracks = 1
sign_num = 4
sign_den = 4
beats = 20
bpm = 120
outputMidiFile = MIDIFile(tracks)


# render audio
elapsedQuarters = 0
outputMidiFile.addTrackName(0, elapsedQuarters, "drums")
outputMidiFile.addTempo(0, elapsedQuarters, bpm)
scale = get_minor_scale(60)
for i in range(beats):
    outputMidiFile.addNote(0, 1, scale[i % len(scale)], elapsedQuarters, 0.25, 100) #0.25 = a quarter of a beat (quarter)
    elapsedQuarters += sign_num / (sign_den / 4)


data = [30,40,10,20,40,60,10,30,50,10,220,20,30,10,30,20,30,10,30,20,30,10,30,20,30,10,30,70,30,10,30,20,30,10,30,20,30,10,30,20,30,10,30,180,70,90,90,90,90,90,89,20,30,10,30,20,30,10,150,20,30,10,30,20,30,10,30,20,30,10,30,20,50,10,30,20,30,10,30]
residue = get_residue(data)
states = get_residue_states(residue)
# plot data blue residue red
plt.plot(data, 'b')
plt.plot(residue, 'r')
plt.plot(states, 'g')
plt.show()

# save file as midi
with open("result.mid", 'wb') as outf:
    outputMidiFile.writeFile(outf)
  
