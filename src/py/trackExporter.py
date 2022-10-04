import os
import sys
import numpy as np
from midiutil.MidiFile import MIDIFile
from pedalboard.io import AudioFile
from pydub import AudioSegment


def merge_and_save(*tracks):

    # find max number of samples, add padding and merge by sum
    maxlen  = max([len(track[1]) for track in tracks])
    padded  = [np.pad(track, ((0,0), (0, maxlen - len(track[0]))), 'constant', constant_values=0) for track in tracks]
    final   = np.sum(padded, axis=0)

    # export to wav
    with AudioFile('final.wav', 'w', 44100, final.shape[0]) as f:
        f.write(final)


class TrackExporter:

    def __init__(self, time, sign_num, sign_den):
        self.bpm        = time
        self.sign_num   = sign_num
        self.sign_den   = sign_den

    def create_track_samples(self, track_name, instrument, notes, vsts, filename):

        midi_filename   = filename + ".mid"
        wav_filename    = filename + ".wav"

        # create midi file
        midi = MIDIFile(1)
        midi.addTrackName(0, 0, track_name)
        midi.addTempo(0, 0, self.bpm)
        midi.addProgramChange(0, 0, 0, instrument)

        # add notes
        for note in notes:
            # pitch, time, duration are required
            pitch, time, duration = note["note"], note["time"], note["duration"]
            # volume is optional
            volume = note["volume"] if "volume" in note else 100
            midi.addNote(0, 0, pitch, time, duration, volume)

        # save midi file
        with open(midi_filename, "wb") as output_file:
            midi.writeFile(output_file)

        # convert midi to wav, preserve silence is important
        os.system('timidity ' + midi_filename + ' -Ow --preserve-silence -t 120')

        # apply vsts
        with AudioFile(wav_filename, 'r') as f:
            samples = f.read(f.frames)
            samplerate = f.samplerate

        for vst in vsts:
            samples = vst.render(samples, samplerate)

        return samples



        

