import os
from midiutil.MidiFile import MIDIFile
from pedalboard.io import AudioFile
from pydub import AudioSegment


class TrackExporter:

    def __init__(self, time, sign_num, sign_den, beats):
        self.bpm        = time
        self.sign_num   = sign_num
        self.sign_den   = sign_den
        self.beats      = beats

    def export_track(self, track_name, instrument, notes, vsts, filename):

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
            audio = f.read(f.frames)
            samplerate = f.samplerate

        for vst in vsts:
            audio = vst.render(audio, samplerate)

        with AudioFile(wav_filename, 'w', samplerate, audio.shape[0]) as f:
            f.write(audio)

        # return audio to merge later ?
        return wav_filename



        

