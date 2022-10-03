from lead import get_chords, get_lead
from residue import get_residue_arpeggio
from harmonizer import get_harmonization
from vsthost import get_vsts
from trackExporter import TrackExporter
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
    arpeggio    = get_residue_arpeggio(data, voicing)
    progression = get_chords(data, voicing)
    lead        = get_lead(data, voicing)

    # generate tracks
    lead        = exporter.export_track("lead",  11, lead,       [gojira_shimmer],   "lead")
    arp         = exporter.export_track("arp",   5,  arpeggio,   [gojira_delay],     "arp")
    prog        = exporter.export_track("prog",  0,  progression,[],                 "prog")

    # mix tracks
    lead_wav    = AudioSegment.from_wav(lead)
    arp_wav     = AudioSegment.from_wav(arp)
    prog_wav    = AudioSegment.from_wav(prog)
    lead_wav    = lead_wav + 5 # make sound louder
    prog_wav    = prog_wav - 4 # make sound quiter

    # cleanup
    import os
    os.system("del *wav")
    os.system("del *mid")

    # export
    overlay = lead_wav.overlay(arp_wav, position=0)
    overlay = overlay.overlay(prog_wav, position=0)
    overlay.export("final.wav", format="wav")



