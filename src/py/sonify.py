import os
import sys
import json
from lead import get_chords, get_lead
from residue import get_residue_arpeggio
from harmonizer import get_harmonization
from vsthost import get_vsts
from trackExporter import TrackExporter, merge_and_save
from animator import animate_data, merge_video
from sub import get_sub
from measures import convert, BPM, SIGN_DEN, SIGN_NUM


# load payload as json from arg
payload     = json.loads(sys.argv[1])
dir         = payload["dir"]
index       = payload["index"]
data        = payload["data"]
days        = payload["days"]

os.mkdir(dir)
os.chdir(dir)

# audio file exporter
exporter    = TrackExporter(BPM, SIGN_NUM, SIGN_DEN)

# load audio effects
gojira_delay, gojira_shimmer = get_vsts()

# convert index values
convert(index, data)

# midi content (get midi notes)
voicing     = get_harmonization(data)
arp, res    = get_residue_arpeggio(data, voicing)
prog        = get_chords(data, voicing)
lead        = get_lead(data, voicing)

# generate tracks (get samples)
lead        = exporter.create_track_samples("lead",  5, lead,  [gojira_shimmer], "lead")
arp         = exporter.create_track_samples("arp",   11,  arp,   [gojira_delay], "arp")
prog        = exporter.create_track_samples("prog",  0,  prog,  [], "prog")
sub         = get_sub(data)

# merge tracks, create animation, merge both
merge_and_save("final.wav", arp, lead, prog, sub)
animate_data(index, data, days, res, "animation.mp4")
merge_video("animation.mp4", "final.wav", "final.mp4")

