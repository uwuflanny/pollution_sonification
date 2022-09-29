import wave
import sys
from lead import randomize_progression, get_lead
from residue import get_residue_arpeggio
from wave_buffer import calculate_wavetable
from harmonizer import get_harmonization
from vsthost import VSTHost
from trackExporter import TrackExporter
from pydub import AudioSegment


# load gojira delay
gojira_delay = VSTHost("C:\Program Files\Common Files\VST3\\Neural DSP\Archetype Gojira.vst3")
gojira_delay.apply_settings({
    "amp_section_active": "Inactive",
    "cab_section_active": "Inactive",
    "dly_active": "Active",
    "dly_sync_active": "Inactive",
    "dly_dry_wet": 0.5,
})

# load gojira shimmer reverb
gojira_shimmer = VSTHost("C:\Program Files\Common Files\VST3\\Neural DSP\Archetype Gojira.vst3")
gojira_shimmer.apply_settings({
    "amp_section_active": "Inactive",
    "cab_section_active": "Inactive",
    "rev_active": "Active",
    "rev_dry_wet": 0.5,
    "rev_mode": "Shimmer"
})



# data input
data = [30,40,10,20,40,60,10,30,50,10,110,20,12,10,50,20,30,10,45,20,30,10,5,20,23,10,30,70,30,10,12,12,30,10,30,20,30,10,30,20,30,10,30,180,70,90,90,90,90,90,89,20,30,10,30,20,100,120,150,66,12,10,30,66,15,10,30,20,55,10,30,20,50,10,30,44,30,10,30]
# data = [184,184,185,184,182,181,179,177,175,176,177,178,176,175,173,173,172,172,172,172,172,171,170,169,165,161,157,152,147,136,135,134,133,149,155,163,165,166,168,167,167,166,163,160,157,154,152,152,151,152,154,156,158,160,162,164,166,168,171,173,170,167,164,161,157,154,155,156,156,157,158,159,160,162,167,172,177,183,179,175,170,164,158,151,152,152,153,156,160,163,156,148,141,142,142,143,146,148,151,156,162,167,166,165,163,157,151,146,148,150,152,159,166,173,169,165,161,165,168,172,174,176,178,176,173,171,165,159,153,150,148,145,153,160,168,172,176,180,176,171,166,167,169,170,173,176,179,175,171,168,160,153,146,143,141,139,145,151,157,168,178,189,181,173,165,167,169,171,173,174,176,173,169,166,161,156,150,146,143,139,138,137,137,151,164,178,173,169,170,169,167,165,166,167,171,182,192,209,198,192,187,186,185,184,175,167,172,162,152,138,134,131,127,127,126,126,123,120,117,124,131,138,153,165,176,172,168,164,155,145,126,128,129,131,136,142,148,146,143,141,130,118,107,101,97,92,90,89,87,94,101,108,101,96,91,92,93,94,96,98,99,100,101,102,111,119,128,131,134,137,149,154,160,167,174,182,180,179,177,172,167,162,159,157,154,154,153,153,156]


# midi content
voicing, key, arp, chord    = get_harmonization()
arpeggio                    = get_residue_arpeggio(data, voicing)
progression                 = randomize_progression(data, chord)
lead                        = get_lead(data, voicing)


# audio file exporter
bpm         = 120
sign_num    = 4
sign_den    = 4
beats       = len(data)
exporter    = TrackExporter(120, 4, 4, len(data))


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

overlay = lead_wav.overlay(arp_wav, position=0)
overlay = overlay.overlay(prog_wav, position=0)
file_handle = overlay.export("final.wav", format="wav")

