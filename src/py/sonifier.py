import os
import sys
from lead import get_chords, get_lead
from residue import get_residue_arpeggio
from harmonizer import get_harmonization
from vsthost import get_vsts
from trackExporter import TrackExporter, merge_and_save
from animator import animate_data, merge_video

# audio file exporter
bpm         = 120
sign_num    = 4
sign_den    = 4
exporter    = TrackExporter(bpm, sign_num, sign_num)

def export(data, folder):

    # audio effects
    gojira_delay, gojira_shimmer = get_vsts()

    # sonification folder
    os.mkdir(folder)

    # midi content
    voicing     = get_harmonization(data)
    arp, res    = get_residue_arpeggio(data, voicing)
    prog        = get_chords(data, voicing)
    lead        = get_lead(data, voicing)

    # generate tracks (get samples)
    lead        = exporter.create_track_samples("lead",  5, lead,  [gojira_shimmer], folder + "/lead")
    arp         = exporter.create_track_samples("arp",   11,  arp,   [gojira_delay], folder + "/arp")
    prog        = exporter.create_track_samples("prog",  0,  prog,  [], folder + "/prog")

    # merge tracks, create animation, merge both
    merge_and_save(folder + "/final.wav", arp, lead)
    animate_data(data, res, folder + "/animation.gif")
    merge_video(folder + "/animation.gif", folder + "/final.wav", folder + "/final.mp4")

    with open(folder + "/final.mp4", "rb") as f:
        data = f.read()
    os.system("rd /s /q " + folder)

    return data
    

