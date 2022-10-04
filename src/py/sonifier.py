import sys
import numpy as np
from turtle import left
from lead import get_chords, get_lead
from residue import get_residue_arpeggio
from harmonizer import get_harmonization
from vsthost import get_vsts
from trackExporter import TrackExporter, merge_and_save
from pydub import AudioSegment
from animator import animate_data, merge_video
from pedalboard.io import AudioFile
from pydub import AudioSegment

# audio effects
gojira_delay, gojira_shimmer = get_vsts()

# audio file exporter
bpm         = 120
sign_num    = 4
sign_den    = 4
exporter    = TrackExporter(bpm, sign_num, sign_num)

def export(data):

    # midi content
    voicing     = get_harmonization(data)
    arp, res    = get_residue_arpeggio(data, voicing)
    prog        = get_chords(data, voicing)
    lead        = get_lead(data, voicing)

    # generate tracks (get samples)
    lead        = exporter.create_track_samples("lead",  11, lead,  [], "lead")
    arp         = exporter.create_track_samples("arp",   5,  arp,   [], "arp")
    prog        = exporter.create_track_samples("prog",  0,  prog,  [], "prog")

    # merge tracks, create animation, merge both
    merge_and_save(lead, arp, prog)
    animate_data(data, res)
    merge_video("animation.gif", "final.wav", "final.mp4")

    # cleanup
    import os
    os.system("del *wav")
    os.system("del *mid")
    os.system("del *gif")
