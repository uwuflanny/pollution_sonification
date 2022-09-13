from midiutil.MidiFile import MIDIFile
from os import replace
import numpy as np
import math
import json
import sys
import string
import os 
from notes import get_minor_scale


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
piano = 1
outputMidiFile.addTrackName(0, elapsedQuarters, "drums")
outputMidiFile.addTempo(0, elapsedQuarters, bpm)
scale = get_minor_scale(60)
for i in range(beats):
    outputMidiFile.addNote(0, piano, scale[i % len(scale)], elapsedQuarters, 0.25, 100) #0.25 = a quarter of a beat (quarter)
    elapsedQuarters += sign_num / (sign_den / 4)


# save file as midi
with open("result.mid", 'wb') as outf:
    outputMidiFile.writeFile(outf)
  
