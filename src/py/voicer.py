from trackExporter import TrackExporter
from harmonizer import note_to_midi

def build_and_export(set):
    bpm         = 120
    sign_num    = 4
    sign_den    = 4
    exporter    = TrackExporter(bpm, sign_num, sign_num)
    notes = []
    for i in range(len(set)):
        notes.append({"note":set[i], "time":i * 0.25, "duration":1, "volume":100})
    exporter.export_track("test",  1, notes,   [],   "test")



# 0 = perfect fifth, 1 = major third, 2 = minor third
harmonics = {
    "A":    ["E", "C#", "C"],
    "B":    ["F#", "D#", "D"],
    "C":    ["G", "E", "D#"],
    "D":    ["A", "F#", "F"],
    "E":    ["B", "G#", "G"],
    "F":    ["C", "A", "G#"],
    "G":    ["D", "B", "A#"],
    "A#":   ["F", "D", "C#"],
    "C#":   ["G#", "E", "D#"],
    "D#":   ["A#", "F#", "F"],
    "F#":   ["C#", "A", "G#"],
    "G#":   ["D#", "B", "A#"]
}




ionian_maj          = ["C", "D", "E", "F", "G", "A", "B"]
dorian_maj          = ["D", "E", "F", "G", "A", "B", "C"],
phrygian_maj        = ["E", "F", "G", "A", "B", "C", "D"],
lydian_maj          = ["F", "G", "A", "B", "C", "D", "E"],
mixolydian_maj      = ["G", "A", "B", "C", "D", "E", "F"],
aeolian_minor_maj   = ["A", "B", "C", "D", "E", "F", "G"],
locrian_maj         = ["B", "C", "D", "E", "F", "G", "A"],


ionian_min          = ["C", "D", "E", "F", "G#", "A", "B"]
dorian_min          = ["D", "E", "F", "G#", "A", "B", "C"],
mixolydian_min      = ["E", "F", "G#", "A", "B", "C", "D"],
lydian_min          = ["F", "G#", "A", "B", "C", "D", "E"],
locrian_min         = ["G#", "A", "B", "C", "D", "E", "F"],
aeolian_min         = ["A", "B", "C", "D", "E", "F", "G#"]
locrian_min         = ["B", "C", "D", "E", "F", "G#", "A"]




major           = ["C", "D", "E", "F", "G", "A", "B"]
minor           = ["C", "D", "D#", "F", "G", "G#", "A#"]
melodic_minor   = ["C", "D", "D#", "F", "G", "A", "B"]
harmonic_minor  = ["C", "D", "D#", "F", "G", "G#", "B"]
myxolydian      = ["C", "D", "E", "F", "G", "A", "A#"]
dorian          = ["C", "D", "D#", "F", "G", "A", "A#"]
diminished      = ["C", "D", "E", "F#", "G#", "A#", "A#"]

major           = [0, 2, 4, 5, 7, 9, 11]
minor           = [0, 2, 3, 5, 7, 8, 10]
melodic_minor   = [0, 2, 3, 5, 7, 9, 11]
harmonic_minor  = [0, 2, 3, 5, 7, 8, 11]


scale = major
scale = [x + 36 for x in scale] + [x + 48 for x in harmonic_minor] + [x + 60 for x in major] + [x + 72 for x in harmonic_minor]
build_and_export(scale)