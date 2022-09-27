from midiutil.MidiFile import MIDIFile

class MidiBuilder:

    def __init__(self, time, tracks, sign_num, sign_den, beats):
        self.midi = MIDIFile(tracks)
        self.bpm = time
        self.tracks = tracks
        self.sign_num = sign_num
        self.sign_den = sign_den
        self.beats = beats

    def add_track(self, track_number, start_time, track_name):
        self.midi.addTrackName(track_number, start_time, track_name)
        self.midi.addTempo(track_number, start_time, self.bpm)

    def add_notes(self, notes, track, channel):
        for note in notes:
            # pitch, time, duration are required
            pitch, time, duration = note["note"], note["time"], note["duration"]
            # volume is optional
            volume = note["volume"] if "volume" in note else 100
            self.midi.addNote(track, channel, pitch, time, duration, volume)

    def get_beats(self):
        return self.beats

    def save(self, filename='result.mid'):
        with open(filename, "wb") as output_file:
            self.midi.writeFile(output_file)
