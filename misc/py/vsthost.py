import os
from pedalboard import Pedalboard, Reverb, load_plugin
from pedalboard.io import AudioFile

class VSTHost:

    def __init__(self, vst_path):
        self.vst_path = vst_path
        self.vst = load_plugin(vst_path)

    def apply_settings(self, settings):
        for key, value in settings.items():
            setattr(self.vst, key, value)            

    def print_parameters(self):
        for key, val in self.vst.parameters.items():
            print(key, val)

    def render(self, audio, samplerate):
        return self.vst(audio, samplerate)


