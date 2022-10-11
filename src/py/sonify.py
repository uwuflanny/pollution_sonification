import os
import sys
from lead import get_chords, get_lead
from residue import get_residue_arpeggio
from harmonizer import get_harmonization
from vsthost import get_vsts
from trackExporter import TrackExporter, merge_and_save
from animator import animate_data, merge_video
from ast import literal_eval

# audio file exporter
bpm         = 120
sign_num    = 4
sign_den    = 4
exporter    = TrackExporter(bpm, sign_num, sign_num)

dir = sys.argv[1]
os.mkdir(dir)
os.chdir(dir)

data = sys.argv[2]
data = literal_eval(data)

# audio effects
gojira_delay, gojira_shimmer = get_vsts()

# midi content
voicing     = get_harmonization(data)
arp, res    = get_residue_arpeggio(data, voicing)
prog        = get_chords(data, voicing)
lead        = get_lead(data, voicing)

# generate tracks (get samples)
lead        = exporter.create_track_samples("lead",  5, lead,  [gojira_shimmer], "lead")
arp         = exporter.create_track_samples("arp",   11,  arp,   [gojira_delay], "arp")
prog        = exporter.create_track_samples("prog",  0,  prog,  [], "prog")

# merge tracks, create animation, merge both
merge_and_save("final.wav", arp, lead)
animate_data(data, res, "animation.gif")
merge_video("animation.gif", "final.wav", "final.mp4")

with open("final.mp4", "rb") as f:
    data = f.read()

    

